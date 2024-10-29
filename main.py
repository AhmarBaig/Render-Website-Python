import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

start_time = time.time()
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--headless")

def getScreenshot(numRequests):
    driver = webdriver.Chrome(options=chromeOptions)
    driver.maximize_window()
    url = "https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location"
    url.rstrip("/")
    width = 2560
    height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(width, height)

    for _ in range(numRequests):
        driver.get(url)
        filename = re.sub(r'[^a-zA-Z0-9]', '_', url) + '.png'
        driver.save_screenshot("./images/" + filename)
        time.sleep(0.1)
        print(filename)

    driver.quit()
    
# Multithreading so that up to 10,000 screenshots can be done at one time

# Running 100 times takes around 7 mins
# for _ in range(100):
#     getScreenshot(driver, url)

# Use ThreadPoolExecutor to manage fixed number of threads
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit each URL to executor
    futures = [executor.submit(getScreenshot, 10) for _ in range(10)]


print("Time: ", time.time() - start_time)