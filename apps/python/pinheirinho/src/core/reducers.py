from src.core.state import RaceState, LaneState, RaceInputs, RaceStatus, LaneStatus, RaceLights, create_initial_lights

# ==========================================
# 1. LANE REDUCER (Per Car Logic)
# ==========================================

def lane_reducer(old_lane, is_pre, is_stage, speed_kmh, elapsed_dist, current_time, race_status, green_time):
    """
    Pure function to determine the next state of a single lane.
    inputs:
        old_lane: LaneState
        is_pre, is_stage: Booleans from sensors
        race_status: Global RaceStatus
    """
    new_status = old_lane.status
    fault_reason = old_lane.fault_reason
    
    # If already finished or disqualified, state is terminal (mostly)
    # Exception: Maybe reset? (Handled by global reset logic, not here)
    if old_lane.status in [LaneStatus.FINISHED, LaneStatus.FAULT]:
        return old_lane

    # --- FAULT DETECTION (Jump Start) ---
    # Moved before Green Light AND Race is in Sequence
    # Tolerance: speed > 1.0 km/h (?) or dist > 0.1m? 
    # Let's use speed for now, or combination.
    MOVEMENT_THRESHOLD_KMH = 5.0 # Tolerance for "creeping"
    
    if race_status == RaceStatus.SEQUENCE:
        if speed_kmh > MOVEMENT_THRESHOLD_KMH or (not is_stage and not is_pre):
             # Left the beams during sequence = Jump Start
             # Or strict movement check
             return LaneState(LaneStatus.FAULT, 0.0, 0.0, speed_kmh, "JUMP START")

    # --- STAGING LOGIC ---
    if race_status in [RaceStatus.WAITING, RaceStatus.STAGING]:
        if is_pre and is_stage:
            new_status = LaneStatus.STAGED
        elif is_pre and not is_stage:
            new_status = LaneStatus.PRE_STAGE
        elif is_stage and not is_pre:
            # Deep Stage violation
            new_status = LaneStatus.DEEP_STAGE_WARNING
        else:
            new_status = LaneStatus.IDLE
            
    # --- RACING LOGIC ---
    if race_status == RaceStatus.RACING:
        # Check if crossed finish line
        # Assuming track length is standard 402m (1/4 mile) or 201m (1/8)
        # We need track config passed in inputs? 
        # For now, let's assume Finish is handled if speed > 0 and distance > 402
        # BUT we don't have distance in inputs yet in the plan properly mapped.
        # Let's trust "is_finished" sensor or similar. 
        # For Phase 1, we focus on Start logic.
        new_status = LaneStatus.RACING
        
    return LaneState(new_status, old_lane.reaction_time, old_lane.elapsed_time, speed_kmh, fault_reason)

# ==========================================
# 2. RACE REDUCER (Global Logic)
# ==========================================

def race_reducer(state, inputs):
    """
    Main State Transition Function.
    (old_state, input_data) -> new_state
    """
    now = inputs.time
    
    # 1. Update Lanes first (Independent logic)
    green_ts = state.race_start_time if state.race_start_time else 0.0
    
    new_left = lane_reducer(state.left_lane, inputs.left_in_pre, inputs.left_in_stage, 
                           inputs.left_speed_kmh, inputs.left_dist_traveled, now, state.status, green_ts)
                           
    new_right = lane_reducer(state.right_lane, inputs.right_in_pre, inputs.right_in_stage,
                            inputs.right_speed_kmh, inputs.right_dist_traveled, now, state.status, green_ts)

    # 2. Global State Transitions
    status = state.status
    stage_ts = state.stage_timer_start
    seq_ts = state.sequence_start
    race_ts = state.race_start_time
    
    # --- WAITING -> STAGING ---
    if status == RaceStatus.WAITING:
        # If anyone enters Pre-Stage or Staged, we are preparing
        if (new_left.status >= LaneStatus.PRE_STAGE) or (new_right.status >= LaneStatus.PRE_STAGE):
            status = RaceStatus.STAGING
            # Timer doesn't start yet, only when STAGED

    # --- STAGING LOGIC (7s Rule) ---
    if status == RaceStatus.STAGING:
        left_ready = (new_left.status == LaneStatus.STAGED)
        right_ready = (new_right.status == LaneStatus.STAGED)
        
        # Start timer if one is ready and timer not running
        if (left_ready or right_ready) and stage_ts is None:
            stage_ts = now
        
        # Reset timer if nobody is ready (backed out)
        if not left_ready and not right_ready:
            stage_ts = None
            
        # Check for ALL READY -> Start Sequence
        if left_ready and right_ready:
            # OPTIONAL: Add a small delay 'Auto-Start' or go straight
            status = RaceStatus.SEQUENCE
            seq_ts = now # Sequence starts NOW
            stage_ts = None # Clear staging timer
            
        # Check 7s Timeout
        elif stage_ts is not None and (now - stage_ts > 7.0):
            # Who is not ready?
            if not left_ready:
                new_left = new_left._replace(status=LaneStatus.FAULT, fault_reason="TIMEOUT 7s")
            if not right_ready:
                new_right = new_right._replace(status=LaneStatus.FAULT, fault_reason="TIMEOUT 7s")
            
            # If someone faulted, do we proceed?
            # Typically, the valid car gets a solo run (Bye run)
            # So we proceed to Sequence for the survivor
            status = RaceStatus.SEQUENCE
            seq_ts = now
            
    # --- SEQUENCE (The Tree) ---
    if status == RaceStatus.SEQUENCE:
        # Sportsman Tree: 1.5s delay + 0.5 + 0.5 + 0.5
        time_since_seq = now - seq_ts
        TOTAL_SEQ_TIME = 3.0 # 1.5 start + 0.5 * 3
        
        if time_since_seq >= TOTAL_SEQ_TIME:
            status = RaceStatus.RACING
            race_ts = now

    # --- CALCULATE LIGHTS (Visuals) ---
    lights = calculate_lights(status, new_left, new_right, now, seq_ts)

    return RaceState(
        status,
        stage_ts,
        seq_ts,
        race_ts,
        new_left,
        new_right,
        lights
    )

def calculate_lights(status, left, right, now, seq_ts):
    # Defaults
    l_pre, l_stage = False, False
    r_pre, r_stage = False, False
    a1, a2, a3 = False, False, False
    g_l, g_r = False, False
    red_l, red_r = False, False
    
    # 1. Staging Bulbs
    if status in [RaceStatus.WAITING, RaceStatus.STAGING, RaceStatus.SEQUENCE]:
        # They stay on during sequence? Yes usually.
        # Logic matches lane status (feedback)
        if left.status == LaneStatus.PRE_STAGE: l_pre = True
        if left.status == LaneStatus.STAGED: l_pre = True; l_stage = True
        if left.status == LaneStatus.DEEP_STAGE_WARNING: l_stage = True # Pre OFF

        if right.status == LaneStatus.PRE_STAGE: r_pre = True
        if right.status == LaneStatus.STAGED: r_pre = True; r_stage = True
        if right.status == LaneStatus.DEEP_STAGE_WARNING: r_stage = True
        
    # 2. Tree Sequence
    if status == RaceStatus.SEQUENCE and seq_ts:
        dt = now - seq_ts
        # Sportsman: 
        # 0.0 - 1.5: All Off
        # 1.5 - 2.0: Amber 1
        # 2.0 - 2.5: Amber 2
        # 2.5 - 3.0: Amber 3
        if 1.5 <= dt < 2.0: a1 = True
        if 2.0 <= dt < 2.5: a2 = True
        if 2.5 <= dt < 3.0: a3 = True
        
    # 3. Green / Red
    if status == RaceStatus.RACING:
        # Green is ON unless Fault
        if left.status != LaneStatus.FAULT: g_l = True
        if right.status != LaneStatus.FAULT: g_r = True
        
    # Fault overrides
    if left.status == LaneStatus.FAULT: red_l = True
    if right.status == LaneStatus.FAULT: red_r = True

    return RaceLights(l_pre, l_stage, r_pre, r_stage, a1, a2, a3, g_l, g_r, red_l, red_r, False)
