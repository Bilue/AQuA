# Full list of available capabilities here: https://appium.github.io/appium/docs/en/2.0/guides/caps/
import os

from utilities.read_properties import read_config


def getAndroidCapabilities(section_name):
    config = read_config()

    capabilities = {
        "platformName": config.get(section_name, "platform_name"),
        "appium:automationName": "uiautomator2",
        "appium:deviceName": config.get(section_name, "device_name"),
        "appium:app": os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'apps', config.get(section_name, "app_name"))),
        "appium:ensureWebviewsHavePages": True,
        "appium:nativeWebScreenshot": True,
        "appium:showGradleLog": "true",
        "appium:full_reset": True,
        "appium:newCommandTimeout": 3600,
        "appium:connectHardwareKeyboard": True,
        "appium:appPackage": config.get(section_name, "package_name") if config.has_option(section_name, "package_name") else "",
        "appium:appActivity": config.get(section_name, "activity_name") if config.has_option(section_name, "activity_name") else "",
        "appium:espressoBuildConfig": "{\"additionalAndroidTestDependencies\": [\"androidx.lifecycle:lifecycle-extensions:2.2.0\", \"androidx.activity:activity:1.3.1\",  \"androidx.fragment:fragment:1.3.5\"]}"
    }
    return capabilities
