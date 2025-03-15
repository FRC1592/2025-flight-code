from magicbot import state, timed_state

from magicbot import AutonomousStateMachine

from chassis_control import ChassisControl
from lift_control import LiftControl
from climber_control import ClimberControl


class NoMove(AutonomousStateMachine):
    MODE_NAME = 'NoMove'

    chassis_control : ChassisControl
    lift_control : LiftControl
    climber_control : ClimberControl

    def initialize(self):
        pass

    @state(first=True)
    def stupid(self):
        self.next_state('auto_done')

    @state
    def auto_done(self):
        self.lift_control.request_state(None)

    def on_iteration(self, tm):
        self.chassis_control.engage()
        self.lift_control.engage()
        self.climber_control.engage()


        super().on_iteration(tm)
