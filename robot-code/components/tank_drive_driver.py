import ctre
from magicbot import magiccomponent
import wpilib
from wpilib.drive import DifferentialDrive
from common.limelight import Limelight
import ntcore

from navx import AHRS #Navx

class TankDriveDriver:
    # These modules will be injected from ../robot.py
    leftMotor1: ctre.WPI_TalonFX
    leftMotor2: ctre.WPI_TalonFX
    rightMotor1: ctre.WPI_TalonFX
    rightMotor2: ctre.WPI_TalonFX
    navx: AHRS
    pixie_offset: wpilib.AnalogInput
    pixie_valid: wpilib.DigitalInput
    limelight: Limelight

    def setup(self):
        """
        Called after injection.
        """
        self.left = wpilib.MotorControllerGroup(self.leftMotor1, self.leftMotor2)
        self.right = wpilib.MotorControllerGroup(
            self.rightMotor1, self.rightMotor2
        )
        self.robot_drive = DifferentialDrive(self.left, self.right)
        self.robot_drive.setExpiration(0.1)

        self.move_request = [0, 0]
        self.debug = True

        self.table = ntcore.NetworkTableInstance.getDefault().getTable("SmartDashboard")

    def move(self, left_stick, right_stick):
        """ """
        self.move_request = [left_stick, right_stick]

    def pixie_drive(self):
        print(self.navx)
        print(self.pixie_offset)
        print(self.pixie_valid)

        if not self.pixie_valid.get():
            self.move_request = [0.2, 0.2]
        else:
            offset = ((self.pixie_offset.getValue() / 1024) - 0.5) * 2  # offset from -1 to 1
            left_side = min(1, 1 - offset)
            right_side = min(1, 1 + offset)
            self.move_request = [left_side, right_side]

    def limelight_drive(self):
        print(self.limelight)
        # if not self.limelight.valid_target():
        #     self.move_request = [0, 0]
        # else:
        #     offset = ((self.limelight.get_target_x_offset() / 300) - 0.5) * 2  # offset from -1 to 1
        #     left_side = min(1, 1 - offset)
        #     right_side = min(1, 1 + offset)
        #     self.move_request = [left_side, right_side]


    def execute(self):
        """ """
        self.robot_drive.tankDrive(self.move_request[0], self.move_request[1])
        self.move_request = [0, 0]

        if self.debug:
            self.table.putNumber("tank_drive/left", self.move_request[0])
            self.table.putNumber("tank_drive/righ", self.move_request[1])