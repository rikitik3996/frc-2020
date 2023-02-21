from magicbot.state_machine import state, timed_state, AutonomousStateMachine

from components import tank_drive_driver

class BaseAuto(AutonomousStateMachine):
    """
    This class is used to end each autonomous mode.
    At the end of each mode either failed or finished will be called.
    Flushing the drive system reduces potential errrors.
    """

    drive: tank_drive_driver.TankDriveDriver

    @state
    def failed(self):
        """
        This state should only be called when an auto mode has failed.
        """
        self.drive.debug(debug_modules=True)
        self.next_state('finish')

    @state
    def finish(self):
        self.drive.flush()
        self.done()
