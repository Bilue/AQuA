import configparser
import os

import pytest
from py._xmlgen import html
from platform import python_version

from tests.bilue.base_tests import ScreenshotManager
from utilities.application import Application
from utilities.custom_logger import LogGen
from utilities.read_properties import ReadProperties

logger = LogGen.loggen()


@pytest.fixture(scope='session')
def mobile_devices():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'configs', 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    devices = [section for section in config.sections() if "iOS" in section]
    logger.info(f"Config path: {config_path}")
    logger.info(f"Sections in config file: {config.sections()}")
    logger.info(f"iOS devices: {devices}")
    return devices


@pytest.fixture(scope='class')
def App(request, mobile_devices):
    section_name = request.config.getoption("--section_name")
    if not section_name:
        section_name = mobile_devices[0]
    ReadProperties.set_platform_name(section_name)
    ReadProperties.set_device_selection_name(section_name)

    App = Application()
    logger.info("in setup")
    App.set_actions()
    logger.info(f"Running Test on Mobile device: {section_name}")
    App.launchApp(section_name)
    screenSize = App.driver_instance.get_window_size()
    logger.info("Screen size is: %s", screenSize)

    def tearDown():
        logger.info("In tearDown")
        App.close_my_application()
    request.addfinalizer(tearDown)

    return App


def pytest_addoption(parser):
    parser.addoption(
        "--section_name",
        action="store",
        help="section name in config file"
    )


def pytest_configure(config):
    py_version = python_version()
    config.pluginmanager.register(MyCustomHook(), 'my_custom_hook')
    # overwriting old parameters with new parameters
    config._metadata = {
        "User Name": "Gaurav Purwar",
        "Python Version": py_version,
        "Project Name": "Bilue App"
    }


class MyCustomHook:
    @staticmethod
    def pytest_html_results_summary(prefix, summary, postfix):
        prefix.extend([html.h1("Project Name: Bilue App")])
        summary.extend([html.h2("Description: Bilue App for iOS and Android Smoke Test Suite")])
        postfix.extend([html.h2("Status : Completed")])
        # TODO If HTML needs to be in table format

    @staticmethod
    def pytest_html_results_table_row(report, cells):
        from py.xml import html

        class_and_method = report.nodeid.split("::")[-1]
        print("class_and_method: " + class_and_method)

        tcName = class_and_method
        # Add values for the new headers
        # cells.insert(0, html.td(str(report.duration)))
        # cells.insert(1, html.td(str(report.keywords)))
        if report.outcome == 'failed':
            for screenshot_index in range(len(ScreenshotManager.scr)):
                screenshot_filepath = ScreenshotManager.scr[screenshot_index]
                if tcName in screenshot_filepath:
                    cells.insert(5, html.td(html.img(src=screenshot_filepath, width=300, height=500)))

        cells.insert(6, html.td(str(report.nodeid)))
