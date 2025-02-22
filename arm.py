from wpimath import units
import phoenix6
from magicbot import tunable
import rev


class Arm:
    f_arm_tilt : phoenix6.hardware.TalonFX
    s_arm_wrist : rev.SparkMax
    s_arm_gather : rev.SparkMax

    arm_state = tunable(0.0)

    tilt_cmd = tunable(0.0)
    wrist_cmd = tunable(0.0)
    gather_cmd = tunable(0.0)

    def setup(self):
        # self._deg2cnt = 2048 * 112 / units.degrees(360)
        tilt_cfg = phoenix6.configs.Slot0Configs()
        tilt_cfg.k_p = 0.1
        tilt_cfg.k_i = 0.0
        tilt_cfg.k_d = 0.0
        
        config = rev.SparkMaxConfig()
        self.s_arm_wrist.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)
        self.s_arm_gather.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)

    def execute(self):
        # self.arm_state = self.f_arm_tilt.getSelectedSensorPosition() / self._deg2cnt
        # self.f_gather_tilt.set(phoenix6.ControlMode.Position, self.tilt_cmd * self._deg2cnt)
        self.s_arm_gather.set(self.gather_cmd)

    def tilt(self, angle : units.degrees):
        self.tilt_cmd = angle
        
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
