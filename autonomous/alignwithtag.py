from magicbot import state, timed_state

from magicbot import AutonomousStateMachine

from chassis_control import ChassisControl
from lift_control import LiftControl
from climber_control import ClimberControl
from vision import Vision


class AlignWithTag(AutonomousStateMachine):
    MODE_NAME = 'Align with Tag'

    chassis_control : ChassisControl
    lift_control : LiftControl
    climber_control : ClimberControl
    vision : Vision

    def initialize(self):
        self.chassis_control.request_state('drive_gyro')

    @state(first=True)
    def start_turn(self):
        if self.vision.getOffsetPosition() > 0:
            self.chassis_control.update_joysticks(0, 0, 0.2)
        if self.vision.getOffsetPosition() < 0:
            self.chassis_control.update_joysticks(0, 0, -0.2)
        if self.vision.AlignedTag(7):
            self.next_state('stop')

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