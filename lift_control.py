from magicbot import StateMachine, state, timed_state, default_state, tunable
from magicbot.state_machine import default_state

from lift import Lift
from arm import Arm
from claw import Claw

class LiftControl(StateMachine):
    lift : Lift
    arm : Arm
    claw : Claw

    def __init__(self):
        self._requested_state = None

    def request_state(self, state):
        self._requested_state = state

    @state
    def stow_pos(self):
        self.lift.lift(0)
        self.arm.tilt(0)
        self.arm.wrist(0)
        self.claw.wrist(0)

        if self._requested_state == 'stop':
            self.next_state('stop')

    @state
    def floor_pos(self):
        self.lift.lift(0)
        self.arm.tilt(0)
        self.arm.wrist(0)

        if self._requested_state == 'stop':
            self.next_state('stop')
    
    @state
    def processor_pos(self):
        self.lift.lift(10)
        self.arm.tilt(0)
        self.arm.wrist(0)

        if self._requested_state == 'stop':
            self.next_state('stop')
    
    @state
    def gather_pos(self):
        self.lift.lift(20)
        self.arm.tilt(10)
        self.arm.wrist(0)

        if self._requested_state == 'stop':
            self.next_state('stop')

    @state
    def trough_pos(self):
        self.lift.lift(0)
        self.arm.tilt(0)
        self.arm.wrist(60)

        if self._requested_state == 'stop':
            self.next_state('stop')
            
    @state
    def low_pos(self):
        self.lift.lift(20)
        self.arm.tilt(0)
        self.arm.wrist(60)

        if self._requested_state == 'stop':
            self.next_state('stop')
            
    @state
    def med_pos(self):
        self.lift.lift(35)
        self.arm.tilt(0)
        self.arm.wrist(60)

        if self._requested_state == 'stop':
            self.next_state('stop')
    
    @state
    def high_pos(self):
        self.lift.lift(50)
        self.arm.tilt(15)
        self.arm.wrist(75)

        if self._requested_state == 'stop':
            self.next_state('stop')

    @state
    def gather_coral(self):
        self.arm.gather()

        if self._requested_state == 'stop':
            self.next_state('stop')
            
    @state
    def gather_algae(self):
        self.claw.wrist(90)
        self.claw.gather()

        if self._requested_state == 'stop':
            self.next_state('stop')
            
    @state
    def store_algae(self):
        self.claw.wrist(0)

        if self._requested_state == 'stop':
            self.next_state('stop')
    
    @state
    def eject_coral(self):
        self.arm.eject()

        if self._requested_state == 'stop':
            self.next_state('stop')
            
    @state
    def eject_algae(self):
        self.claw.eject()

        if self._requested_state == 'stop':
            self.next_state('stop')

    @state
    def stop(self):
        self.arm.stop()
        self.claw.stop()

        self.next_state('idle')

    @state(first=True)
    def idle(self):
        if self._requested_state is not None:
            self.next_state(self._requested_state)
            self._requested_state = None