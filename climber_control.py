from magicbot import tunable, StateMachine, state, timed_state, default_state
from magicbot.state_machine import default_state

from climber import Climber


class ClimberControl(StateMachine):
    climber : Climber

    def __init__(self):
        self._requested_state = None

    def request_state(self, state):
        self._requested_state = state

    @state()
    def extend(self):
        self.climber.set_climb(0.1)

        if self._requested_state == 'stop':
            self.next_state('stop')

    @state
    def stop(self):
        self.climber.stop()

        self.next_state('idle')

    @state(first=True)
    def idle(self):
        if self._requested_state is not None:
            self.next_state(self._requested_state)
