from magicbot import state, timed_state

from magicbot import AutonomousStateMachine

from chassis_control import ChassisControl
from lift_control import LiftControl
from climber_control import ClimberControl


class Med1(AutonomousStateMachine):
    MODE_NAME = '1 Medium'

    chassis_control : ChassisControl
    lift_control : LiftControl
    climber_control : ClimberControl

    def initialize(self):
        pass

    @timed_state(duration=2.0, next_state='shoot', first=True)
    def dont_screw_up_other_autos(self):
        pass

    @state
    def shoot(self):
        self.shooter_control.request_state('aim')
        self.next_state('wait_shoot')

    @state
    def wait_shoot(self):
        if self.shooter_control.current_state == 'idle':
            self.next_state('stupid')

    @timed_state(duration=0.5, next_state='drive_forward')
    def stupid(self):
        pass

    @timed_state(duration=2, next_state='stop')
    def drive_forward(self):
        self.shooter_control.request_state(None)
        self.chassis_control.drive_hold_heading(0, 0, 0)

    @state
    def stop(self):
        self.chassis_control.update_joysticks(0, 0, 0)
        self.next_state('auto_done')

    @state
    def auto_done(self):
        pass

    def on_iteration(self, tm):
        self.chassis_control.engage()
        self.lift_control.engage()
        self.climber_control.engage()


        super().on_iteration(tm)
