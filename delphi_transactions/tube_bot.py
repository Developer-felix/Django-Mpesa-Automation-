
from selenium import webdriver
import time
from random import randrange

refresh_time = 20000000
browser_list = []

browser_one = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")

browser_list.append(browser_one)

videos = [
    'https://www.youtube.com/watch?v=bElhxzQweYQ'
]
random_video = random.randint(0,1)
for i in range(1000):
    print("Running the video for {} time",formatZ(i))
    browser_one.get(videos[random_video])
    sleep_time = random.randint(10,20)
    time.sleep(sleep_time)

driver.quit()

# for browser in browser_list:
#     browser.get("https://www.youtube.com/watch?v=bElhxzQweYQ")

# while(True):
#      browser_num = randrange(0, len(browser_list))
#      browser_list[browser_num].refresh()
#      print("browser number", browser_num, "refreshed")
#      time.sleep(refresh_time)
      
# browser.close()

