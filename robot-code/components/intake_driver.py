import ctre
from magicbot import magiccomponent
import wpilib
import time

from navx import AHRS #Navx

class IntakeDriver:
    # These modules will be injected from ../robot.py
    sorterMotor: ctre.TalonSRX
    BeltMotor: ctre.VictorSPX
    intakeMotor: ctre.TalonSRX
    limitSwitchStart: wpilib.DigitalInput
    limitSwitchStop: wpilib.DigitalInput
    navx: AHRS

    def setup(self):
        """
        Called after injection.
        """
        self.intake_request_time = 0
        pass

    def shoot_request(self):
        self.shoot_request = 1

    def intake_request(self):
        self.intake_request_time = time.time()

    def execute(self):
        """ """
        if time.time() - self.intake_request_time < 2:
            self.intakeMotor.set(ctre.ControlMode.PercentOutput, 0.2)
        else:
            self.intakeMotor.set(ctre.ControlMode.PercentOutput, 0.0)

        if time.time() - self.intake_request_time < 5:
            self.sorterMotor.set(ctre.ControlMode.PercentOutput, 0.2)
        else:
            self.sorterMotor.set(ctre.ControlMode.PercentOutput, 0.0)


        if self.shoot_request == 1:
            self.BeltMotor.set(0.2)
            self.shoot_request = 0
            return

        if self.limitSwitchStop.get():
            return

        if self.limitSwitchStart.get():
            self.BeltMotor.set(0.2)
            self.sorterMotor.set(ctre.ControlMode.PercentOutput, 30)
        else:
            self.sorterMotor.set(ctre.ControlMode.PercentOutput, 0)
