# Render Website Python
- This is a python script that will take a screenshot of at least 2500px width (more realistically the whole webpage) and save it locally. 1000s of URLs (Max 10,000) can be used at 1 time for the script, although it is untested due to personal limitations.
- Screenshots are named with the URL of the website.
  - Example: A screenshot of https:://google.com will become https:__google_com.

# How does the program work?
- There is a `websites.py` file that contains the top 1000 websites (alot of these websites cause a TimeoutException and I cannot audit all of them). You can add more or less websites to the file as needed.
- `main.py` will process all of the websites within `websites.py`.
- Using multi-threading (`ThreadPoolExecutor`) and Selenium, websites are processed at around 10 threads at a time. 1 thread takes roughly 1 second to process 
  - NOTE: Only in the most ideal circumstances. Hardware limitations and long processing times can cause delays within the program.
- The screenshots are saved within the "images" folder.

# To run the program, you MUST have:
1. Selenium
2. Enough time, disk space and RAM space

# Timings 
- Based on the specifications and timings below, you can calculate how long it would take to run given the amount of URLs

## Specs
- Intel i7 13700KF: Around 40% of processor was used
- 2GB of RAM (at the least ONLY for this program)

## Run 1: Running 100 URLs with a for loop
- Using the `getScreenshot()` function in a for loop 100 times, the program runs for approxiamately 7 minutes.

## Run 2: Running 100 URLs (5 Threads)
- Using `ThreadPoolExecutor` and 5 Threads, the program runs for almost exactly 5 minutes (299 seconds)

## Run 3: Running 100 URLs (10 Threads)
- Using `ThreadPoolExecutor` and 10 Threads, the program runs almost half of Run 2's runtime (159 seconds, expected)

## Run 4: Running 1000 URLs (10 Threads)
- Using `ThreadPoolExecutor` and 10 Threads, the program runs completes in roughly 38 minutes (2326.384374141693 seconds)
### NOTE: Runtimes above differ due to threads waiting for 30 seconds to see if a link will work. If not, a TimeoutException occurs

## Run 5 (THEORETICAL): Running 10,000 URLs (10 Threads)
- Given the amount of screenshots saved in my personal run with 1000 URLs, only 76.4% of websites were screenshotted due to TimeoutExceptions from the other websites. Assuming the equations are conceptually correct:
  - Error Time = (30 seconds * (10,000 links * 24.6% errors)) = 73,800 seconds
  - Success Time = (1 second per thread + (2 seconds after all 10 threads complete / every 10 threads)) * (10,000 links * 76.4% success rate) = 9,168 seconds
  - Error time + Success time = 82,968 seconds = 23:02:48 (almost 1 whole day)

# Limitations & Constraints
- The program should be able to run 10,000 URLs at one time however, I have only tested 1000 URLs in one run.
- The program may be able to do more, but a hard limit is set within the `ThreadPoolManager` executor. You may change it at your own risk.
- All website links must have `https://` prepended to the link. It will be prepended automatically when you add a website to the list in websites.py as long as it is ran before main.py.
- Lastly, 

### NOTE: The program will hang near the end, presumably to clean up all of the threads.

# Errors
- Errors are outputted using the built-in Python Logging API.

### 1. The website does not exist
    - A TimeoutException/RemoteError/WebDriverError will occur. A thread will wait up to 30 seconds and if it does not find the website, it will move onto the next one.
    
### 2. The website exists, but 4**/5** errors occur
    - Check the link to the website that causes it. It will most likely be true that the website link does not actually exist, either due to client or server problems. 
    - If not, it may be due to the Firefox Options at the top of `main.py`. Comment, Uncomment, add or remove any tags you would like.
    - NOTE: If this occurs, a screenshot will still be taken of the website, as most websites will have a 4**/5** errors displayed if the link doesn't exist within the website.

### 3. A blank or empty  or almost-empty screenshot is saved. 
    - This could be due to the websites' own limitations. For example, screenshotting YouTube (to the best of my understanding) will produce a blank screen without any videos.