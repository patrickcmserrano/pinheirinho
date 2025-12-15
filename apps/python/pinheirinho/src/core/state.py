from collections import namedtuple

# ==========================================
# CONSTANTS (ENUM-LIKE)
# ==========================================

class RaceStatus:
    WAITING = 0         # Waiting for cars to approach
    STAGING = 1         # One or both cars are aligning (7s timer might be active)
    SEQUENCE = 2        # Tree is coming down (Ambers)
    RACING = 3          # Green light, race in progress
    FINISHED = 4        # Race over, showing results

class LaneStatus:
    IDLE = 0            # Not in beams
    PRE_STAGE = 1       # Pre-stage beam active
    STAGED = 2          # Both beams active (Ready)
    DEEP_STAGE_WARNING = 3 # Passed pre-stage (must reverse)
    RACING = 4          # Moving after green
    FINISHED = 5        # Crossed finish line
    FAULT = 6           # Red light (Jump start or Timeout)

# ==========================================
# DATA STRUCTURES (IMMUTABLE STATE)
# ==========================================

# Visual State of the Christmas Tree (Output)
RaceLights = namedtuple('RaceLights', [
    'pre_stage_left', 'stage_left',
    'pre_stage_right', 'stage_right',
    'amber_1', 'amber_2', 'amber_3',
    'green_left', 'green_right',
    'red_left', 'red_right',
    'blue_light' # Optional: "Autostart" or center light
])

# Initial state helper for lights
def create_initial_lights():
    return RaceLights(
        False, False, False, False, # Stage lights
        False, False, False,        # Ambers (Shared or split? Assuming shared for now based on standard tree)
        False, False,               # Greens
        False, False,               # Reds
        False                       # Blue
    )

# Snapshot of a single lane's logic state
LaneState = namedtuple('LaneState', [
    'status',           # LaneStatus value
    'reaction_time',    # Float (seconds)
    'elapsed_time',     # Float (seconds) - E.T.
    'final_speed',      # Float (km/h)
    'fault_reason'      # String
])

def create_initial_lane():
    return LaneState(LaneStatus.IDLE, 0.0, 0.0, 0.0, "")

# The Global State Container
RaceState = namedtuple('RaceState', [
    'status',           # RaceStatus value
    'stage_timer_start',# Timestamp when 7s timer started (None or float)
    'sequence_start',   # Timestamp when tree sequence began (None or float)
    'race_start_time',  # Timestamp when Green Light happened (T=0 for race)
    'left_lane',        # LaneState
    'right_lane',       # LaneState
    'lights'            # RaceLights
])

def create_initial_state():
    return RaceState(
        RaceStatus.WAITING,
        None, # stage_timer_start
        None, # sequence_start
        None, # race_start_time
        create_initial_lane(), # left_lane
        create_initial_lane(), # right_lane
        create_initial_lights() # lights
    )

# Inputs from the Sensor System (Pure Data)
RaceInputs = namedtuple('RaceInputs', [
    'time',                 # Current Global Time (seconds)
    'left_in_pre',          # Bool
    'left_in_stage',        # Bool
    'left_speed_kmh',       # Float
    'left_dist_traveled',   # Float (meters from start)
    'right_in_pre',         # Bool
    'right_in_stage',       # Bool
    'right_speed_kmh',      # Float
    'right_dist_traveled'   # Float
])
