from selenium.webdriver import ActionChains

from utilities.main_driver import MainDriver
from utilities.custom_logger import LogGen
from utilities.utils import Utils


class BaseUI(ActionChains):
    """
    Base class for UI-related functionality in the test automation framework.

    This class provides common methods and utilities for interacting with the user interface.
    It extends the `ActionChains` class, allowing for performing actions like mouse movements and interactions.

    Attributes:
        app (MainDriver): The main driver instance representing the application under test.
        logger: The logger instance for logging purposes.
        utils (Utils): An instance of the Utils class providing utility methods for UI interactions.

    """
    app = None
    logger = LogGen.loggen()

    def __init__(self, app: MainDriver):
        self.app = app
        self.utils = Utils(app)

    def get_element(self, locator):
        return self.utils.get_element(locator)

    def get_attribute(self, locator, attribute: str):
        return self.utils.get_attribute(locator, attribute)

    def get_elements(self, locator):
        return self.utils.get_elements(locator)

    def get_element_by_type(self, method, value):
        return self.utils.get_element_by_type(method, value)

    def is_visible(self, locator):
        self.logger.info("*************** verifying element visibility")
        return self.utils.is_visible(locator)

    def swipe_down(self, locator, timeout):
        self.utils.swipe_down(locator=locator, timeout=timeout)

    def swipe_up(self, locator, timeout):
        self.utils.swipe_up(locator=locator, timeout=timeout)

    def swipe_l_r_l(self, locator, direction='l_t_r', timeout=None):
        self.utils.swipe_l_r_l(locator, direction=direction, timeout=timeout)

    def wait_visible(self, locator, timeout=None):
        self.utils.wait_visible(locator, timeout=timeout)
        self.logger.info("*************** Wait for element visible performed")

    def is_visible_after_wait(self, locator, timeout=None):
        try:
            self.utils.wait_visible(locator, timeout=timeout)
            self.logger.info("*************** Wait for element visible performed")
            return True
        except Exception as e:
            self.logger.warning("*************** Element Not visible: " + str(e))
            return False

    def wait_implicit(self, timeout):
        self.utils.wait_implicit(timeout)

    def wait_for_element_to_appear(self, locator, timeout):
        self.utils.wait_for_element_to_appear(locator, timeout)

    def click(self, locator=None, element=None):
        self.utils.click(locator, element)
        if locator is not None:
            self.logger.info("***************" + str(locator[1]) + " Button clicked")
        else:
            self.logger.info("***************Element clicked")

    def tap(self, locator=None, percentage=1.0):
        self.utils.tap(locator, percentage)

    def send_keys(self, locator, text):
        self.utils.send_keys(locator, text)
        self.logger.info("***************" + str(text) + " Input Entered")

    def set_value(self, locator, text):
        self.utils.set_value(locator, text)
        self.logger.info("***************" + str(text) + " Input Entered")

    def clear(self, locator):
        self.utils.clear(locator)

    def hide_keyboard(self):
        self.utils.hide_keyboard()

    def wait(self, locator):
        self.utils.wait_visible(locator)

    def get_text(self, locator):
        return self.utils.get_text(locator)

    def swipe(self, Direction: str):
        self.utils.Swipe(Direction, velocity=1000)

    def get_toggle_switch_status(self, locator):
        self.utils.get_toggle_switch_status(locator)

    def tap_toggle_switch_button(self, locator, status=False, percentage=1.0):
        self.utils.tap_toggle_switch_button(locator, status=status, percentage=percentage)
        self.logger.info("*************** Tap Toggle Switch performed to:"+str(status))

    def is_enabled(self, locator) -> bool:
        """
        Checks if an element is enabled or disabled.

        Args:
            locator: The element to check.

        Returns:
            True if the element is enabled, False if it is disabled.
        """

        return self.get_element(locator).is_enabled()
