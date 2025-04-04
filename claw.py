from wpimath import units
from magicbot import tunable
import rev
import math


class Claw:
    s_claw_wrist : rev.SparkMax
    s_claw_gather : rev.SparkMax

    wrist_state = tunable(0.0)

    wrist_cmd = tunable(0.0)
    gather_cmd = tunable(0.0)
    
    wrist_limit = 220

    def setup(self):
        self.s_claw_wrist.IdleMode(rev.SparkMax.IdleMode.kBrake)
        config = rev.SparkMaxConfig()
        config.smartCurrentLimit(20)
        self.s_claw_gather.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)
        config.closedLoop.setFeedbackSensor(config.closedLoop.FeedbackSensor.kPrimaryEncoder)
        self.s_claw_wrist.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)
        self._rad2rev = 80 / units.radians(2 * math.pi)
        # pid_cfg = rev.ClosedLoopConfig()
        # pid_cfg.P(1.0, rev.ClosedLoopSlot.kSlot0)
        # self.s_claw_wrist.configure(rev.ClosedLoopConfig().P(1.0, rev.ClosedLoopSlot.kSlot0), rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)
        
        

    def execute(self):
        self.wrist_state = self.s_claw_wrist.getEncoder().getPosition() / self._rad2rev
        self.s_claw_wrist.getClosedLoopController().setReference(self.wrist_cmd * self._rad2rev, rev.SparkLowLevel.ControlType.kPosition)
        # self.s_claw_wrist.getClosedLoopController().setReference(self.wrist_cmd * self._rad2rev, rev.SparkLowLevel.ControlType.kPosition, rev.ClosedLoopSlot.kSlot0, self.plz_mommy, rev.SparkClosedLoopController.ArbFFUnits.kPercentOut)
        # self.s_claw_wrist.getClosedLoopController().setReference(self.wrist_cmd * self._rad2rev, rev.SparkLowLevel.ControlType.kPosition, arbFeedforward=0.1, arbFFUnits=rev.SparkClosedLoopController.ArbFFUnits.kPercentOut)
        
        
        self.s_claw_gather.set(self.gather_cmd)

    def wrist(self, angle : units.degrees):
        if angle <= self.wrist_limit:
            self.wrist_cmd = math.radians(angle)

    def gather(self):
        self.gather_cmd = 0.75

    def eject(self):
        self.gather_cmd = -1.0
        
    def hold(self):
        self.gather_cmd = 0.75

    def stop(self):
        self.gather_cmd = 0.0

    def wristed(self):
        max_err = units.radians(0.087) * self._rad2rev
        return abs(self.s_claw_wrist.getEncoder().getPosition() - self.wrist_cmd * self._rad2rev) < max_err
