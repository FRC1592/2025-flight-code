from magicbot import StateMachine, state, timed_state, default_state, tunable
from magicbot.state_machine import default_state

from lift import Lift
from arm import Arm
from claw import Claw

class LiftControl(StateMachine):
    lift : Lift
    arm : Arm
    claw : Claw

    plz_daddy = tunable(31.0)

    def __init__(self):
        self._requested_state = None

    def request_state(self, state):
        self._requested_state = state
    
    def zeroed(self):
        return self.arm.tilted() and self.arm.wristed() and self.claw.wristed()

    @state 
    def stow_pos(self):
        self.lift.lift(0)
        self.arm.tilt(0)
        self.arm.wrist(0)
        self.claw.wrist(0)
        
        if self.zeroed():
            self.next_state('idle')

    @timed_state(duration=0.5, next_state='claw_prep')
    def floor_pos(self):
        self.lift.lift(20)
        self.arm.tilt(0)
        self.arm.wrist(0)
        self.claw.wrist(90)
    
    @timed_state(duration=0.8, next_state='lower_claw')
    def claw_prep(self):
        self.lift.lift(20)
        self.claw.wrist(180)
        
    @state
    def lower_claw(self):
        self.lift.lift(9.5)
        self.claw.wrist(180)
        
        if self.zeroed():
            self.next_state('idle')
            
    @timed_state(duration=0.8, next_state='flow_two')
    def scoop_algae(self):
        self.lift.lift(20)
        self.claw.wrist(185)
    
    # @timed_state(duration=0.5, next_state='flow_two')
    # def flow_one(self):
    #     self.lift.lift(20)
    #     self.claw.wrist(180)
        
    @timed_state(duration=0.8, next_state='flow_three')
    def flow_two(self):
        self.lift.lift(18)
        self.claw.wrist(65)
        
    @timed_state(duration=1.0, next_state='processor_pos')
    def flow_three(self):
        self.lift.lift(18)
        self.claw.wrist(100)
    
    @state
    def processor_pos(self):
        self.lift.lift(8)
        self.arm.tilt(0)
        self.arm.wrist(0)
        self.claw.wrist(121)
        
        if self.zeroed():
            self.next_state('idle')
            
    @state
    def flick_algae(self):
        self.lift.lift(20)
        self.claw.wrist(150)
        
        if self.zeroed():
            self.next_state('idle')
    
    @state
    def gather_pos(self):
        self.lift.lift(4)
        self.arm.tilt(17)
        self.arm.wrist(-45)
        self.claw.wrist(0)
        
        if self.zeroed():
            self.next_state('idle')

    @state
    def trough_pos(self):
        self.lift.lift(0)
        self.arm.tilt(55)
        self.arm.wrist(-55)
        
        if self.zeroed():
            self.next_state('idle')
            
    @state
    def low_pos(self):
        self.lift.lift(5)
        self.arm.tilt(0)
        self.arm.wrist(20)
        
        if self.zeroed():
            self.next_state('idle')
            
    @state
    def med_pos(self):
        self.lift.lift(18)
        self.arm.tilt(0)
        self.arm.wrist(22)
        self.claw.wrist(70)
        
        if self.zeroed():
            self.next_state('idle')
    
    @timed_state(duration=0.3, next_state='wunadeez')
    def high_eject(self):
        self.arm.eject()
    
    @timed_state(duration=0.1, next_state='wunadoz')
    def wunadeez(self):
        self.arm.wrist(29)
    
    @timed_state(duration=0.3, next_state='wunadat')
    def wunadoz(self):
        self.arm.wrist(22)
    
    @state
    def wunadat(self):
        self.arm.wrist(0)
        self.arm.stop()
        
        if self.zeroed():
            self.next_state('idle')

    @state
    def high_pos(self):
        self.lift.lift(46)
        self.arm.tilt(0)
        self.arm.wrist(34)
        self.claw.wrist(170)
        
        if self.zeroed():
            self.next_state('idle')

    @state
    def gather_coral(self):
        self.arm.gather()

        if self._requested_state == 'stop':
            self.next_state('stop')
            
    @state
    def gather_algae(self):
        # self.claw.wrist(90)
        self.claw.gather()

        if self._requested_state == 'stop':
            self.next_state('stop')
            
    @state
    def stow_claw(self):
        self.claw.wrist(0)
        
        if self.zeroed():
            self.next_state('idle')
    
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