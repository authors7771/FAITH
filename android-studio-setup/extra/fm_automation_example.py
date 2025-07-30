import time
import random
from appium import webdriver
from selenium.webdriver.common.by import By
import datetime
import os
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options

# Loading time constants
LOADING_SCROLL_WAIT_TIME = 2
LOADING_TAB_WAIT_TIME = 5
LOADING_WAIT_TIME = 1

# Screenshot output path
SCREEN_PATH = "fm/"

# Appium Desired Capabilities
capabilities = dict(
    platformName='Android',
    automationName='UiAutomator2',
    deviceName='', # Replace with your actual deviceName
    udid='',  # Replace with your actual device/emulator ID
    appPackage='com.facebook.orca',
    appActivity='com.facebook.orca.auth.StartScreenActivity',
    noReset='true',
    fullReset='false',
    ensureWebviewsHavePages=True,
    nativeWebScreenshot=True,
    newCommandTimeout=3600,
    language='en',
    locale='US'
)

# Start Appium session
appium_server_url = 'http://localhost:4723'
capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)

# Load test site domain list
with open('testsitelist.txt', 'r') as f:
    tests = [line.strip() for line in f.readlines()]

def access_once(index):
    print('[*] Accessing at:', datetime.datetime.now())
    start = time.time()

    # Navigate to the link in Facebook Messenger
    print(f"[*] Clicking chat thread to find test link (scrolls: {index})")
    ele = driver.find_element(By.XPATH, value='/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[5]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout[1]/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup')
    ele.click()
    time.sleep(LOADING_WAIT_TIME)

    for j in range(index):
        if j % 2 == 0:
            driver.swipe(150, 1000, 150, 645, 900)
            time.sleep(LOADING_SCROLL_WAIT_TIME + round(random.random(), 2))

    time.sleep(1)

    # Attempt to click the domain
    test_domain = tests[index]
    xpath = f'//android.view.View[@content-desc="{test_domain}"]/android.widget.TextView'
    print(f"[*] Clicking test domain: {test_domain}")
    try:
        test_elem = driver.find_element(By.XPATH, value=xpath)
        test_elem.click()
        time.sleep(4)

        # If still on the same page, assume fail and go back
        driver.find_element(By.XPATH, value=xpath)
        driver.back()
        print("[!] Navigation failed, returning to chat.")
    except:
        # Screenshot after successful navigation
        screenshot_name = SCREEN_PATH + f"{index}_fm_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.png"
        driver.save_screenshot(screenshot_name)
        print(f"[+] Screenshot saved to: {screenshot_name}")
        driver.back()
        driver.back()

    end = time.time()
    print('[*] Elapsed time:', str(datetime.timedelta(seconds=end - start)).split('.')[0])

# Example test execution: test the first domain (index 0)
access_once(0)

