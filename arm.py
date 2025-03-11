from wpimath import units
from magicbot import tunable
import rev
import math


class Arm:
    s_arm_tilt : rev.SparkMax
    s_arm_wrist : rev.SparkMax
    s_arm_gather : rev.SparkMax

    tilt_state = tunable(0.0)
    wrist_state = tunable(0.0)

    tilt_cmd = tunable(0.0)
    wrist_cmd = tunable(0.0)
    gather_cmd = tunable(0.0)
    
    tilt_limit = tunable(90.0)
    wrist_limit = tunable(90.0)

    def setup(self):
        self.s_arm_tilt.IdleMode(rev.SparkMax.IdleMode.kBrake)
        self.s_arm_wrist.IdleMode(rev.SparkMax.IdleMode.kBrake)
        config = rev.SparkMaxConfig()
        config.smartCurrentLimit(20)
        self.s_arm_gather.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)
        config.closedLoop.setFeedbackSensor(config.closedLoop.FeedbackSensor.kPrimaryEncoder)
        self.s_arm_tilt.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)
        self.s_arm_wrist.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)
        
        self.t_rad2rev = 120 / units.radians(2 * math.pi)
        self.w_rad2rev = 50 / units.radians(2 * math.pi)

    def execute(self):
        self.tilt_state = self.s_arm_tilt.getEncoder().getPosition() / self.t_rad2rev
        self.s_arm_tilt.getClosedLoopController().setReference(self.tilt_cmd * self.t_rad2rev, rev.SparkLowLevel.ControlType.kPosition)
        
        self.wrist_state = self.s_arm_wrist.getEncoder().getPosition() / self.w_rad2rev
        self.s_arm_wrist.getClosedLoopController().setReference(self.wrist_cmd * self.w_rad2rev, rev.SparkLowLevel.ControlType.kPosition)
        
        self.s_arm_gather.set(self.gather_cmd)

    def tilt(self, angle : units.degrees):
        if angle <= self.tilt_limit:
            self.tilt_cmd = math.radians(angle)
        
    def wrist(self, angle : units.degrees):
        if angle <= self.wrist_limit:
            self.wrist_cmd = math.radians(angle)

    def gather(self):
        self.gather_cmd = 1.0

    def eject(self):
        self.gather_cmd = -1.0

    def stop(self):
        self.gather_cmd = 0.0

    def tilted(self):
        max_err = units.radians(0.087) * self.t_rad2rev
        return abs(self.s_arm_tilt.getEncoder().getPosition() - self.tilt_cmd * self.t_rad2rev) < max_err
    
    def wristed(self):
        max_err = units.radians(0.087) * self.w_rad2rev
        return abs(self.s_arm_wrist.getEncoder().getPosition() - self.wrist_cmd * self.w_rad2rev) < max_err
