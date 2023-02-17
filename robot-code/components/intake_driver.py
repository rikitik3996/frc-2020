
import ctre
from dataclasses import dataclass

@dataclass
class IntakeConfig:
    speed: float

class Intake:
    motor: ctre.WPI_VictorSPX
    config: IntakeConfig

    def setup(self):
        print(self.config)

    def execute(self):
        print("TODO")