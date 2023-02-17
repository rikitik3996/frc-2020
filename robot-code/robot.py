#!/usr/bin/env python3

import wpilib   # Librairie de base de la FRC
import ctre     # Librairie pour les produits de Cross The Road Electronics
import rev      # Librairie pour les produits de REV Robotics
from magicbot import MagicRobot # La modele de programmation de notre robot. Magic robot
from robotpy_ext.autonomous.selector import AutonomousModeSelector # Crée les modes automatiques à partir des fichier dans ./autonomous/*.py. Sélectionnable depuis le SmartDashbaord
from ntcore import NetworkTableInstance     # Outils pour les NetworkTables
# from networktables.util import ntproperty   # Outils pour les NetworkTables
from components import swervedrive, swervemodule, intake_driver    # Nos composantes logiciels. Permet de grouper les composantes par fonctionalitée
from common import vision                           # Du code générique qui peut nous servir à différente place
from navx import AHRS  # C'est NavX(giro)
import ntcore

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





    navx: AHRS

   


    def createObjects(self):
        """
        This is where all the components are actually created with "=" sign.
        Components with a parent prefix like "shooter_" will be injected.
        """

       
        # Gamepad
        self.gamepad1 = wpilib.Joystick(0)
        # self.gamepad2 = wpilib.Joystick(1)

        # Left Motor
        self.leftMotor1 = ctre.WPI_TalonFX(1)
        self.leftMotor2 = ctre.WPI_TalonFX(2)

        # Right Motor
        self.rightMotor1 = ctre.WPI_TalonFX(3)
        self.rightMotor2 = ctre.WPI_TalonFX(4)
    
         #Navx initalize
        self.navx = AHRS.create_spi()

        # ShuffleBoard ####################################################
        self.configTab = ntcore.NetworkTableInstance.getDefault().getTable("Config")

        self.configTab.putNumber("Pid Kp", 0.01)
        self.configTab.putNumber("Pid Ki", 0)
        self.configTab.putNumber("Pid Kd", 0)

        #######################################################################
        


        # Intake
        # self.intake_motor = ctre.WPI_VictorSPX(6)

        # Wheel of Fortune
        # self.wof_motor = ctre.WPI_VictorSPX(13)

        # Climber
        # self.climbingMotor = ctre.WPI_VictorSPX(10)
        # self.hookMotor = ctre.WPI_VictorSPX(1)

        # Color Sensor
        #self.colorSensor = color_sensor.ColorSensor()

        # Vision
        # self.vision = vision.Vision()

        # Limit Switch
        # self.switch = wpilib.DigitalInput(0)

        # PDP
        self.pdp = wpilib.PowerDistribution()

    def disabledPeriodic(self):
        # Update the dashboard, even when the robot is disabled.
        self.update_sd()

    # def autonomousInit(self):
    #     # Reset the drive when the auto starts.
    #     self.drive.flush()ss
    #     self.drive.threshold_input_vectors = True

    def autonomous(self):
        # For auto, use MagicBot's auto mode.
        # This will load the ./autonomous folder.
        super().autonomous()

    def teleopInit(self):
        self.NavxZero = self.navx.getPitch()
        # Reset the drive when the teleop starts.
        self.NavxYawZero = self.navx.getYaw()
        print(self.NavxYawZero)
        # self.drive.NavxYawZero = self.NavxYawZero
        # self.drive.flush()
        # self.drive.squared_inputs = True
        # self.drive.threshold_input_vectors = True

        # self.sd.putNumber('test/val ue', 0)

    def move(self, fwd, straff, rcw):
        """
        This function is ment to be used by the teleOp.
        :param x: Velocity in x axis [-1, 1]
        :param y: Velocity in y axis [-1, 1]
        :param rcw (Rotation clockwise): Velocity in z axis [-1, 1]
        """

        # self.drive.move(fwd, straff, rcw)

    def teleopPeriodic(self):

        
        NavxPitch = self.navx.getPitch() - self.NavxZero
        #Mettre le NavX à zéro grâce à la gachette
        if self.gamepad1.getRawButton(10):
            self.NavxYawZero = self.navx.getYaw


        # Drive
        # self.gamepad1.getRawAxis(0) == Left joystick, X axis
        # self.gamepad1.getRawAxis(1) == Left joystick, Y axis
        # self.gamepad1.getRawAxis(5) == Right joystick, Y axis
        # self.gamepad1.getRawAxis(4) == Right joystick, X axis
        if self.gamepad1.getRawButton(4):
            print(NavxPitch)
            self.move(NavxPitch / 10, 0, 0)
        elif self.gamepad1.getRawButton(7):
            print("button pressed")

        else:
            self.fwd.append(-self.gamepad1.getRawAxis(1))
            self.straff.append(self.gamepad1.getRawAxis(0))
            self.rot.append(self.gamepad1.getRawAxis(4))

            average_samples = 5
            self.fwd = self.fwd[-average_samples:]
            self.straff = self.straff[-average_samples:]
            self.rot = self.rot[-average_samples:]

            fwd = sum(self.fwd)/len(self.fwd)
            straff = sum(self.straff)/len(self.straff)
            rot = sum(self.rot)/len(self.rot)

            self.move(fwd, straff, rot)
        # print(self.frontLeftModule_encoder.getAbsolutePosition(),
        #         self.frontRightModule_encoder.getAbsolutePosition(),
        #         self.rearLeftModule_encoder.getAbsolutePosition(),
        #         self.rearRightModule_encoder.getAbsolutePosition())
        # Lock
        #  if self.gamepad1.getRawButton(1):
        #     self.drive.request_wheel_lock = True

        # # Vectoral Button Drive
        # if self.gamepad1.getPOV() == 0:
        #     self.drive.set_raw_fwd(-0.99)
        # elif self.gamepad1.getPOV() == 180:
        #     self.drive.set_raw_fwd(0.99)
        # elif self.gamepad1.getPOV() == 90:
        #     self.drive.set_raw_strafe(0.99)
        # elif self.gamepad1.getPOV() == 270:
        #     self.drive.set_raw_strafe(-0.99)


        # print("NavX Gyro", self.navx.getYaw, self.navx.getPitch(), self.navx.getRoll(),"Angle ", self.navx.getAngle())

        # Climber
        # if self.gamepad2.getRawButton(1):
        #     self.climbingMotor.set(1)
        # else:
        #     self.climbingMotor.set(0)

        # Hook
        # if self.gamepad2.getRawAxis(5) < 0 and not self.switch.get():
        #     self.hookMotor.set(self.gamepad2.getRawAxis(5))
        # elif self.gamepad2.getRawAxis(5) > 0:
        #     self.hookMotor.set(self.gamepad2.getRawAxis(5))
        # else:
        #     self.hookMotor.set(0)

        # Shooter
        # if self.gamepad1.getRawAxis(3) > 0:
        #     self.shooter.shoot()
        # elif self.gamepad1.getRawButton(6):
        #     self.shooter.align()
        # elif self.gamepad1.getRawButton(5) or self.gamepad2.getRawAxis(2) > 0:
        #     self.shooter.unload()
        # elif self.gamepad1.getRawAxis(2) > 0 or self.gamepad2.getRawAxis(3) > 0:
        #     self.shooter.intake()
        # else:
        #     self.shooter.stop()

        # WoF
        # if self.gamepad2.getRawButton(3):
        #     self.wof.handleFirstStage()
        # elif self.gamepad2.getRawButton(2):
        #     self.wof.handleSecondStage()
        # elif self.gamepad2.getRawButton(4):
        #     self.wof.reset()
        # elif self.gamepad2.getRawButton(5):
        #     self.wof.manualTurn(1)
        # elif self.gamepad2.getRawButton(6):
        #     self.wof.manualTurn(-1)
        # else:
        #     self.wof.manualTurn(0)

        # Update smartdashboard
        self.update_sd()

    def update_sd(self):
        """
        Calls each component's own update function
        and puts data to the smartdashboard.
        """
        # self.sd.putNumber('Climb_Current_Draw', self.pdp.getCurrent(10))
        return
        # self.drive.update_smartdash()
        #self.colorSensor.updateSD()
        # self.wof.updateSD()
        # self.vision.updateTable()

if __name__ == "__main__":
    wpilib.run(MyRobot)
