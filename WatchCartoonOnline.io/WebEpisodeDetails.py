from tqdm import tqdm
import math
import os
import os.path
import re
import requests
import Constants
import Parameters
from Enums import DownloadTypeEnum, StatusTypeEnum


class WebEpisodeDetails:
    def __init__(self, anchor_element=None):
        self.element = anchor_element
        self.Title = None
        self.BaseURL = None
        self.ResolvedURL = None
        self.DestinationFileName = None
        self.DestinationDirectory = None
        self.Season = 0
        self.Episode = 0
        self.Download = StatusTypeEnum.DOWNLOAD_SKIP
        if anchor_element:
            self.Title = anchor_element.renderContents()
            self.BaseURL = anchor_element[Constants.IDENTIFIER_URL]

    def extract_details_from_title(self):
        match = re.search(Constants.REGEX_SEASON, self.Title, re.IGNORECASE)
        if match:
            self.Season = int(match.group(1))
        match = re.search(Constants.REGEX_EPISODE, self.Title, re.IGNORECASE)
        if match:
            self.Episode = int(match.group(1))

    def resolve_iframe_url(self, web_driver=None):
        try:
            web_driver.get(self.BaseURL)
            all_frames = web_driver.find_elements_by_tag_name(Constants.IDENTIFIER_IFRAME)
            if all_frames:
                for iframe in all_frames:
                    self.ResolvedURL = self.resolve_iframe(web_driver, iframe)
                    if self.ResolvedURL:
                        break
        except Exception:
            pass

    @staticmethod
    # Private method
    def resolve_iframe(web_driver, frame):
        src = ''
        try:
            web_driver.switch_to_frame(frame)
            video_elem = web_driver.find_element_by_xpath(Constants.XPATH_VIDEO_ELEM_WITH_INNER_SRC)
            if video_elem:
                src = video_elem.get_attribute(Constants.SOUP_VIDEO_ELEM_SRC_ATTR)
                # soup = BeautifulSoup(video_elem.get_attribute(Constants.SOUP_VIDEO_ELEM_GET_ATTR))
                # video_src_element = soup.find(Constants.SOUP_VIDEO_ELEM_FIND_ATTR)
                # if video_src_element:
                #     src = str(video_src_element[Constants.SOUP_VIDEO_ELEM_SRC_ATTR])

                try:
                    all_play_buttons = web_driver.find_elements_by_class_name(Constants.VIDEO_OVERLAY_PLAY_BTN_CLASS)
                    overlay_play_button = None
                    for play_button in all_play_buttons:
                        if 'play' in play_button.text.lower():
                            overlay_play_button = play_button
                            break
                    web_driver.execute_script(Constants.SCRIPT_ELEM_CLICK, overlay_play_button)

                    pause_button = web_driver.find_element_by_css_selector(Constants.CSS_SELECTOR_PAUSE_BTN)
                    web_driver.execute_script(Constants.SCRIPT_ELEM_CLICK, pause_button)

                    quality_button = web_driver.find_element_by_css_selector(Constants.CSS_SELECTOR_QUALITY_BTN)
                    web_driver.execute_script(Constants.SCRIPT_ELEM_CLICK, quality_button)

                    hd_selector = web_driver.find_element_by_css_selector(Constants.CSS_SELECTOR_HD_QUALITY)
                    web_driver.execute_script(Constants.SCRIPT_ELEM_CLICK, hd_selector)

                    video_elem_hd = web_driver.find_element_by_xpath(Constants.XPATH_VIDEO_ELEM)
                    if video_elem_hd:
                        src = video_elem_hd.get_attribute(Constants.SOUP_VIDEO_ELEM_SRC_ATTR)

                except Exception:
                    pass
        except Exception:
            pass
        web_driver.switch_to_default_content()
        return src

    # Private method
    def resolve_save_location(self):
        if Parameters.TYPE_OF_DOWNLOAD is DownloadTypeEnum.BY_SEASON and self.Season > 0:
            self.DestinationDirectory = os.path.join(Parameters.SAVE_LOCATION, 'Season ' + str(self.Season))
        else:
            self.DestinationDirectory = Parameters.SAVE_LOCATION
        self.DestinationFileName = Parameters.SAVE_FORMAT.format(s_no=str(self.Season),
                                                                 ep_no=str(self.Episode),
                                                                 title=self.Title)
        if not os.path.exists(self.DestinationDirectory):
            os.makedirs(self.DestinationDirectory)

    def download_and_save_file(self):
        if not self.ResolvedURL:
            return StatusTypeEnum.DOWNLOAD_FAILED
        download_status = StatusTypeEnum.DOWNLOAD_STARTED
        self.resolve_save_location()

        dst_file = os.path.join(self.DestinationDirectory, self.DestinationFileName)
        r = requests.get(self.ResolvedURL, stream=True)
        total_size = int(r.headers.get(Constants.REQUEST_HEADER_PARAM, 0))
        wrote = 0
        with open(dst_file, 'wb') as f:
            for data in tqdm(r.iter_content(Constants.BUFFER_SIZE),
                             total=math.ceil(total_size // Constants.BUFFER_SIZE),
                             unit=' KB', unit_scale=True, desc=self.DestinationFileName):
                wrote = wrote + len(data)
                f.write(data)
        if total_size != 0 and wrote != total_size:
            print('ERROR while downloading file from "{url}" at "{1}"', self.ResolvedURL, dst_file)
            download_status |= StatusTypeEnum.DOWNLOAD_FAILED
        else:
            download_status = StatusTypeEnum.DOWNLOAD_SUCCESS
        return download_status

    def __str__(self):
        return self.Title
