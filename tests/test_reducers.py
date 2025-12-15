import sys
import os
import unittest

# Add the project root to sys.path so we can import 'src'
# Assuming this test file is in c:\dev\pinheirinho\tests\
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../apps/python/pinheirinho'))
sys.path.append(project_root)

from src.core.state import create_initial_state, RaceInputs, RaceStatus, LaneStatus
from src.core.reducers import race_reducer

class TestRaceLogic(unittest.TestCase):
    
    def create_empty_inputs(self, time=0.0):
        return RaceInputs(
            time=time,
            left_in_pre=False, left_in_stage=False, left_speed_kmh=0.0, left_dist_traveled=0.0,
            right_in_pre=False, right_in_stage=False, right_speed_kmh=0.0, right_dist_traveled=0.0
        )

    def test_staging_flow_normal(self):
        """Test normal staging: Both cars enter, sequence starts"""
        state = create_initial_state()
        
        # 1. Left enters Pre-Stage
        inputs = self.create_empty_inputs(time=1.0)
        inputs = inputs._replace(left_in_pre=True)
        state = race_reducer(state, inputs)
        self.assertEqual(state.status, RaceStatus.STAGING)
        self.assertEqual(state.left_lane.status, LaneStatus.PRE_STAGE)
        self.assertIsNone(state.stage_timer_start, "Timer should not start on Pre-Stage")

        # 2. Left Stages (Fully)
        inputs = inputs._replace(time=2.0, left_in_stage=True)
        state = race_reducer(state, inputs)
        self.assertEqual(state.left_lane.status, LaneStatus.STAGED)
        self.assertIsNotNone(state.stage_timer_start, "Timer MUST start when one car stages")
        
        # 3. Right enters and Stages immediately
        inputs = inputs._replace(time=3.0, right_in_pre=True, right_in_stage=True)
        state = race_reducer(state, inputs)
        
        # Should go to SEQUENCE immediately
        self.assertEqual(state.status, RaceStatus.SEQUENCE)
        self.assertIsNone(state.stage_timer_start, "Timer should clear on sequence start")
        self.assertEqual(state.sequence_start, 3.0)

    def test_staging_timeout_rule(self):
        """Test the 7-second rule violation"""
        state = create_initial_state()
        
        # 1. Left Stages at T=10
        inputs = self.create_empty_inputs(time=10.0)
        inputs = inputs._replace(left_in_pre=True, left_in_stage=True)
        state = race_reducer(state, inputs)
        
        self.assertEqual(state.stage_timer_start, 10.0)
        
        # 2. Advance time to T=17.0 (Exactly 7s) -> Should be fine
        inputs = inputs._replace(time=17.0)
        state = race_reducer(state, inputs)
        self.assertEqual(state.status, RaceStatus.STAGING)
        
        # 3. Advance to T=17.1 -> BOOM
        inputs = inputs._replace(time=17.1)
        state = race_reducer(state, inputs)
        
        # Right lane was IDLE, so it Faults
        self.assertEqual(state.right_lane.status, LaneStatus.FAULT)
        self.assertEqual(state.right_lane.fault_reason, "TIMEOUT 7s")
        
        # Left lane is innocent and stays Staged
        self.assertEqual(state.left_lane.status, LaneStatus.STAGED)
        
        # Race proceeds to Sequence (Bye run)
        self.assertEqual(state.status, RaceStatus.SEQUENCE)

    def test_deep_stage_warning(self):
        """Test Deep Stage behavior (must reverse)"""
        state = create_initial_state()
        inputs = self.create_empty_inputs(time=1.0)
        
        # 1. Left moves to Stage (Pre + Stage)
        inputs = inputs._replace(left_in_pre=True, left_in_stage=True)
        state = race_reducer(state, inputs)
        self.assertEqual(state.left_lane.status, LaneStatus.STAGED)
        
        # 2. Left moves too far (Pre OFF, Stage ON)
        inputs = inputs._replace(left_in_pre=False, left_in_stage=True)
        state = race_reducer(state, inputs)
        
        self.assertEqual(state.left_lane.status, LaneStatus.DEEP_STAGE_WARNING)
        
        # 3. Does this stop the race? No, but they are not 'Ready'.
        # If the other car stages, the logic says "Both Ready -> Sequence".
        # This car is NOT ready, so Sequence won't start. Valid.

    def test_jump_start(self):
        """Test moving before Green"""
        # Set up a sequence state
        state = create_initial_state()
        state = state._replace(
            status=RaceStatus.SEQUENCE, 
            sequence_start=10.0,
            left_lane=state.left_lane._replace(status=LaneStatus.STAGED),
            right_lane=state.right_lane._replace(status=LaneStatus.STAGED)
        )
        
        # Time is 11.0 (Amber 1). Green is at 13.0
        # Right car moves (speed > 5 kmh)
        inputs = self.create_empty_inputs(time=11.0)
        inputs = inputs._replace(
            right_speed_kmh=10.0,
            # If they move, they typically leave the sensors too, but speed trigger is faster
            right_in_pre=True, right_in_stage=True 
        )
        
        state = race_reducer(state, inputs)
        
        self.assertEqual(state.right_lane.status, LaneStatus.FAULT)
        self.assertEqual(state.right_lane.fault_reason, "JUMP START")
        
        # Lights should show Red for Right
        self.assertTrue(state.lights.red_right)

if __name__ == '__main__':
    unittest.main()
