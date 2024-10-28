import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

start_time = time.time()
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--headless")

def getScreenshot():
    driver = webdriver.Chrome(options=chromeOptions)
    driver.maximize_window()
    url = "https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location"
    url.rstrip("/")
    driver.get(url)

    width = 2560
    height = driver.execute_script("return document.body.scrollHeight")

    driver.set_window_size(width, height)

    filename = re.sub(r'[^a-zA-Z0-9]', '_', url) + '.png'

    # print(filename)
    driver.save_screenshot("./images/" + filename)
    driver.quit()
    time.sleep(0.5)
    
# getScreenshot(driver, url)

# Multithreading so that up to 10,000 screenshots can be done at one time

# Running 100 times takes around 7 mins
# for _ in range(100):
#     getScreenshot(driver, url)

# Use ThreadPoolExecutor to manage fixed number of threads
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit each URL to executor
    futures = [executor.submit(getScreenshot()) for _ in range(100)]

    print(len(futures))

    # Error Handling
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error: {e}")


print("Time: ", time.time() - start_time)