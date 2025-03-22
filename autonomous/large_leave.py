from magicbot import state, timed_state

from magicbot import AutonomousStateMachine

from chassis_control import ChassisControl
from lift_control import LiftControl
from climber_control import ClimberControl
from vision import Vision
from april_constants import AprilConstants
from chassis import Chassis


class LargeLeave(AutonomousStateMachine):
    MODE_NAME = 'Large Leave'

    chassis_control : ChassisControl
    lift_control : LiftControl
    climber_control : ClimberControl
    chassis : Chassis

    def initialize(self):
        # self.chassis.zero_gyro()
        self.chassis_control.request_state('drive_gyro')

    @timed_state(duration=1.0, next_state='leave', first = True)
    def start(self):
        self.chassis_control.request_state('drive_gyro')
        self.chassis_control.drive_hold_heading(0, 0, 0)
        self.chassis.zero_pods()

    @timed_state(duration=6.0, next_state='stop')
    def leave(self):
        self.chassis_control.request_state('drive_gyro')
        self.chassis_control.drive_df(0, -20, 0, 6.0)

    @state
    def stop(self):
        self.chassis_control.update_joysticks(0, 0, 0)
        self.next_state('auto_done')

    @state
    def auto_done(self):
        self.chassis_control.update_joysticks(0, 0, 0)

    def on_iteration(self, tm):
        self.chassis_control.engage()
        self.lift_control.engage()
        self.climber_control.engage()

        super().on_iteration(tm)
