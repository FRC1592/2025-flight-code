from wpimath import units
from magicbot import tunable
import rev


class Lift:
    s_lift_left : rev.SparkMax
    s_lift_right : rev.SparkMax

    lift_state = tunable(0.0)

    lift_cmd = tunable(0.0)

    def setup(self):
        # self._deg2cnt = 2048 * 112 / units.degrees(360)
        
        config = rev.SparkMaxConfig()
        self.s_lift_left.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)
        self.s_lift_right.configure(config, rev.SparkMax.ResetMode.kNoResetSafeParameters, rev.SparkMax.PersistMode.kNoPersistParameters)

    def execute(self):
        pass
        # self.arm_state = self.f_gather_tilt.getSelectedSensorPosition() / self._deg2cnt
        # self.f_gather_tilt.set(phoenix5.ControlMode.Position, self.tilt_cmd * self._deg2cnt)

    def lift(self, angle : units.degrees):
        self.tilt_cmd = angle

    # def tilted(self):
    #     max_err = units.degrees(5) * self._deg2cnt
    #     return abs(self.f_gather_tilt.getSelectedSensorPosition() - self.tilt_cmd * self._deg2cnt) < max_err
