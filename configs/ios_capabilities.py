# Full list of available capabilities here: https://appium.github.io/appium/docs/en/2.0/guides/caps/
import os

from utilities.read_properties import read_config, ReadProperties


def getiOSCapabilities(section_name):
    config = read_config()

    capabilities = {
        "platformName": config.get(section_name, "platform_name"),
        "appium:app": os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'apps', config.get(section_name, "app_name"))),
        "appium:autoAcceptAlerts": True,
        "appium:autoGrantPermissions": True,
        "appium:automationName": "XCuiTest",
        "appium:commandTimeouts": "12000",
        "appium:deviceName": config.get(section_name, "device_name"),
        "appium:platformVersion": config.get(section_name, "platform_version"),
        "appium:udid": config.get(section_name, "udid"),
        "appium:wdaLaunchTimeout": 50000,
        "appium:xcodeOrgId": "gaurav.purwar@bilue.com.au",
        "appium:xcodeSigningId": "Developer"
    }

    return capabilities
