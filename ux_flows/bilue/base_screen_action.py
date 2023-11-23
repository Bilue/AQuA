from datetime import datetime

from utilities.main_driver import MainDriver


class BaseScreenAction:
    """
    BaseScreenAction class for common steps that needs to be performed which is to be used in test class using flow or navigator class methods.
    Example: go_to_home, go_to_categories, logout, etc

    """
    def __init__(self, app: MainDriver):
        self.app = app

