from wpimath import units
from magicbot import tunable
import rev


class Lift:
    s_lift_left : rev.SparkMax
    s_lift_right : rev.SparkMax

    lift_state = tunable(0.0)

    lift_cmd = tunable(0.0)
    
    max_lift = tunable(50.0)

    def setup(self):
        self.s_lift_left.setInverted(True)
        self.s_lift_right.setInverted(False)
    
        self._inch2rev = 9 / 4.5

    def execute(self):
        self.lift_state = ((self.s_lift_left.getEncoder().getPosition() / self._inch2rev) + (self.s_lift_right.getEncoder().getPosition() / self._inch2rev)) / 2
        
        self.s_lift_left.getClosedLoopController().setReference(self.lift_cmd * self._inch2rev, rev.SparkLowLevel.ControlType.kPosition)
        self.s_lift_right.getClosedLoopController().setReference(self.lift_cmd * self._inch2rev, rev.SparkLowLevel.ControlType.kPosition)

    def lift(self, height : units.inches):
        if height <= self.max_lift:
            self.lift_cmd = height

    def lifted(self):
        max_err = units.inches(1) * self._inch2rev
        return abs(self.s_lift_left.getEncoder().getPosition() - self.lift_cmd * self._inch2rev) < max_err and abs(self.s_lift_right.getEncoder().getPosition() - self.lift_cmd * self._inch2rev) < max_err
