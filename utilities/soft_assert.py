from utilities.custom_logger import LogGen
from typing import List, Tuple, Any, Optional, Dict


class SoftAssert:
    """
    SoftAssert class provides a mechanism for performing soft assertions in test scripts.
    Soft assertions allow the test execution to continue even if an assertion fails,
    and collect all the failed assertions for reporting.

    Usage:
        1. Initialize an instance of the SoftAssert class:
           soft_assert = SoftAssert()

        2. Use the available assertion methods to perform soft assertions:
           - assert_true(expr, msg=None)
           - assert_false(expr, msg=None)
           - assert_equal(actual, expected, msg=None)

        3. Call the assert_all() method at the end to raise an AssertionError if any
           soft assertions have failed.

    Example:
        soft_assert = SoftAssert()
        soft_assert.assert_true(5 > 3, "Check if 5 is greater than 3")
        soft_assert.assert_false(2 == 2, "Check if 2 is not equal to 2")
        soft_assert.assert_equal(10, 20, "Check if 10 is equal to 20")

        soft_assert.assert_all()

    Author:
        Gaurav Purwar

    """
    logger = LogGen.loggen()

    def __init__(self):
        self.errors = []

    def __call__(self, condition, msg=None, assertion_type=""):
        try:
            assert condition, msg
            self.logger.info(f"{msg}: Assertion {assertion_type} Performed!***")
        except AssertionError as e:
            self.errors.append(str(e))

    def assert_true(self, expr, msg=None):
        self(expr, msg, assertion_type="True")

    def assert_false(self, expr, msg=None):
        self(not expr, msg, assertion_type="False")

    def assert_equal(self, actual, expected, msg=None):
        self(actual == expected, msg, assertion_type="Equal")

    def assert_all(self):
        if len(self.errors) > 0:
            message = '\n'.join(self.errors)
            raise AssertionError(message)

    def perform_equal_assertions(self, assertions: List[Tuple[Any, Any]], page_object: Any, attribute: Optional[str] = None) -> None:
        """
            Performs a series of assertions by comparing expected values with the actual values
            of a specific attribute of the menu_side_bar object.

            Args:
                assertions (List[Tuple[Any, Any]]): A list of tuples containing expected values and elements to assert.
                page_object (Any): The page object representing a specific page within the test class.
                attribute (str, optional): The attribute to retrieve from the menu_side_bar elements. Defaults to None.
            Returns:
                None
            """
        for expected_value, element in assertions:
            actual_value = page_object.get_attribute(element, attribute)
            message = f"Expected value: '{expected_value}' should match the actual value: '{actual_value}'"
            self.assert_equal(actual_value, expected_value, message)

    def perform_true_assertions(self, elements_to_check: Dict[Any, str], page_object: Any) -> None:
        """
        Asserts the visibility of specified elements on a page.

        Args:
            elements_to_check (Dict[Any, str]): Dictionary containing elements and their associated messages.
            page_object (Any): The page object representing a specific page within the test class.

        Returns:
            None
        """
        for ele, message in elements_to_check.items():
            is_visible = page_object.is_visible_after_wait(ele)
            self.assert_true(is_visible, message)
