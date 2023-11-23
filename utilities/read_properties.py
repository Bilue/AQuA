import os
from pathlib import Path
import configparser

from utilities.custom_logger import LogGen


def read_config():
    path = Path(__file__)
    ROOT_DIR = path.parent.absolute().parent
    config_path = os.path.join(ROOT_DIR, "configs/config.ini")
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


"""This script reads values from a configuration file located at "Configs/config.ini". The script 
    contains a class named "ReadProperties" which has four static methods:
    
    *getPlatformName(): returns the value of the "platform" field under the section "common info" in the configuration file.
    *getUserEmail(): returns the value of the "useremail" field under the section "common info" in the configuration file.
    *getPassword(): returns the value of the "password" field under the section "common info" in the configuration file.
    *getSubProfile(): returns the value of the "subprofileName" field under the section "common info" in the configuration file.
    
    @author Gaurav Purwar
"""


class ReadProperties:
    platform_name = None
    # Not the device name, it's the section name in the config.ini
    device_section_name = None

    @staticmethod
    def get_device_name():
        device_name = read_config().get(ReadProperties.device_section_name, 'device_name')
        return device_name

    @staticmethod
    def get_package_name():
        package_name = read_config().get(ReadProperties.device_section_name, 'package_name')
        return package_name

    @staticmethod
    def get_platform_name():
        return ReadProperties.platform_name

    @staticmethod
    def get_user_email():
        return read_config().get('common info', 'useremail')

    @staticmethod
    def get_password():
        return read_config().get('common info', 'password')

    @staticmethod
    def get_sub_profile():
        return read_config().get('common info', 'subprofileName')

    @staticmethod
    def get_ctv_login_url():
        return read_config().get('common info', 'ctv_login_url')

    @staticmethod
    def get_ctv_verify_url():
        return read_config().get('common info', 'ctv_verify_url')

    @staticmethod
    def get_api_key():
        return read_config().get('common info', 'api_key')

    @staticmethod
    def get_ios_wait_time():
        iosWait = read_config().get('common info', 'iosWaitTime')
        return int(iosWait)

    @staticmethod
    def get_android_wait_time():
        androidWait = read_config().get('common info', 'androidWaitTime')
        return int(androidWait)

    @staticmethod
    def get_appium_session_url():
        appiumSession = read_config().get('common info', 'appiumSessionUrl')
        return appiumSession

    @staticmethod
    def set_platform_name(section_name):
        logger = LogGen.loggen()
        platform_name = read_config().get(section_name, 'platform_name')
        logger.info(f" Setting Platform Name as : {platform_name}")
        ReadProperties.platform_name = platform_name

    @staticmethod
    def set_device_selection_name(section_name):
        """
        Called within base_tests.py fixture to set the section_name (test device), to allow other method to use this value.
        """
        logger = LogGen.loggen()
        logger.info(f" Setting Device-section Name as : {section_name}")
        ReadProperties.device_section_name = section_name
        logger.info(f" Device-section Name set as : {ReadProperties.device_section_name}")
