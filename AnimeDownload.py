from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from sortedcontainers import SortedSet
import Constants
import os
import os.path
from tqdm import tqdm
import requests
import math


def resolve_hyphenated_range(hyphen_str):
    resolved_list = SortedSet()
    ep_str_hyphen_split = hyphen_str.split('-')
    ep_hyphen_0, ep_hyphen_1 = ep_str_hyphen_split[0].strip(), ep_str_hyphen_split[1].strip()
    if ep_hyphen_0.isdigit() and ep_hyphen_1.isdigit():
        for eps in range(int(ep_hyphen_0), int(ep_hyphen_1) + 1):
            resolved_list.add(eps)
    return resolved_list


def resolve_episode_list(str_list):
    episodes_to_download = SortedSet()
    episodes_split = str_list.strip().split(',')
    for i in range(len(episodes_split)):
        ep_str = episodes_split[i].strip()
        if ep_str.isdigit():
            episodes_to_download.add(int(ep_str))
        else:
            hyp = resolve_hyphenated_range(ep_str)
            episodes_to_download = episodes_to_download.union(hyp)
    return episodes_to_download


def get_episode_listing(web_driver, url_to_navigate, xpath_to_search, episodes_to_download):
    web_driver.get(url_to_navigate)
    episode_list_web_ids = web_driver.find_elements_by_xpath(xpath_to_search)
    web_episode_dict = {}
    for episode in episode_list_web_ids:
        soup = BeautifulSoup(episode.get_attribute('innerHTML'))
        anchor_element = soup.find('a', href=True)
        if anchor_element:
            anchor_title = anchor_element['title']
            anchor_href_url = anchor_element['href']
            for episode_to_download in episodes_to_download:
                if str(episode_to_download) in anchor_title:
                    web_episode_dict[episode_to_download] = anchor_href_url
                    episodes_to_download.remove(episode_to_download)
                    break
        if not episodes_to_download:
            break
    return web_episode_dict


def resolve_iframe(web_driver, frame, video_elem_xpath):
    src = ''
    web_driver.switch_to_frame(frame)
    video_elem = web_driver.find_element_by_xpath(video_elem_xpath)
    if video_elem:
        soup = BeautifulSoup(video_elem.get_attribute('outerHTML'))
        video_src_element = soup.find('source')
        if video_src_element:
            src = str(video_src_element['src'])
    web_driver.switch_to_default_content()
    return src


def resolve_actual_urls_and_download(web_driver, web_episode_dict):
    success_list, failed_list = [], []
    for ep_no, url in web_episode_dict.iteritems():
        src = ''
        web_driver.get(url)
        frame = web_driver.find_element_by_id(Constants.IFRAME_ID)
        if not frame:
            all_frames = web_driver.find_elements_by_tag_name('iframe')
            if all_frames:
                for iframe in all_frames:
                    # web_driver.switch_to_frame(frame)
                    src = resolve_iframe(web_driver, iframe, Constants.VIDEO_ELEM_XPATH)
                    # web_driver.switch_to.defaultContent()
        else:
            src = resolve_iframe(web_driver, frame, Constants.VIDEO_ELEM_XPATH)
        if src:
            dst_file_name = Constants.SAVE_FORMAT.format(ep_no=str(ep_no))
            success = download_and_save_file(src, dst_file_name)
            if success:
                success_list.append(ep_no)
            else:
                failed_list.append(ep_no)
    return success_list, failed_list


def download_and_save_file(src_url, file_name):
    success = False
    if not os.path.exists(Constants.SAVE_LOCATION):
        os.makedirs(Constants.SAVE_LOCATION)
    dst_file = os.path.join(Constants.SAVE_LOCATION, file_name)
    r = requests.get(src_url, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    wrote = 0
    with open(dst_file, 'wb') as f:
        for data in tqdm(r.iter_content(Constants.BUFFER_SIZE), total=math.ceil(total_size // Constants.BUFFER_SIZE),
                         unit=' KB', unit_scale=True, desc=file_name):
            wrote = wrote + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        print('ERROR while downloading file from "{url}" at "{1}"', src_url, dst_file)
    else:
        success = True
    return success


driver = webdriver.Chrome(Constants.CHROME_WEB_DRIVER_PATH)
episodes_to_download_set = resolve_episode_list(Constants.DOWNLOAD_EPISODES_NOS)
episodes_dict = get_episode_listing(driver, Constants.BASE_URL, Constants.EPISODE_LIST_XPATH, episodes_to_download_set)
success_list, failed_list = resolve_actual_urls_and_download(driver, episodes_dict)

print 'Succeeded: ', success_list
print 'Failed: ', failed_list
