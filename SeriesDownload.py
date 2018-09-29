import os
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from pyvirtualdisplay import Display
import requests

if __name__ == "__main__":
    basePage = 'http://www.todaytvseries.com/tv-series/166-brooklyn-nine-nine'
    page = requests.get(basePage)
    tree = html.fromstring(page.content)
    episodeUrlLists = tree.xpath('//a[@class="sonra"]/@href')
    for link in episodeUrlLists:
        print link

    driver = webdriver.Chrome('C:\Program Files (x86)\Google\WebDriver\chromedriver.exe')
    driver.get('http://www.todaytvseries.com/tv-series/166-brooklyn-nine-nine')
    root_ele = driver.find_element_by_xpath('//*[@id="tm-content"]/article/div/div[2]/div/div[5]/div')

    for tag in tags:
        tag_class = tag.get_attribute('class')
        if 'reklam' in tag_class:
            print tag_class
            tag.click()
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'b-reklam')))
    # ele = driver.find_element_by_xpath('//a[@class="round-buton"]')
    # ele.click()
    # # ele2 = driver.find_element_by_xpath('//*[@class="jw-video"]')
    # if ele:
    #     print ele.text
    # else:
    #     print 'ele not found'
    # if ele2:
    #     print ele2
    # else:
    #     print 'elew not found'
    # print p.content
    driver.close()
    # display.stop()