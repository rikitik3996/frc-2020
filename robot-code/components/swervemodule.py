import math

import wpilib
import ctre

# from networktables import NetworkTables
from wpimath.controller import PIDController
from dataclasses import dataclass
import ntcore


# Create the structure of the config: SmartDashboard prefix, Encoder's zero point, Drive motor inverted, Allow reverse
@dataclass
class SwerveModuleConfig:
    sd_prefix: str
    zero: int
    inverted: bool
    allow_reverse: bool


class SwerveModule:
    # Get the motors, encoder and config from injection
    driveMotor: ctre.WPI_TalonFX
    rotateMotor: ctre.WPI_TalonFX
    encoder: ctre.WPI_CANCoder
    cfg: SwerveModuleConfig

    def setup(self):
        """
        Called after injection
        """
        # Config
        # self.sd_prefix = self.cfg.sd_prefix or 'Module'
        self.encoder_zero = self.cfg.zero or 0
        self.inverted = self.cfg.inverted or False
        self.allow_reverse = self.cfg.allow_reverse or True

        # SmartDashboard
        # # self.sd = NetworkTables.getTable('SmartDashboard')
        # self.debugging = # self.sd.getEntry('drive/drive/debugging')

        # Motor
        self.driveMotor.setInverted(self.inverted)

        self._requested_degree = 0
        self._requested_speed = 0

        # PID Controller
        # kP = 1.5, kI = 0.0, kD = 0.0
        #  16.27 - 16.09 = 0.18
        Ku = 0.025
        Tu = 0.18
        Kp = 0.8 * Ku / 4
        Ki = 0.4 * Ku / Tu
        Kd = 0.1 * Ku * Tu
        self._pid_controller = PIDController(Kp, 0, Kd)
        self._pid_controller.enableContinuousInput(0.0, 360) # Will set the 0 and 5 as the same point
        self._pid_controller.setTolerance(0, 0) # Tolerance where the PID will be accpeted aligned

        self.configTab = ntcore.NetworkTableInstance.getDefault().getTable("Config")

    def flush(self):
        """
        Flush the modules requested speed and angle.
        Resets the PID controller.
        """
        self._requested_degree = self.encoder_zero
        self._requested_speed = 0
        self._pid_controller.reset()


    def get_encoder_abs_position(self):
        return (self.encoder.getAbsolutePosition() + self.encoder_zero) % 360

    def move(self, speed, deg):
        """
        Set the requested speed and rotation of passed.

        :param speed: requested speed of wheel from -1 to 1
        :param deg: requested angle of wheel from 0 to 359 (Will wrap if over or under)
        """
        deg %= 360 # Prevent values past 360

        if self.allow_reverse:
            """
            If the difference between the requested degree and the current degree is
            more than 90 degrees, don't turn the wheel 180 degrees. Instead reverse the speed.
            """
            if abs(deg - self.get_encoder_abs_position()) > 90:
                speed *= -1
                deg += 180
                deg %= 360
        # offset_nt = # self.sd.getNumber('test/value', 0)
        # print(offset_nt)
        self._requested_speed = speed
        self._requested_degree = deg

    def debug(self):
        """
        Print debugging information about the module to the log.
        """
        pass
        #print(self.sd_prefix, '; requested_speed: ', self._requested_speed, ' requested_voltage: ', self._requested_degree)

    def execute(self):
        """
        Use the PID controller to get closer to the requested position.
        Set the speed requested of the drive motor.

        Called every robot iteration/loop.
        """
        self._pid_controller.setP(self.configTab.getNumber("Pid Kp", 0))
        self._pid_controller.setI(self.configTab.getNumber("Pid Ki", 0))
        self._pid_controller.setD(self.configTab.getNumber("Pid Kd", 0))
        error = self._pid_controller.calculate(self.get_encoder_abs_position(), self._requested_degree)
        # Set the output 0 as the default value
        output = 0
        # If the error is not tolerable, set the output to the error.
        # Else, the output will stay at zero.
        if not self._pid_controller.atSetpoint():
            # Use max-min to clamped the output between -1 and 1.
            output = max(min(error, 1), -1)

        # Put the output to the dashboard
        # self.sd.putNumber('drive/%s/output' % # self.sd_prefix, output)
        # Set the output as the rotateMotor's voltage
        self.rotateMotor.set(output)

        # Set the requested speed as the driveMotor's voltage
        self.driveMotor.set(self._requested_speed) 

        
        # self.driveMotor.set(0)

        self.update_smartdash()

    def update_smartdash(self):
        """
        Output a bunch on internal variables for debugging purposes.
        """
        # self.sd.putNumber('drive/%s/degrees' % # self.sd_prefix, self.get_encoder_abs_position())

        #if self.debugging.getBoolean(False):
        #   pass
            # self.sd.putNumber('drive/%s/requested_degree' % # self.sd_prefix, self._requested_degree)
            # self.sd.putNumber('drive/%s/requested_speed' % # self.sd_prefix, self._requested_speed)
            # self.sd.putNumber('drive/%s/encoder_zero' % # self.sd_prefix, self.encoder_zero)

            # self.sd.putNumber('drive/%s/PID Setpoint' % # self.sd_prefix, self._pid_controller.getSetpoint())
            # self.sd.putNumber('drive/%s/PID Error' % # self.sd_prefix, self._pid_controller.getPositionError())
            # self.sd.putBoolean('drive/%s/PID isAligned' % # self.sd_prefix, self._pid_controller.atSetpoint())

            # self.sd.putBoolean('drive/%s/allow_reverse' % # self.sd_prefix, self.allow_reverse)
