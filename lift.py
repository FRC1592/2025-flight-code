from wpimath import units
from magicbot import tunable
import rev


class Lift:
    s_lift_left : rev.SparkMax
    s_lift_right : rev.SparkMax

    lift_state = tunable(0.0)

    lift_cmd = tunable(0.0)
    
    max_lift = tunable(46.5)

    def setup(self):
        self.s_lift_left.IdleMode(rev.SparkMax.IdleMode.kBrake)
        self.s_lift_right.IdleMode(rev.SparkMax.IdleMode.kBrake)
        
        config = rev.SparkMaxConfig()
        config.closedLoop.setFeedbackSensor(config.closedLoop.FeedbackSensor.kPrimaryEncoder)
        config.smartCurrentLimit(40)
        self.s_lift_left.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)
        self.s_lift_right.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)
    
        self._inch2rev = 9 / units.inches(6.75)

    def execute(self):
        self.lift_state = ((self.s_lift_left.getEncoder().getPosition() / self._inch2rev) + (self.s_lift_right.getEncoder().getPosition() / self._inch2rev)) / 2
        
        self.s_lift_left.getClosedLoopController().setReference(self.lift_cmd * self._inch2rev, rev.SparkLowLevel.ControlType.kPosition)
        self.s_lift_right.getClosedLoopController().setReference(-self.lift_cmd * self._inch2rev, rev.SparkLowLevel.ControlType.kPosition)

    def lift(self, height : units.inches):
        if height <= self.max_lift:
            self.lift_cmd = height

    def lifted(self):
        max_err = units.inches(1) * self._inch2rev
        return abs(self.s_lift_left.getEncoder().getPosition() - self.lift_cmd * self._inch2rev) < max_err and abs(self.s_lift_right.getEncoder().getPosition() - self.lift_cmd * self._inch2rev) < max_err
