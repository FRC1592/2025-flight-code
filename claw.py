from wpimath import units
import phoenix6
from magicbot import tunable
import rev


class Claw:
    f_claw_wrist : phoenix6.hardware.TalonFX
    s_claw_gather : rev.SparkMax

    wrist_state = tunable(0.0)

    wrist_cmd = tunable(0.0)
    gather_cmd = tunable(0.0)
    
    wrist_limit = 190

    def setup(self):
        # WHAT IS THE GEAR RATIO KYLE
        self._deg2rev = 60 / units.degrees(360)
        wrist_cfg = phoenix6.configs.Slot0Configs()
        wrist_cfg.k_p = 0.1
        wrist_cfg.k_i = 0.0
        wrist_cfg.k_d = 0.0

    def execute(self):
        self.wrist_state = self.f_claw_wrist.get_position() / self._deg2rev
        self.f_claw_wrist.set_position(self.wrist_cmd * self._deg2rev)
        
        self.s_claw_gather.set(self.gather_cmd)

    def wrist(self, angle : units.degrees):
        if angle <= self.wrist_limit:
            self.wrist_cmd = angle

    def gather(self):
        self.gather_cmd = 0.3

    def eject(self):
        self.gather_cmd = -0.3

    def stop(self):
        self.gather_cmd = 0.0

    def wristed(self):
        max_err = units.degrees(5) * self._deg2rev
        return abs(self.f_claw_wrist.get_position() - self.wrist_cmd * self._deg2rev) < max_err
