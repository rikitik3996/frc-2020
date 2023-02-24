import math
import ntcore

class Limelight:
    # Main networktable
    table = ntcore.NetworkTableInstance.getDefault().getTable('limelight')

    cam_height = 38.5 # Camera's height from the ground in inches
    cam_angle = 70 # Camera's angle from the horizontal in degrees

    target_height = 98.25 # Target's mid-point's height from the ground in inches

    debug = True

    def getValues(self):
        '''
        Get values from the Limelight networktable.
        '''
        values = dict()
        values['tx'] = self.table.getNumber('tx', 0)
        values['ty'] = self.table.getNumber('ty', 0)
        values['tv'] = self.table.getNumber('tv', 0)

        return values

    @staticmethod
    def degree_to_rad(degree):
        """
        Convert a given degree value to rad.

        :param degree: a degree value between 0 and 360
        :returns: the radian value betwen 0 and 2pi
        """
        return degree * math.pi / 180

    def getDistance(self):
        '''
        Calculate the distance between the camera and the target wall.
        :return: Distance in inch
        '''
        # https://docs.limelightvision.io/en/latest/cs_estimating_distance.html

        a1 = self.degree_to_rad(self.ty)
        a2 = self.degree_to_rad(self.cam_angle)

        distance = (self.target_height - self.cam_height) / math.tan(a1 + a2)
        return distance

    def verticalAdjust(self):
        '''
        Return the required vertical adjustment (drive) to align.
        :return: Clamped error [-1, 1]
        '''
        error = self.ty
        if error < 0.5 and error > -0.5:
            error = 0
        adjust = max(min(error, 1), -1)
        return adjust

    def horizontalAdjust(self):
        '''
        Get the required horizontal adjustment (rotate) to align.
        :return: Clamped error [-1, 1]
        '''
        error = self.tx
        if error < 0.5 and error > -0.5:
            error = 0
        adjust = max(min(error, 1), -1)
        return adjust

    def updateTable(self):
        if self.debug:
            self.table.putNumber('Drive', self.verticalAdjust())
            self.table.putNumber('Rotate', self.horizontalAdjust())
            self.table.putNumber('Distance', self.getDistance())

    def get_target_valid(self):
        return self.table.getNumber('tv', 0) == 1

    def get_target_x_offset(self):
        return self.table.getNumber('tx', 0)

    def targetReady(self):
        if self.get_target_valid() is False:
            return False
        
        if abs(self.get_target_x_offset()) < 2:
            return True
        return False
