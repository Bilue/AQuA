import os
from datetime import datetime
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, WebDriverException, InvalidSessionIdException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from utilities.main_driver import MainDriver
from utilities.custom_logger import LogGen
from utilities.read_properties import ReadProperties, read_config

"""
    @Author: Gaurav Purwar
    
    SwipeDirection Utils The class uses Selenium and Appium to find elements on the mobile app's user interface. This 
    code defines a class SwipeDirection with two class variables Up and Down. It also defines a class Utils that 
    performs utility functions for an app called MainDriver. The Utils class has a logger and an instance variable 
    app that is initialized in the constructor.
    
    
    The class provides a get_element method that returns an element based on a provided locator. The locator is a tuple 
    with the first element being the method to use for finding the element and the second element being the locator 
    value. If the locator value is a string, the method get_element_by_type is called with the method and value. If the 
    locator value is a list, the method iterates over the values and tries to find the element using get_element_by_type. 
    If none of the values can find the element, a NoSuchElementException is raised.
    
    Created On: 20 Jan 2023
    Updated On: 27 Jul 2023
    

"""
config = read_config()


class SwipeDirection():
    Up = "Up"
    Down = "Down"


class TVRemoteAction:
    HOME = 'home'
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    MENU = 'menu'
    PLAYPAUSE = 'playpause'
    ENTER = 'select'


class Utils:
    logger = LogGen.loggen()

    def __init__(self, app: MainDriver):
        super().__init__()
        self.app = app

    # get elements
    # posts_icon = ('accessibility_id', 'Posts') > Sample Locator Value
    def get_element(self, locator):
        """
        Returns element based on provided locator.
        Locator include the method and locator value in a tuple.
        :param locator:
        :return:
        """

        method = locator[0]
        values = locator[1]

        if type(values) is str:
            return self.get_element_by_type(method, values)
        elif type(values) is list:
            for value in values:
                try:
                    return self.get_element_by_type(method, value)
                except NoSuchElementException:
                    pass
            raise NoSuchElementException

    def get_attribute(self, locator, attribute):
        return self.get_element(locator).get_attribute(attribute)

    def get_locator(self, method, value):
        """
        This function returns a locator that can be used with Appium's get_element_by_type method.
        The method of finding the element is specified by the method argument, which can be one of the following:

        accessibility_id android ios class_name id xpath name The value argument specifies the search criteria for
        the element. If the specified method is not recognized, the function raises an "Invalid locator method."
        exception.

        :param method: The method of finding the element. Should be one of the MobileBy constants or a string.
        :param value: The search criteria for the element.
        :return: A tuple (locator, value) that can be used with find_element method.
        """
        special_cases = {
            AppiumBy.ANDROID_UIAUTOMATOR: (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().%s' % value)
        }

        if method in special_cases:
            return special_cases[method]
        elif method in [AppiumBy.ACCESSIBILITY_ID, AppiumBy.IOS_PREDICATE, AppiumBy.IOS_UIAUTOMATION,
                        AppiumBy.CLASS_NAME, AppiumBy.ID, AppiumBy.XPATH, AppiumBy.NAME]:
            return method, value
        else:
            raise Exception('Invalid locator method.')

    def get_element_by_type(self, method, value):
        """
        This function finds an element on a mobile app's user interface using Appium with the specified locator and value.

        :param method: The method of finding the element.
        :param value: The search criteria for the element.
        :return: The found element or raises an "Element Not Found" exception.
        """
        try:
            locator, value = self.get_locator(method, value)
            return self.app.driver_instance.find_element(locator, value)
        except Exception as e:
            raise Exception('Element Not Found, method: ' + method + " & locator: " + value)

    def get_elements(self, locator):
        """
        Returns element based on provided locator.
        Locator include the method and locator value in a tuple.
        :param locator:
        :return:
        """

        method = locator[0]
        values = locator[1]

        if type(values) is str:
            return self.get_elements_by_type(method, values)
        elif type(values) is list:
            for value in values:
                try:
                    return self.get_elements_by_type(method, value)
                except NoSuchElementException:
                    pass
            raise NoSuchElementException

    def get_elements_by_type(self, method, value):
        """
        Refer get_element_by_type
        :param method:
        :param value:
        :return:
        """
        try:
            locator, value = self.get_locator(method, value)
            return self.app.driver_instance.find_elements(locator, value)
        except Exception as e:
            raise Exception(
                'Failed to find the locator in the list of elements, method: ' + method + " & locator: " + value + " - Error: " + str(
                    e))

    def is_visible(self, locator):
        try:
            els = self.get_elements(locator)
            if len(els) != 0:
                if els[0].is_displayed():
                    self.logger.info("Verified Element Present: " + locator[1])
                    return True
                else:
                    return False
            else:
                return False
        except:
            self.logger.error("Error while finding element: " + locator[1])
            return False

    def wait_visible(self, locator, timeout=None):
        """
        This is a Python function that waits for an element to become visible on a mobile app's user interface using
        Appium. The element's location is specified by the locator argument, which is a tuple containing two values:
        the method for finding the element (e.g., accessibility_id, class_name, etc.) and the search criteria (e.g.,
        'button1', 'input_field', etc.).

        The function repeatedly calls the is_visible() method, which checks if the element is currently visible on
        the screen, until the element becomes visible or the timeout value is reached. The timeout value depends on
        the platform being used, either 2 seconds for iOS or 1000 for Android. If the element is never visible,
        the function raises an exception indicating that the element never became visible, including the method and
        search criteria used.

        :param timeout:
        :param locator:
        :return:
        """
        i = 0
        platform_name = ReadProperties.get_platform_name()
        if timeout is None:
            if platform_name == 'ios':
                timeout = ReadProperties.get_ios_wait_time()
            else:
                timeout = ReadProperties.get_android_wait_time()

        self.logger.warning(" Wait Timeout Cycle is: " + str(timeout))

        while i != timeout:
            try:
                if not self.is_visible(locator):
                    self.logger.info(str(i) + " Checking for element " + locator[1])
                else:
                    self.logger.info(str(i) + " element visible: " + locator[1])
                    return self.get_element(locator)
            except NoSuchElementException as e:
                self.logger.error("Error occurred while finding element: %s", str(e))
                sleep(0.1)
            i += 1
        raise Exception('Element never became visible: %s (%s)' % (locator[0], locator[1]))

    # save Screenshot
    def saveScreenshot(self, tcName):
        timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        file_name = tcName + "_screenshot_{}.png".format(timestamp)
        screenshots_dir = os.path.join(os.getcwd(), "reports", "screenshots")  # Define the screenshots directory
        file_path = os.path.join(screenshots_dir, file_name)  # Create the full file path
        self.app.driver_instance.get_screenshot_as_file(file_path)
        relative_path = file_path.replace(os.getcwd(), '')  # Get the relative path
        return relative_path

    # clicks and taps
    def click(self, locator=None, element=None):
        if element is not None:
            element.click()
            self.logger.info(f"Clicked on element {str(element)}")
        elif locator is not None:
            element = self.wait_visible(locator)
            element.click()
            self.logger.info(f"Clicked on element {str(locator[1])}")
        else:
            raise ValueError("Either a locator or an element must be provided.")

    def tap(self, locator=None, percentage=1.0):
        if locator is not None:
            element = self.wait_visible(locator)
            location = element.location
            width = element.size['width']
            x = location['x'] + int(width * percentage)
            y = location['y'] + element.size['height'] // 2
            self.logger.warning(
                "x :" + str(x) + " location['x'] :" + str(location['x']) + " width :" + str(width) + " y :" + str(
                    y) + " location['y'] :" + str(location['y']) + " height :" + str(element.size['height']))
            touch_action = TouchAction(self.app.driver_instance)
            touch_action.tap(x=x, y=y).perform()
            self.logger.info("Tapped on element " + locator[1])
        else:
            raise ValueError("A locator must be provided.")

    def tap_center(self, override_x: int = None, override_y: int = None, duration: int = 500):
        """
        Uses the driver 'tap' method to tap in the center of the screen, useful in video test cases/
        The coordinate can also be overridden by giving an int value for BOTH override_x and override_y.
        Otherwise the method will assign its own value by using get_window_size() / 2
        :param duration:
        :param override_x: default None
        :param override_y: default None
        :return:
        """
        screen_size = self.app.driver_instance.get_window_size()
        if override_x is None or override_y is None:
            override_x = (screen_size["width"] / 2)
            override_y = (screen_size["height"] / 2)
        self.app.driver_instance.tap([(override_x, override_y)], duration)

    def hide_keyboard(self):
        try:
            sleep(0.5)
            self.app.driver_instance.hide_keyboard()
        except WebDriverException:
            pass

    def send_keys(self, locator, text):
        element = self.wait_visible(locator)
        element.clear()
        element.send_keys(text)
        sleep(0.1)

    def set_value(self, locator, text):

        element = self.wait_visible(locator)
        element.clear()
        element.set_value(text)
        sleep(0.1)

    def clear(self, locator):
        element = self.wait_visible(locator)
        element.clear()
        sleep(0.1)

    def swipe_down(self, locator=None, timeout=None, duration=2000):
        """
        Swipes down until the given element is visible, or swipes down for a specified duration if no element is specified.
        """
        if locator is None:
            # Swipe down for a specified duration
            i = 0
            timeout = timeout or 50
            while i < timeout:
                start_x = int(self.app.driver_instance.get_window_size()['width'] / 2)
                start_y = int(self.app.driver_instance.get_window_size()['height'] * 0.8)
                end_y = int(self.app.driver_instance.get_window_size()['height'] * 0.2)
                self.app.driver_instance.swipe(start_x, start_y, start_x, end_y, duration)
                self.logger.info(str(i) + " Scrolling down...")
                i += 1
        else:
            # Swipe down until the element is visible
            i = 0
            timeout = timeout or 50
            while i < timeout:
                try:
                    element = self.app.driver_instance.find_element(*locator)
                    if element.is_displayed():
                        break
                except NoSuchElementException:
                    pass
                start_x = int(self.app.driver_instance.get_window_size()['width'] / 2)
                start_y = int(self.app.driver_instance.get_window_size()['height'] * 0.8)
                end_y = int(self.app.driver_instance.get_window_size()['height'] * 0.2)
                self.app.driver_instance.swipe(start_x, start_y, start_x, end_y, duration)
                self.logger.info(str(i) + " Scrolling down to check for the element " + locator[1])
                i += 1
            else:
                raise NoSuchElementException(f"Could not find element during swipe down {locator}")

    def swipe_up(self, locator=None, timeout=None, duration=2000):
        """
        Swipes up until the given element is visible, or swipes up for a specified duration if no element is specified.
        """
        if locator is None:
            # Swipe up for a specified duration
            start_x = int(self.app.driver_instance.get_window_size()['width'] / 2)
            start_y = int(self.app.driver_instance.get_window_size()['height'] * 0.8)
            end_y = int(self.app.driver_instance.get_window_size()['height'] * 0.6)
            # self.app.driver_instance.swipe(start_x, start_y, start_x, end_y, duration)
            self.app.driver_instance.swipe(start_x, end_y, start_x, start_y, duration)

        else:
            # Swipe up until the element is visible
            i = 0
            timeout = timeout or 50
            while i < timeout:
                try:
                    element = self.app.driver_instance.find_element(*locator)
                    if element.is_displayed():
                        break
                except NoSuchElementException:
                    pass
                start_x = int(self.app.driver_instance.get_window_size()['width'] / 2)
                start_y = int(self.app.driver_instance.get_window_size()['height'] * 0.8)
                end_y = int(self.app.driver_instance.get_window_size()['height'] * 0.6)
                self.app.driver_instance.swipe(start_x, end_y, start_x, start_y, duration)
                # self.app.driver_instance.swipe(start_x, start_y, start_x, end_y, duration)
                self.logger.info(str(i) + " Scrolling up to check for the element " + locator[1])
                i += 1
            else:
                raise NoSuchElementException(f"Could not find element during swipe up {locator}")

    def swipe_l_r_l(self, locator, direction='l_t_r', timeout=None):
        """Swipes left until the given element is visible."""
        i = 0
        timeout = timeout or 50
        while i < timeout:
            try:
                element = self.app.driver_instance.find_element(*locator)
                if element.is_displayed():
                    return True
            except NoSuchElementException:
                pass
            if direction == 'l_t_r':
                start_x = int(self.app.driver_instance.get_window_size()['width'] * 0.2)
                end_x = int(self.app.driver_instance.get_window_size()['width'] * 0.8)
            elif direction == 'r_t_l':
                start_x = int(self.app.driver_instance.get_window_size()['width'] * 0.8)
                end_x = int(self.app.driver_instance.get_window_size()['width'] * 0.2)
            else:
                raise ValueError(f"Invalid direction: {direction}")

            start_y = int(self.app.driver_instance.get_window_size()['height'] / 2)
            self.app.driver_instance.swipe(start_x, start_y, end_x, start_y, 2000)
            self.logger.info(str(i) + " Scrolling left to check for the element " + locator[1])
            i += 1
            try:
                self.app.driver_instance.find_element(*locator)
            except NoSuchElementException:
                pass
            else:
                return True
        raise NoSuchElementException(f"Could not find element during swipe left {locator}")

    # get text
    def get_text(self, locator):
        element = self.wait_visible(locator)
        return element.text

    def wait_for_element_to_appear(self, locator, timeout=50):
        try:
            WebDriverWait(self.app.driver_instance, timeout=timeout).until(
                expected_conditions.visibility_of_any_elements_located(self.get_element(locator)))
        except Exception as e:
            self.logger.error(
                "Error while performing explicit wait for element " + locator[1] + " for " + str(timeout) + str(e))
        self.logger.info("Explicit Wait for element " + locator[1] + " for " + str(timeout))

    def wait_implicit(self, timeout):
        self.app.driver_instance.implicitly_wait(timeout)
        self.logger.info("Implicit Wait for " + str(timeout))

    def Swipe_by_element(self, start_element: WebElement, end_element: WebElement, velocity=1000):
        # perform the swipe by element
        action = self.app.set_actions()
        action.long_press(el=start_element, duration=velocity).move_to(el=end_element).perform()

    def Swipe_by_coord(self, start_x: int = 0, start_y: int = 0, end_x: int = 0, end_y: int = 0, velocity=1000):

        # set action object and perform Swipe_Up
        LogGen.loggen().info(f"Swipe_by_coord: start_x:{start_x}, start_y:{start_y}, end_x:{end_x}, end_y:{end_y}, velocity:{velocity}.")
        action = self.app.set_actions()
        action.long_press(el=None, x=start_x, y=start_y, duration=velocity).move_to(el=None, x=end_x,
                                                                                    y=end_y).release().perform()

    def Swipe(self, Direction: str = SwipeDirection.Up, velocity=1000):
        """
        Will attempt to swipe up by using cording from the centre of the screen
        """
        screen_size = self.app.driver_instance.get_window_size()
        # to fix Invalid positon value, either x and y has exceeded the screen or is below minimum
        center_x = screen_size['width'] / 2
        center_y = screen_size['height'] / 2

        if Direction == SwipeDirection.Up:
            start_x = center_x
            start_y = center_y
            end_x = center_x
            end_y = (center_y * 2)
            return self.Swipe_by_coord(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, velocity=velocity)
        elif Direction == SwipeDirection.Down:
            start_x = center_x
            start_y = center_y
            end_x = center_x
            end_y = (center_y * 0)
            return self.Swipe_by_coord(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, velocity=velocity)

        self.logger.info("Swipe performed " + str(Direction))

    def get_list_of_num_from_str(String: str):
        """
        This code defines a function called get_list_of_num_from_str that takes a string as an argument. The function
        splits the string into a list of substrings using the split() method, which by default splits a string into a
        list of words using whitespaces as the separator. Then, it creates a list of integers using a list
        comprehension, where each integer is created from a character in the substrings that is a digit using the
        isdigit() method. Finally, the function returns the list of integers.
        :return:
        """
        num = [int(each_character) for each_character in String.split() if each_character.isdigit()]
        return num

    def get_toggle_switch_status(self, locator):
        """
        Gets the current toggle switch status (ON or OFF).

        Parameters:
        - locator: a locator for the toggle switch button.

        Returns:
        - True if the toggle switch is ON.
        - False if the toggle switch is OFF.
        """
        platform_name = ReadProperties.get_platform_name()
        if platform_name == 'ios':
            return bool(int(self.get_attribute(locator, "value")))
        elif platform_name == 'Android':
            switch_val_str = self.get_attribute(locator, "content-desc")
            return 'not' not in switch_val_str.lower()
        else:
            raise ValueError(
                "Invalid platform name: " + platform_name)

    def tap_toggle_switch_button(self, locator, status=False, percentage=1.0):
        """
        This function taps a toggle switch button and verifies that the switch is in the expected state. It takes in a locator, a status, and an optional percentage parameter.
        :param locator:
        :param status: Toggle Status to be set to ON or OFF
        :param percentage: The percentage parameter is an optional parameter that allows the user to tap on a specific percentage of the toggle switch button. It takes in a float value between 0.0 and 1.0, where 0.0 represents the leftmost edge of the button and 1.0 represents the rightmost edge of the button. By default, the percentage is set to 1.0, which means that the function will tap on the rightmost edge of the button. However, if the user wants to tap on a different part of the button, they can specify the desired percentage value when calling the function.
                            For example, if the user wants to tap in the middle of the button, they can pass in a percentage value of 0.5. If the user wants to tap on the left third of the button, they can pass in a percentage value of 0.33.
        :return:
        """
        switch_val = None
        platform_name = ReadProperties.get_platform_name()
        if platform_name == 'ios':
            switch_val = int(self.get_attribute(locator, "value"))
        elif platform_name == 'Android':
            switch_val_str = self.get_attribute(locator, "content-desc")
            switch_val = 0 if 'not' in switch_val_str.lower() else 1

        if status:
            if switch_val == 0:
                self.tap(locator, percentage)
            elif switch_val == 1:
                self.logger.info("Toggle Switch is Already ON!")
        else:
            if switch_val == 0:
                self.logger.info("Toggle Switch is Already OFF!")
            elif switch_val == 1:
                self.tap(locator, percentage)
            else:
                raise ValueError(
                    "Check the switch value attribute: " + str(switch_val) + " for the locator :" + str(locator[1]))

        if self.get_toggle_switch_status(locator) != status:
            raise ValueError(
                "Toggle Switch state could not be changed to " + str(status) + " current value :" + str(
                    switch_val) + " for the locator :" + str(locator[1]))
        else:
            self.logger.info(
                "Toggle is set to :" + str(status) + "::" + str(switch_val) + " for the locator :" + str(locator[1]))

    def tv_remote_control(self, action: TVRemoteAction):
        """
        Simulate TV remote control actions.

        Parameters:
            action (TVRemoteAction): The TV remote button action to perform.

        Returns:
            None
        """
        # Perform TV remote action
        self.app.driver_instance.execute_script("mobile: pressButton", {"name": action})
        self.logger.info(f"Performed TV remote action '{action}'")
