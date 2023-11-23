from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains

from utilities.main_driver import MainDriver

"""

This script implements a custom class for automating an application. The class is called 
"Application" and it inherits from two base classes: MainDriver and TouchAction. The MainDriver class is likely a 
custom class for setting up a WebDriver instance for automating an application. The TouchAction class is from the 
Appium library and provides methods for performing touch gestures on a mobile device.

*The MyApplication class has several methods for automating the application, such as:

*open_my_application_ios and open_my_application_android: methods for opening the application on iOS and Android 
devices, respectively.

*close_my_application: method for closing the application.

*set_actions: method for creating a TouchAction instance.

*set_ActionChains: method for creating an ActionChains instance.

The class makes use of the MainDriver class to initialize the WebDriver instance and open the application on a mobile 
device. The TouchAction and ActionChains classes are used for performing touch gestures and mouse actions, respectively.


"""


class Application(MainDriver, TouchAction):
    def __init__(self):
        super().__init__()

    def set_actions(self):
        return TouchAction(self.driver_instance)

    def set_ActionChains(self):
        return ActionChains(self.driver_instance)

    def open_my_application_ios(self):
        self.open_application_ios()

    def open_my_application_android(self):
        self.open_application_android()

    def close_my_application(self):
        self.close_application()
