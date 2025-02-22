from wpimath import units
import phoenix6
from magicbot import tunable
import rev


class Claw:
    f_claw_wrist : phoenix6.hardware.TalonFX
    s_claw_gather : rev.SparkMax

    claw_state = tunable(0.0)

    wrist_cmd = tunable(0.0)
    gather_cmd = tunable(0.0)

    def setup(self):
        # self._deg2cnt = 2048 * 112 / units.degrees(360)
        wrist_cfg = phoenix6.configs.Slot0Configs()
        wrist_cfg.k_p = 0.1
        wrist_cfg.k_i = 0.0
        wrist_cfg.k_d = 0.0
        
        config = rev.SparkMaxConfig()
        self.s_claw_gather.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)

    def execute(self):
        # self.arm_state = self.f_gather_tilt.getSelectedSensorPosition() / self._deg2cnt
        # self.f_gather_tilt.set(phoenix5.ControlMode.Position, self.tilt_cmd * self._deg2cnt)
        self.s_claw_gather.set(self.gather_cmd)

    def wrist(self, angle : units.degrees):
        self.wrist_cmd = angle

    def gather(self):
        self.gather_cmd = 0.3

    def eject(self):
        self.gather_cmd = -0.3

    def stop(self):
        self.gather_cmd = 0.0

    # def tilted(self):
    #     max_err = units.degrees(5) * self._deg2cnt
    #     return abs(self.f_gather_tilt.getSelectedSensorPosition() - self.tilt_cmd * self._deg2cnt) < max_err
