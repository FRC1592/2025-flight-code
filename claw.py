# from wpimath import units
# import wpilib
# import phoenix5
# from magicbot import tunable


# class Claw:
#     f_gather_tilt : phoenix5.WPI_TalonFX
#     t_gather : phoenix5.WPI_TalonSRX
#     d_gather_break : wpilib.DigitalInput

#     tilt_state = tunable(0.0)

#     tilt_cmd = tunable(0.0)
#     gather_cmd = tunable(0.0)

#     def setup(self):
#         self._deg2cnt = 2048 * 112 / units.degrees(360)
#         tilt_cfg = phoenix5.TalonFXConfiguration()
#         tilt_cfg.slot0.kP = 0.1
#         tilt_cfg.slot0.kI = 0.0
#         tilt_cfg.slot0.kD = 0.0
#         # tilt_cfg.motionCruiseVelocity = 10
#         self.f_gather_tilt.configFactoryDefault()
#         self.f_gather_tilt.configAllSettings(tilt_cfg)
#         self.f_gather_tilt.setInverted(True)

#     def execute(self):
#         self.tilt_state = self.f_gather_tilt.getSelectedSensorPosition() / self._deg2cnt
#         self.f_gather_tilt.set(phoenix5.ControlMode.Position, self.tilt_cmd * self._deg2cnt)
#         self.t_gather.set(phoenix5.ControlMode.PercentOutput, self.gather_cmd)

#     def tilt(self, angle : units.degrees):
#         self.tilt_cmd = angle

#     def gather(self):
#         self.gather_cmd = 0.7

#     def eject(self):
#         self.gather_cmd = -1.0

#     def stop(self):
#         self.gather_cmd = 0.0

#     def tilted(self):
#         max_err = units.degrees(5) * self._deg2cnt
#         return abs(self.f_gather_tilt.getSelectedSensorPosition() - self.tilt_cmd * self._deg2cnt) < max_err

#     def gathered(self):
#         return not self.d_gather_break.get()
