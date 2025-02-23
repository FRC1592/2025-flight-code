from wpimath import units
import phoenix6
from magicbot import tunable
import rev
import math


class Arm:
    f_arm_tilt : phoenix6.hardware.TalonFX
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
        self._deg2rev =  60 / units.degrees(360)
        tilt_cfg = phoenix6.configs.Slot0Configs()
        tilt_cfg.k_p = 0.1
        tilt_cfg.k_i = 0.0
        tilt_cfg.k_d = 0.0
        
        #KYLE WHAT IS THE GEAR RATIO
        self._rad2rev = 60 / units.radians(2 * math.pi)

    def execute(self):
        self.tilt_state = self.f_arm_tilt.get_position() / self._deg2rev
        self.f_arm_tilt.set_position(self.tilt_cmd * self._deg2rev)
        
        self.wrist_state = self.s_arm_wrist.getEncoder().getPosition() / self._rad2rev
        self.s_arm_wrist.getClosedLoopController().setReference(self.wrist_cmd * self._rad2rev, rev.SparkLowLevel.ControlType.kPosition)
        
        self.s_arm_gather.set(self.gather_cmd)

    def tilt(self, angle : units.degrees):
        if angle <= self.tilt_limit:
            self.tilt_cmd = angle
        
    def wrist(self, angle : units.degrees):
        if angle <= self.wrist_limit:
            self.wrist_cmd = math.radians(angle)

    def gather(self):
        self.gather_cmd = 0.3

    def eject(self):
        self.gather_cmd = -0.3

    def stop(self):
        self.gather_cmd = 0.0

    def tilted(self):
        max_err = units.degrees(5) * self._deg2rev
        return abs(self.f_arm_tilt.get_position() - self.tilt_cmd * self._deg2rev) < max_err
    
    def wristed(self):
        max_err = units.radians(0.087) * self._rad2rev
        return abs(self.s_arm_wrist.getEncoder().getPosition() - self.wrist_cmd * self._rad2rev) < max_err
