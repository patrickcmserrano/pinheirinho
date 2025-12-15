import json
import hashlib
import time
import os
from src.core.state import RaceState, RaceStatus

class AuditorSystem:
    def __init__(self):
        self.buffer = []
        self.is_recording = False
        self.session_id = None
        self.log_dir = "logs"
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        # We need to find absolute path usually relative to app
        # For now, let's try local relative
        try:
             if not os.path.exists(self.log_dir):
                 os.makedirs(self.log_dir)
        except:
            pass

    def on_state_change(self, old_state: RaceState, new_state: RaceState):
        """
        Called every frame. We filter relevant events to avoid massive logs.
        """
        status_changed = old_state.status != new_state.status
        
        # Start Recording
        if status_changed and new_state.status == RaceStatus.STAGING:
            self._start_recording()
        
        # Stop Recording
        if status_changed and new_state.status == RaceStatus.FINISHED:
             self._stop_recording(new_state)

        if not self.is_recording:
            return

        # Snapshot interesting data
        # We don't log every frame unless debugging.
        # Log: Events + Interval snapshots (e.g. every 0.1s)
        # For "Black Box", we might want high frequency but compressed?
        # Let's log State Changes and Faults immediately.
        
        log_entry = None
        
        if status_changed:
            log_entry = {"t": time.time(), "event": "STATUS_CHANGE", "val": new_state.status}
            
        elif new_state.left_lane.status != old_state.left_lane.status:
            log_entry = {"t": time.time(), "event": "L_LANE_STATUS", "val": new_state.left_lane.status}
            
        elif new_state.right_lane.status != old_state.right_lane.status:
            log_entry = {"t": time.time(), "event": "R_LANE_STATUS", "val": new_state.right_lane.status}

        if log_entry:
            self.buffer.append(log_entry)

    def _start_recording(self):
        self.buffer = []
        self.is_recording = True
        self.session_id = str(int(time.time()))
        self.buffer.append({"t": time.time(), "event": "SESSION_START", "id": self.session_id})

    def _stop_recording(self, final_state):
        if not self.is_recording: return
        self.is_recording = False
        
        # Add winners/results
        self.buffer.append({
            "t": time.time(), 
            "event": "SESSION_END", 
            "left_result": final_state.left_lane.status,
            "right_result": final_state.right_lane.status
        })
        
        self._flush_to_disk()

    def _flush_to_disk(self):
        try:
            filename = "{}/race_{}.json".format(self.log_dir, self.session_id)
            data_str = json.dumps(self.buffer, indent=4)
            
            # Write JSON
            with open(filename, 'w') as f:
                f.write(data_str)
                
            # Create Hash
            sha = hashlib.sha256(data_str.encode('utf-8')).hexdigest()
            with open(filename + ".sha256", 'w') as f:
                f.write(sha)
                
            # ac.log("Auditor: Race saved to {}".format(filename))
        except Exception as e:
            pass
