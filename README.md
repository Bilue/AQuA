# AQuA (Automated Quality Assurance) Hybrid Framework in Python
The Hybrid Framework integrates various automation testing methodologies such as Page Object Model (POM), Data-Driven Testing, and Keyword-Driven Testing. The Page Object Model (POM) is a design pattern utilized in test automation to encapsulate and manage the representation of web pages in a single location. It establishes an object-oriented model where web page elements are defined as properties within a class, offering a centralized approach to access these elements. This approach enhances test script readability, maintainability, and scalability by creating a separation between test code and the underlying web page structure.


## Getting started with AQuA
Here are the steps to set up framework in Python:

## Install required packages:
You need to have the following packages installed: selenium, unittest, and pytest.

## Create a directory for your project: 
Choose a location for your project and create a directory for it.

## Create a Python file for your page object class: 
This file will define the page object class and its properties, representing the elements on the page.

## Create a Python file for your tests: 
This file will contain the tests that will interact with the page object class, performing actions on the elements and asserting the results.

## Run your tests: 
Use a test runner, such as Pytest, to run your tests.

## Writing the Page Object Class:
The page object class should contain properties that represent the elements on the page
## Setup

# This test requires the following tools to work
- Appium 2 beta (please use https://appium.github.io/appium/docs/en/2.0/)
- Xcode and simulators 
- Android studio and emulators
- xcuitest - an Appium iOS automator
- uiautomator2 - an Appium Android automator
- Python 3.11 
- All external reqs in the requirements.txt

```
pip install -r requirements.txt
```

## Run tests
### Run all tests
```
pytest --html=reports/Automation-Report.html py.test --log-cli-level=INFO
pytest --html=Reports/report.html tests/bilue --log-cli-level=INFO --section_name=iOS-iPhone14Pro-app
```

### Run an arbitrary file
Pytest uses class, module or method names starting with test_ or Test_ to target test for executions.

```
pytest -k 'Test_app_Login or Test_video_player or Test_Android_Launch_Uiautomator'
pytest --html=reports/report.html tests/bilue/test_profile.py --log-cli-level=INFO --section_name=Android-Pixel5-app
pytest --html=Reports/report.html tests/bilue/test_profile.py --log-cli-level=INFO --section_name=iOS-iPhone14Pro-app
```

## TestCase
### unittest based
```
pytest --html=reports/Automation-Report.html tests/bilue/test_home_screen.py --log-cli-level=INFO
```
### For ERRORS Only and to be used in CI/CD pipeline
```
pytest --html=reports/Automation-Report.html tests/bilue/test_home_screen.py --log-cli-level=INFO
```


