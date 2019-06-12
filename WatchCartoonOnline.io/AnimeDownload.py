from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from sortedcontainers import SortedSet, SortedDict

from WebEpisodeDetails import WebEpisodeDetails
from Enums import DownloadTypeEnum, StatusTypeEnum
import Constants
import Parameters


def resolve_hyphenated_range(hyphen_str):
    resolved_list = SortedSet()
    ep_str_hyphen_split = hyphen_str.split(Constants.HYPHEN)
    ep_hyphen_0, ep_hyphen_1 = ep_str_hyphen_split[0].strip(), ep_str_hyphen_split[1].strip()
    if ep_hyphen_0.isdigit() and ep_hyphen_1.isdigit():
        for eps in range(int(ep_hyphen_0), int(ep_hyphen_1) + 1):
            resolved_list.add(eps)
    return resolved_list


def expand_episode_list(str_list):
    episodes_to_download = SortedSet()
    episodes_split = str_list.strip().split(Constants.COMMA)
    for i in range(len(episodes_split)):
        ep_str = episodes_split[i].strip()
        if ep_str.isdigit():
            episodes_to_download.add(int(ep_str))
        else:
            hyp = resolve_hyphenated_range(ep_str)
            episodes_to_download = episodes_to_download.union(hyp)
    return episodes_to_download


def resolve_season_episode(dict_season_episode):
    resolved_listing = SortedDict()
    for season, episodes in dict_season_episode.values():
        if Constants.STAR in episodes:
            resolved_listing[season] = Constants.STAR
        else:
            resolved_listing[season] = expand_episode_list(episodes)
    return resolved_listing


def get_web_episode_listing(web_driver, url_to_navigate, xpath_to_search):
    web_driver.get(url_to_navigate)
    videos_web = web_driver.find_elements_by_xpath(xpath_to_search)
    web_episode_list = []

    for episode in videos_web:
        soup = BeautifulSoup(episode.get_attribute(Constants.SOUP_BASE_ELEM_GET_ATTR))
        anchor_element = soup.find(Constants.SOUP_ANCHOR_ELEM_FIND_ATTR, href=True)
        if anchor_element:
            web_ep = WebEpisodeDetails(anchor_element)
            web_ep.extract_details_from_title()
            web_episode_list.append(web_ep)

    web_episode_list.sort(key=lambda x: (x.Season, x.Episode))
    return web_episode_list


# def resolve_iframe(web_driver, frame, video_elem_xpath):
#     src = ''
#     web_driver.switch_to_frame(frame)
#     video_elem = web_driver.find_element_by_xpath(video_elem_xpath)
#     if video_elem:
#         soup = BeautifulSoup(video_elem.get_attribute('outerHTML'))
#         video_src_element = soup.find('source')
#         if video_src_element:
#             src = str(video_src_element['src'])
#     web_driver.switch_to_default_content()
#     return src


# def resolve_actual_urls_and_download(web_driver, web_episode_dict):
#     success_list, failed_list = [], []
#     for ep_no, url in web_episode_dict.iteritems():
#         src = ''
#         web_driver.get(url)
#         frame = web_driver.find_element_by_id(Constants.IFRAME_ID)
#         if not frame:
#             all_frames = web_driver.find_elements_by_tag_name('iframe')
#             if all_frames:
#                 for iframe in all_frames:
#                     # web_driver.switch_to_frame(frame)
#                     src = resolve_iframe(web_driver, iframe, Constants.VIDEO_ELEM_XPATH)
#                     # web_driver.switch_to.defaultContent()
#         else:
#             src = resolve_iframe(web_driver, frame, Constants.VIDEO_ELEM_XPATH)
#         if src:
#             dst_file_name = Parameters.SAVE_FORMAT.format(ep_no=str(ep_no))
#             success = download_and_save_file(src, dst_file_name)
#             if success:
#                 success_list.append(ep_no)
#             else:
#                 failed_list.append(ep_no)
#     return success_list, failed_list


# def download_and_save_file(src_url, file_name):
#     success = False
#     if not os.path.exists(Constants.SAVE_LOCATION):
#         os.makedirs(Constants.SAVE_LOCATION)
#     dst_file = os.path.join(Constants.SAVE_LOCATION, file_name)
#     r = requests.get(src_url, stream=True)
#     total_size = int(r.headers.get('content-length', 0))
#     wrote = 0
#     with open(dst_file, 'wb') as f:
#         for data in tqdm(r.iter_content(Constants.BUFFER_SIZE), total=math.ceil(total_size // Constants.BUFFER_SIZE),
#                          unit=' KB', unit_scale=True, desc=file_name):
#             wrote = wrote + len(data)
#             f.write(data)
#     if total_size != 0 and wrote != total_size:
#         print('ERROR while downloading file from "{url}" at "{1}"', src_url, dst_file)
#     else:
#         success = True
#     return success


def fetch_episodes_to_download(web_driver):
    to_download_episode_list = []

    web_episode_list = get_web_episode_listing(web_driver, Parameters.BASE_URL, Constants.XPATH_EPISODE_LIST)

    if Parameters.TYPE_OF_DOWNLOAD is DownloadTypeEnum.ALL or Parameters.DOWNLOAD_EPISODES_NOS == Constants.STAR:
        for web_episode in web_episode_list:
            web_episode.Download = StatusTypeEnum.DOWNLOAD_PENDING
            to_download_episode_list.append(web_episode)

    elif Parameters.TYPE_OF_DOWNLOAD is DownloadTypeEnum.BY_SEASON:
        episodes_to_download = resolve_season_episode(Parameters.DOWNLOAD_SEASON_EPISODE)
        for web_episode in web_episode_list:
            if web_episode.Season in episodes_to_download.items():
                if episodes_to_download[web_episode.Season] == Constants.STAR:
                    web_episode.Download = StatusTypeEnum.DOWNLOAD_PENDING
                    to_download_episode_list.append(web_episode)
                elif web_episode.Episode in episodes_to_download[web_episode.Season]:
                    web_episode.Download = StatusTypeEnum.DOWNLOAD_PENDING
                    to_download_episode_list.append(web_episode)

    elif Parameters.TYPE_OF_DOWNLOAD is DownloadTypeEnum.BY_EPISODE:
        episodes_to_download = expand_episode_list(Parameters.DOWNLOAD_EPISODES_NOS)
        for web_episode in web_episode_list:
            if web_episode.Episode in episodes_to_download:
                web_episode.Download = StatusTypeEnum.DOWNLOAD_PENDING
                episodes_to_download.remove(web_episode.Episode)
                to_download_episode_list.append(web_episode)
            if not episodes_to_download:
                break

    elif Parameters.TYPE_OF_DOWNLOAD is DownloadTypeEnum.BY_TITLE:
        for web_episode in web_episode_list:
            if web_episode.Title in Parameters.DOWNLOAD_TITLES:
                web_episode.Download = StatusTypeEnum.DOWNLOAD_PENDING
                to_download_episode_list.append(web_episode)

    return to_download_episode_list


def download_episodes(to_download_episode_list, web_driver):
    for web_episode in to_download_episode_list:
        web_episode.resolve_iframe_url(web_driver)
        web_episode.download_and_save_file()
        # print web_episode.ResolvedURL, status


driver = webdriver.Chrome(Constants.CHROME_WEB_DRIVER_PATH)

web_episodes_to_download = fetch_episodes_to_download(driver)
download_episodes(web_episodes_to_download, driver)
print 'Completed...'
