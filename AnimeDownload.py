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
    basePage = 'https://www.watchcartoononline.io/anime/sword-art-online'
    page = requests.get(basePage)
    tree = html.fromstring(page.content)
    episodeUrlLists = tree.xpath('//a[@class="sonra"]/@href')
    for link in episodeUrlLists:
        print link
    # p = requests.get(episodeUrlLists[2])
    # t = html.fromstring(p.content)
    # ele = t.xpath('//*[@id="reklam_kapat"]')
    # display = Display(visible=0, size=(800, 600))
    # display.start()
    driver = webdriver.Chrome('C:\Program Files (x86)\Google\WebDriver\chromedriver.exe')
    # chromeOptions = Options()
    # chromeOptions.add_argument('--headless')
    driver.get(episodeUrlLists[2])
    tags = driver.find_elements_by_tag_name('a')
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