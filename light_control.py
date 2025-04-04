from magicbot import tunable, StateMachine, state, timed_state, default_state
from magicbot.state_machine import default_state

from light import Light


class LightControl(StateMachine):
    light : Light

    def __init__(self):
        self._requested_state = None

    def request_state(self, state):
        self._requested_state = state

    @state
    def turn_on(self):
        self.light.execute()

        self.next_state('idle')

    @state
    def turn_off(self):
        self.light.stop()

        self.next_state('idle')

    #@state
    #def change_color(self, color):
        #AVAILABLE COLORS: red, blue, orange, green, white
    #    self.led.setColor(color)

    #    self.next_state('idle')

    @state(first=True)
    def idle(self):
        if self._requested_state is not None:
            self.next_state(self._requested_state)
