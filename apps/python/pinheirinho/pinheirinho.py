import ac
import acsys
import sys
import os
import time

# AC Magic to add current directory to path for imports
try:
    app_window = 0
    app_name = "Pinheirinho"
    
    # Add local 'src' to path
    # AC executes from root of AC folder usually
    # We need to find where this file is
    # In AC, __file__ might not be reliable, but let's try standard boilerplate
    
    # We assume standard structure
    # apps/python/pinheirinho/src
    
    # For now, let's try to import directly assuming AC adds the app folder to path
    from src.core.state import create_initial_state, RaceInputs
    from src.core.reducers import race_reducer
    # We will implement SensorSystem and Lighting transitionally
    from src.infrastructure.sensor import SensorSystem
    from src.infrastructure.lighting import LightingSystem
    from src.infrastructure.auditor import AuditorSystem
except Exception as e:
    ac.log("Pinheirinho Init Error: {}".format(e))
    ac.console("Pinheirinho Error: Check log")

# Global Mutable App State (The Shell)
class AppState:
    race_state = None
    sensor_system = None
    lighting_system = None
    auditor_system = None
    lbl_status = 0 # UI Label ID
    last_update_time = 0.0

APP = AppState()

def acMain(ac_version):
    global app_window, APP
    
    try:
        app_window = ac.newApp(app_name)
        ac.setSize(app_window, 200, 200)
        
        APP.lbl_status = ac.addLabel(app_window, "INIT")
        ac.setPosition(APP.lbl_status, 10, 30)
        
        ac.console("Pinheirinho: Initializing...")
        
        # Initialize Functional Core
        APP.race_state = create_initial_state()
        
        # Initialize Infrastructure
        # Resolve path to config
        base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_path, 'config', 'tracks.json')
        APP.sensor_system = SensorSystem(config_path)
        APP.lighting_system = LightingSystem()
        APP.auditor_system = AuditorSystem()
        # Fix log dir
        APP.auditor_system.log_dir = os.path.join(base_path, 'logs')
        APP.auditor_system._ensure_log_dir()
        
        ac.console("Pinheirinho: Ready. Waiting for cars.")
        
        return app_name
    except Exception as e:
        ac.log("Pinheirinho acMain Error: {}".format(e))
        return "Pinheirinho Error"

def acUpdate(delta_t):
    global APP
    
    try:
        # 1. Gather Inputs (Side Effects / Dirty)
        # We assume Car 0 is Left Lane (Driver) for testing
        car_pos = ac.getCarState(0, acsys.CS.WorldPosition)
        speed = ac.getCarState(0, acsys.CS.SpeedKMH)
        
        # Determine active track/lane logic (Mocking Right Lane as simple clone or static for now)
        l_pre, l_stg = APP.sensor_system.get_lane_data(0, "left_lane", car_pos)
        
        # TODO: Get Right Lane (Multiplayer or AI)
        # For solo testing, we might map Right Lane to Key Press? or just disable
        r_pre, r_stg = False, False # Stub
        
        now = time.time() # This is System Time. Better to use Game Time if possible? 
        # ac.getCarState(0, acsys.CS.PerformanceMeter) ?? 
        # using time.time() is fine because deltas matter more.
        
        inputs = RaceInputs(
            time=now,
            left_in_pre=l_pre, left_in_stage=l_stg, left_speed_kmh=speed, left_dist_traveled=0.0,
            right_in_pre=r_pre, right_in_stage=r_stg, right_speed_kmh=0.0, right_dist_traveled=0.0
        )
        
        # 2. Update Core Logic (Pure)
        # (old_state, inputs) -> new_state
        new_state = race_reducer(APP.race_state, inputs)
        
        # 3. Render Outputs (Side Effects)
        if new_state.lights != APP.race_state.lights:
            APP.lighting_system.update(new_state.lights)
            
        # Audit Logs
        APP.auditor_system.on_state_change(APP.race_state, new_state)

        # UI Validation
        ac.setText(APP.lbl_status, "State: {}\nL: PRE={} STG={}".format(
            new_state.status, l_pre, l_stg))
            
        APP.race_state = new_state
        
    except Exception as e:
        pass # ac.log("Pinheirinho Update Error: {}".format(e))
