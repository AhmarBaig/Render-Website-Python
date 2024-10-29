import time
import re
import logging

from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import TimeoutException

from websites import urls

start_time = time.time()

# Trying to log threads
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(threadName)s] %(message)s')

# 100 URLs used for testing
# urls = ['http://www.youtube.com', 'http://www.facebook.com', 'http://www.baidu.com', 'http://www.yahoo.com', 'http://www.amazon.com', 'http://www.wikipedia.org', 'http://www.qq.com', 'http://www.google.co.in', 'http://www.twitter.com', 'http://www.live.com', 'http://www.taobao.com', 'http://www.bing.com', 'http://www.instagram.com', 'http://www.weibo.com', 'http://www.sina.com.cn', 'http://www.linkedin.com', 'http://www.yahoo.co.jp', 'http://www.msn.com', 'http://www.vk.com', 'http://www.google.de', 'http://www.yandex.ru', 'http://www.hao123.com', 'http://www.google.co.uk', 'http://www.reddit.com', 'http://www.ebay.com', 'http://www.google.fr', 'http://www.t.co', 'http://www.tmall.com', 'http://www.google.com.br', 'http://www.360.cn', 'http://www.sohu.com', 'http://www.amazon.co.jp', 'http://www.pinterest.com', 'http://www.netflix.com', 'http://www.google.it', 'http://www.google.ru', 'http://www.microsoft.com', 'http://www.google.es', 'http://www.wordpress.com', 'http://www.gmw.cn', 'http://www.tumblr.com', 'http://www.paypal.com', 'http://www.blogspot.com', 'http://www.imgur.com', 'http://www.stackoverflow.com', 'http://www.aliexpress.com', 'http://www.naver.com', 'http://www.ok.ru', 'http://www.apple.com', 'http://www.github.com', 'http://www.chinadaily.com.cn', 'http://www.imdb.com', 'http://www.google.co.kr', 'http://www.fc2.com', 'http://www.jd.com', 'http://www.blogger.com', 'http://www.163.com', 'http://www.google.ca', 'http://www.whatsapp.com', 'http://www.amazon.in', 'http://www.office.com', 'http://www.tianya.cn', 'http://www.google.co.id', 'http://www.youku.com', 'http://www.rakuten.co.jp', 'http://www.craigslist.org', 'http://www.amazon.de', 'http://www.nicovideo.jp', 'http://www.google.pl', 'http://www.soso.com', 'http://www.bilibili.com', 'http://www.dropbox.com', 'http://www.xinhuanet.com', 'http://www.outbrain.com', 'http://www.pixnet.net', 'http://www.alibaba.com', 'http://www.alipay.com', 'http://www.microsoftonline.com', 'http://www.booking.com', 'http://www.googleusercontent.com', 'http://www.google.com.au', 'http://www.popads.net', 'http://www.cntv.cn', 'http://www.zhihu.com', 'http://www.amazon.co.uk', 'http://www.diply.com', 'http://www.coccoc.com', 'http://www.cnn.com', 'http://www.bbc.co.uk', 'http://www.twitch.tv', 'http://www.wikia.com', 'http://www.google.co.th', 'http://www.go.com', 'http://www.google.com.ph', 'http://www.doubleclick.net', 'http://www.onet.pl', 'http://www.googleadservices.com', 'http://www.accuweather.com', 'http://www.googleweblight.com', 'http://www.answers.yahoo.com']

# Creates Firefox Driver, had issues with Chrome
def createDriver():
    FirefoxOptions = webdriver.FirefoxOptions()

    # All options to optimize selenium processing
    FirefoxOptions.add_argument("--headless") # Runs without opening any windows
    FirefoxOptions.add_argument('--ignore-certificate-errors')
    FirefoxOptions.add_argument('--incognito')
    FirefoxOptions.add_argument('--no-sandbox')
    FirefoxOptions.add_argument('--enable-automation')
    FirefoxOptions.add_argument('--disable-gpu')
    FirefoxOptions.add_argument('--disable-infobars')
    FirefoxOptions.add_argument('--disable-browser-side-navigation')
    FirefoxOptions.add_argument('--disable-dev-shm-usage')
    FirefoxOptions.add_argument('--disable-features=VizDisplayCompositor')
    FirefoxOptions.add_argument('--dns-prefetch-disable')

    driver = webdriver.Firefox(options=FirefoxOptions)
    driver.set_page_load_timeout(30)
    driver.maximize_window()

    return driver

# Screenshots and saves to "images" folder
def getScreenshot(url):  
    # Driver is created per thread. Selenium is thread-safe usually,
    #   but the flow of the program allows explicit thread-safety
    driver = createDriver()
    try:
        driver.get(url)

        # Specifying dimensions of the screenshot
        width = 2560
        height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(width, height)

        # Filename is the URL, cleaned up so that it can be saved properly
        filename = re.sub(r'[^a-zA-Z0-9]', '_', url) + '.png'
        driver.save_screenshot("./images/" + filename)
        
        # Ensuring that there aren't rapid calls to the function
        time.sleep(0.1)
        logging.info(f"Screenshot saved from {url}")
    except TimeoutException as e:
        logging.error(f"TimeoutException for URL {url} - {e}")
    finally:
        driver.quit()

# ------------------------------------------------ #
#     Running 100 times takes around 7 mins
#     - Play around with the range

#   what the timings are for yourself
# for _ in range(100):
#     getScreenshot(driver, url)
# ------------------------------------------------ #

# ------------------------------------------------ #
#                  Multithreading 
# Up to 10,000 screenshots can be done at one time
# ------------------------------------------------ #
numThreads = 10

# Use ThreadPoolExecutor to manage fixed number of threads
with ThreadPoolExecutor(max_workers=numThreads) as executor:
    # Submit each URL to executor
    # Set up as a key-value pair to have threads execute unique URLs
    if (len(urls) <= 10000):
        futures = {executor.submit(getScreenshot, url): url for url in urls}
    else:
        logging.error(f"Too Many URLS! Amount of URLs={len(urls)}")

print("Time: ", time.time() - start_time)