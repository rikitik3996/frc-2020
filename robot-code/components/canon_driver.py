import ctre
from magicbot import magiccomponent

from navx import AHRS #Navx

class CanonDriver:
    # These modules will be injected from ../robot.py
    leftMotor: ctre.WPI_TalonFX
    rightMotor: ctre.WPI_TalonFX

    def setup(self):
        """
        Called after injection.
        """
        self.shoot_request = 0

    def shoot(self):
        self.shoot_request = 1

    def execute(self):
        """ """
        if self.shoot_request:
            self.leftMotor.set(0.2)
            self.rightMotor.set(-0.2)
        else:
            self.leftMotor.set(0)
            self.rightMotor.set(0)
        self.shoot_request = 0
