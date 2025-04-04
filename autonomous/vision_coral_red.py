# from magicbot import state, timed_state

# from magicbot import AutonomousStateMachine

# from arm import Arm
# from chassis_control import ChassisControl
# from lift_control import LiftControl
# from climber_control import ClimberControl
# from vision import Vision
# from april_constants import AprilConstants
# from chassis import Chassis


# class VisionCoralRed(AutonomousStateMachine):
#     MODE_NAME = 'Vision Coral Red'

#     arm : Arm
#     chassis_control : ChassisControl
#     lift_control : LiftControl
#     climber_control : ClimberControl
#     chassis : Chassis

#     def initialize(self):
#         self.chassis_control.request_state('drive_gyro')
        
#     @timed_state(duration=2.0, next_state='raise_lift', first=True)
#     def fix_arm(self):
#         self.chassis_control.righty = True
#         self.chassis_control.request_state('drive_gyro')
#         self.chassis_control.drive_hold_heading(0, 0, 180)
#         self.arm.hold()
#         # self.chassis.zero_pods()
#         self.lift_control.request_state('stow_pos')
        
#     @timed_state(duration=2.0, next_state='approach_tag')
#     def raise_lift(self):
#         self.chassis_control.request_state('drive_gyro')
#         self.chassis_control.drive_hold_heading(0, 0, 180)
#         self.lift_control.request_state('high_pos')

#     @timed_state(duration=4.0, next_state='score')
#     def approach_tag(self):
#         self.chassis_control.request_state('drive_gyro_tag')
#         self.chassis_control.drive_hold_heading(0, 0, 180)
#         self.arm.stop()
        
#     @timed_state(duration=0.7, next_state='back_up')
#     def score(self):
#         self.chassis_control.request_state('stop')
#         self.chassis_control.drive_hold_heading(0, 0, 180)
#         self.lift_control.request_state('high_eject')
        
#     @timed_state(duration=2.0, next_state='stop')
#     def back_up(self):
#         self.chassis_control.request_state('drive_gyro')
#         self.chassis_control.drive_df(0, -3, 180, 2.0)
#         self.lift_control.request_state('stow_pos')

#     @state
#     def stop(self):
#         self.chassis_control.update_joysticks(0, 0, 0)
#         self.next_state('auto_done')

#     @state
#     def auto_done(self):
#         self.chassis_control.update_joysticks(0, 0, 0)

#     def on_iteration(self, tm):
#         self.chassis_control.engage()
#         self.lift_control.engage()
#         self.climber_control.engage()

#         super().on_iteration(tm)
