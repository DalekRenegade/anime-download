import json

import Constants
import FileOps
import HelperFunctions
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Logger
from Enums import DownloadByEnum, StatusTypeEnum, AnimeCategoryEnum, AiringStatusEnum
from WebEpisodeDetails import WebEpisodeDetails


class AnimeInfo:
    def __init__(self, web_driver, url, id=0, series_name='', anime_category=AnimeCategoryEnum.NONE):
        self.WebDriver = web_driver
        self.ID = id
        self.URL = url
        self.DownloadEpisodeList = []
        self.WebEpisodeList = []
        self.SeriesName = series_name
        self.ReleaseYear = 0
        self.AnimeDirectory = ''
        self.AiringStatus = ''
        self.AnimeCategory = anime_category if anime_category else AnimeCategoryEnum.NONE

    def createDirectory(self):
        series_name_with_year = '{name} ({year})'.format(name=self.SeriesName, year=self.ReleaseYear)
        if Constants.USE_CUSTOM_SAVE_LOCATION:
            self.AnimeDirectory = os.path.join(Constants.CUSTOM_SAVE_LOCATION_BASE_DIR, series_name_with_year)
        else:
            self.AnimeDirectory = os.path.join(Constants.USER_DIR_VIDEOS, series_name_with_year)
        if not os.path.exists(self.AnimeDirectory):
            os.makedirs(self.AnimeDirectory)

    def fetchAnimeInfo(self):
        try:
            self.WebDriver.get(self.URL)
            anime_info_div = self.WebDriver.find_element_by_class_name(Constants.CLASS_DIV_ANIME_NAME)
            series_name = anime_info_div.find_element_by_tag_name(Constants.IDF_H1).text
            if not self.SeriesName:
                self.SeriesName = HelperFunctions.transformFileName(series_name)
            anime_details = anime_info_div.find_elements_by_class_name(Constants.CLASS_P_ANIME_DETAILS)

            for anime_detail in anime_details:
                text = anime_detail.text.strip().lower()
                if Constants.TEXT_RELEASED in text:
                    self.ReleaseYear = HelperFunctions.extractNumbersFromString(text)
                elif Constants.TEXT_STATUS in text:
                    self.AiringStatus = AiringStatusEnum.translateToEnum(text.split(':')[1])
            return True
        except Exception, ex:
            Logger.addExceptionLog(str(ex.__class__) + ex.message, __name__)
        return False

    def fetchAnimeEpisodesList(self):
        try:
            self.WebEpisodeList = []
            episode_pages = self.WebDriver.find_element_by_id(Constants.ELEM_ID_UL_EPS_PAGE)\
                .find_elements_by_tag_name(Constants.IDF_ANCHOR)
            for ep_page in episode_pages:
                self.WebDriver.execute_script(Constants.SCRIPT_ELEM_CLICK, ep_page)
                related_eps = WebDriverWait(self.WebDriver, Constants.SLEEP_TIME_LONG).until(
                    EC.presence_of_element_located((By.ID, Constants.ELEM_ID_UL_EPS_LIST))
                )
                videos_web_list = related_eps.find_elements_by_tag_name(Constants.IDF_LI)
                for episode in videos_web_list:
                    anchor_element = HelperFunctions.findAnchorElementHref(episode)
                    if anchor_element:
                        web_ep = WebEpisodeDetails(anchor_element, self.WebDriver)
                        web_ep.extractDetailsFromHtmlElement()
                        self.WebEpisodeList.append(web_ep)

            self.WebEpisodeList.sort(key=lambda k: (k.EpisodeNo, k.Title))
            self.createDirectory()
            return True
        except Exception, ex:
            Logger.addExceptionLog(str(ex.__class__) + ex.message, __name__)
        return False

    def identifyCategory(self):
        if self.AnimeCategory == AnimeCategoryEnum.NONE:
            subbed_count, dubbed_count = 0, 0
            for x in self.WebEpisodeList:
                if x.EpisodeCategory == AnimeCategoryEnum.SUBBED:
                    subbed_count += 1
                elif x.EpisodeCategory == AnimeCategoryEnum.DUBBED:
                    dubbed_count += 1
            if subbed_count > 0 and dubbed_count > 0:
                self.AnimeCategory = AnimeCategoryEnum.COMBINED
            elif subbed_count > 0:
                self.AnimeCategory = AnimeCategoryEnum.SUBBED
            elif dubbed_count > 0:
                self.AnimeCategory = AnimeCategoryEnum.DUBBED

    def identifyEpisodesToDownload(self, download_episode_nos):
        self.DownloadEpisodeList = []

        if download_episode_nos == Constants.DOWNLOAD_ALL:
            for web_episode in self.WebEpisodeList:
                self.DownloadEpisodeList.append(web_episode)
        else:
            episodes_to_download = HelperFunctions.resolveEpisodes2Dict(download_episode_nos)

            for web_episode in self.WebEpisodeList:
                for category, ep_val in episodes_to_download.items():
                    if (category == DownloadByEnum.EXACT and web_episode.EpisodeNo in ep_val) \
                            or (category == DownloadByEnum.RANGE_LESS_THAN and web_episode.EpisodeNo < ep_val) \
                            or (category == DownloadByEnum.RANGE_GREATER_THAN and web_episode.EpisodeNo > ep_val):
                        self.DownloadEpisodeList.append(web_episode)
                        break
                    if category == DownloadByEnum.RANGE_BETWEEN:
                        for ep_range in ep_val:
                            if ep_range[0] <= web_episode.EpisodeNo <= ep_range[1]:
                                self.DownloadEpisodeList.append(web_episode)
                                break
        return len(self.DownloadEpisodeList) > 0

    def downloadEpisodes(self, server_list):
        total_episodes = len(self.DownloadEpisodeList)
        downloaded, failed = [], []
        for idx, web_episode in enumerate(self.DownloadEpisodeList):
            web_episode.updateIndexFraction(idx + 1, total_episodes)
            web_episode.getDownloadLinks()
            web_episode.download(server_list, self.AnimeDirectory, self.SeriesName)
            if web_episode.DownloadStatus == StatusTypeEnum.DOWNLOAD_SUCCESS:
                downloaded.append(web_episode.EpisodeNo)
            else:
                failed.append(web_episode.EpisodeNo)
        return downloaded, failed

    def updateJson(self, episodes):
        if episodes:
            content = FileOps.readFile(file_name=Constants.FILE_ANIME_LIST, is_json=True)
            for idx in range(len(content[Constants.ANIME_LIST_JSON_ROOT_KEY])):
                if content[Constants.ANIME_LIST_JSON_ROOT_KEY][idx][Constants.TEXT_ID] == self.ID:
                    num, flag = HelperFunctions.parse_string_to_number(content[Constants.ANIME_LIST_JSON_ROOT_KEY]
                                                                       [idx][Constants.TEXT_EPISODES])
                    if flag:
                        episodes.append(num)
                    content[Constants.ANIME_LIST_JSON_ROOT_KEY][idx][Constants.TEXT_EPISODES] = str(max(episodes))
                    break
            FileOps.writeFile(file_name=Constants.FILE_ANIME_LIST, data=content, is_json=True)

    def addAsNewAnime(self):
        content = FileOps.readFile(file_name=Constants.FILE_ANIME_LIST, is_json=True)
        self.ID = max([x[Constants.TEXT_ID] for x in content[Constants.ANIME_LIST_JSON_ROOT_KEY]]) + 1
        new_entry = Constants.NEW_ANIME_FORMAT.format(cat=self.AnimeCategory.name, url=self.URL,
                                                      ep=Constants.DOWNLOAD_ALL, id=self.ID, name=self.SeriesName)
        content[Constants.ANIME_LIST_JSON_ROOT_KEY].append(json.loads(new_entry))
        FileOps.writeFile(file_name=Constants.FILE_ANIME_LIST, data=content, is_json=True)

    def cleanupDirectory(self):
        if len(os.listdir(self.AnimeDirectory)) == 0:
            os.rmdir(self.AnimeDirectory)

    def __str__(self):
        return self.SeriesName if self.SeriesName else self.URL
