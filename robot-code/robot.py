#!/usr/bin/env python3
import os, pwd
os.getlogin = lambda: pwd.getpwuid(os.getuid())[0]

import wpilib   # Librairie de base de la FRC
import ctre     # Librairie pour les produits de Cross The Road Electronics
import rev      # Librairie pour les produits de REV Robotics
from magicbot import MagicRobot # La modele de programmation de notre robot. Magic robot
from robotpy_ext.autonomous.selector import AutonomousModeSelector # Crée les modes automatiques à partir des fichier dans ./autonomous/*.py. Sélectionnable depuis le SmartDashbaord
from components import canon_driver, intake_driver, tank_drive_driver    # Nos composantes logiciels. Permet de grouper les composantes par fonctionalitée
from common.limelight import Limelight
from navx import AHRS  # C'est NavX(giro)
import ntcore   # NetworkTables

class MyRobot(MagicRobot):
    """
    Après avoir créer les 'components' de bas niveau, tel que 'drivetrain' ou 'intake', utiliser leur nom suivi d'un trait souligné (_)
    pour injecter des objets au composant.

    ex.:
    Après avoir créer dans 'components' un fichier shooter.py, utiliser une variable nommée "shooter_beltMotor: ctre.WPI_TalonFX" déclare le type de la variable.
    Quand 'beltMotor' sera appelée depuis 'shooter', ce sera un objet de type 'WPI_TalonFX'.

    Utiliser un signe égale (=) pendant la déclaration des variables tel que "shooter_beltMotor = ctre.WPI_TalonFX(11)" crée l'objet.
    Quand 'beltMotor' est appelé depuis le composant 'shooter' et ce sera un WPI_TalonFX avec un ID CAN de 11.

    Utilisez le signe = dans la fonction 'createObjects' pour vous assurer que les données sont biens transmises à leur composantes.

    Pour plus d'information: https://robotpy.readthedocs.io/en/stable/frameworks/magicbot.html
    """

    # PCM: CAN ID 30
    # PDP: CAN ID 21
    # Talon SRX: CAN ID 11
    # Talon SRX: CAN ID 9
    # Victor SPX: CAN ID 10
    #Spark MAX Motor Controller: CAN ID 1 - Left Wheel
    #Spark MAX Motor Controller: CAN ID 2 - Left Wheel
    #Spark MAX Motor Controller: CAN ID 3 - Right Wheel
    #Spark MAX Motor Controller: CAN ID 4 - Right Wheel
    #Spark MAX Motor Controller: CAN ID 7 - Left Canon
    #Spark MAX Motor Controller: CAN ID 8 - Right Canon

    drive: tank_drive_driver.TankDriveDriver
    canon: canon_driver.CanonDriver
    intake: intake_driver.IntakeDriver

    def createObjects(self):
        """
        This is where all the components are actually created with "=" sign.
        Components with a parent prefix like "shooter_" will be injected.
        """
        # Drivetrain
        self.drive_leftMotor1 = ctre.WPI_TalonFX(1)
        self.drive_leftMotor2 = ctre.WPI_TalonFX(2)
        self.drive_rightMotor1 = ctre.WPI_TalonFX(3)
        self.drive_rightMotor2 = ctre.WPI_TalonFX(4)

        # Canon
        self.canon_leftMotor = ctre.WPI_TalonFX(7)
        self.canon_rightMotor = ctre.WPI_TalonFX(8)

        # Intake
        self.intake_sorterMotor = ctre.VictorSPX(10)
        self.intake_BeltMotor = ctre.TalonSRX(9)
        self.intake_intakeMotor = ctre.TalonSRX(11)
        self.intake_limitSwitchStart = wpilib.DigitalInput(0)
        self.intake_limitSwitchStop = wpilib.DigitalInput(1)

        # NetworkTable
        self.nt = ntcore.NetworkTableInstance.getDefault().getTable("SmartDashboard")

        # General
        self.pdp = wpilib.PowerDistribution(21, wpilib.PowerDistribution.ModuleType.kCTRE)
        self.pcm = wpilib.PneumaticsControlModule(30)
        self.navx = AHRS.create_spi()
        self.pixie_offset = wpilib.AnalogInput(0)
        self.pixie_valid = wpilib.DigitalInput(2)
        self.limelight = Limelight()

        # Gamepad
        self.gamepad1 = wpilib.Joystick(0)

    def disabledPeriodic(self):
        # Update the dashboard, even when the robot is disabled.
        self.update_sd()

    def autonomousInit(self):
        # Reset the drive when the auto starts
        pass

    def autonomous(self):
        # For auto, use MagicBot's auto mode.
        # This will load the ./autonomous folder.
        super().autonomous()

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        if self.gamepad1.getRawButton(1):
            self.drive.pixie_drive()
            self.intake.intake_request()
        elif self.gamepad1.getRawButton(2):
            self.drive.limelight_drive()
            if self.limelight.targetReady():
                self.canon.shoot()
        else:
            self.drive.move(self.gamepad1.getRawAxis(1) * -1, self.gamepad1.getRawAxis(5) * -1)
        self.nt.putNumber('gamepad1/axis/0', self.gamepad1.getRawAxis(0))
        self.nt.putNumber('gamepad1/axis/1', self.gamepad1.getRawAxis(1))
        self.nt.putNumber('gamepad1/axis/2', self.gamepad1.getRawAxis(2))
        self.nt.putNumber('gamepad1/axis/3', self.gamepad1.getRawAxis(3))
        self.nt.putNumber('gamepad1/axis/4', self.gamepad1.getRawAxis(4))
        self.nt.putNumber('gamepad1/axis/5', self.gamepad1.getRawAxis(5))

        self.nt.putNumber('gamepad1/buttons/1', self.gamepad1.getRawButton(1))
        self.nt.putNumber('gamepad1/buttons/2', self.gamepad1.getRawButton(2))
        self.nt.putNumber('gamepad1/buttons/3', self.gamepad1.getRawButton(3))
        self.nt.putNumber('gamepad1/buttons/4', self.gamepad1.getRawButton(4))

        self.nt.putNumber('navx/pitch', self.navx.getPitch())
        self.nt.putNumber('navx/yaw', self.navx.getYaw())
        self.nt.putNumber('navx/roll', self.navx.getRoll())
        self.nt.putNumber('navx/angle', self.navx.getAngle())


        self.update_sd()

    def update_sd(self):
        """
        Calls each component's own update function
        and puts data to the smartdashboard.
        """
        self.nt.putNumber('test', 123)
        # self.configTab.putNumber('Channel 0 current', self.pdp.getCurrent(0))
        return

if __name__ == "__main__":
    wpilib.run(MyRobot)
