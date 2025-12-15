import ac
import acsys
import json
import os
from src.utils.math_utils import is_point_in_cylinder, vec_dist_sq

class SensorSystem:
    def __init__(self, track_json_path):
        self.track_data = self._load_config(track_json_path)
        # Default to kunos drag strip for now, or detect track name from AC
        self.current_track = self.track_data.get("drag_strip_kunos")
        self.sensor_radius = 0.5 # 50cm tolerance?
        
    def _load_config(self, path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            ac.log("SensorSystem: Could not load tracks.json: {}".format(e))
            return {}

    def get_lane_data(self, car_id, lane_name, ac_pos):
        """
        car_id: AC Car ID (0 for player usually)
        lane_name: 'left_lane' or 'right_lane'
        ac_pos: tuple (x, y, z) from ac.getCarState
        Returns: (in_pre, in_stage)
        """
        if not self.current_track:
            return False, False

        lane = self.current_track.get(lane_name)
        if not lane:
            return False, False
            
        # Coordinates from JSON
        # Format assumed: {"center": [x, y, z], "width": w}
        # Real tracks use lines (Start -> End). Our JSON current has "center".
        # Let's assume the sensor is a line perpendicular to track?
        # Or just a point with radius for simplicity in Phase 1?
        # Re-reading Plan: "Laser scanned beams".
        # Let's treat valid zone as a sphere/cylinder around the center point for now.
        
        pre_center = lane['pre_stage']['center']
        stg_center = lane['stage']['center']
        
        # Simple distance check
        # AC Coordinates: X is Left/Right, Y is Up, Z is Forward
        
        # Check Pre-Stage
        # Distance squared check
        dist_pre = vec_dist_sq(ac_pos, pre_center)
        in_pre = dist_pre < (self.sensor_radius * self.sensor_radius)
        
        # Check Stage
        dist_src = vec_dist_sq(ac_pos, stg_center)
        in_stage = dist_src < (self.sensor_radius * self.sensor_radius)
        
        return in_pre, in_stage

