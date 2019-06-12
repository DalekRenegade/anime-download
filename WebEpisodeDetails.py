import Constants
import FileOps
import HelperFunctions
import Logger
import os
import os.path
from CaseInsensitiveDict import CaseInsensitiveDict
from Enums import StatusTypeEnum, AnimeCategoryEnum


class WebEpisodeDetails:
    def __init__(self, element, web_driver):
        self.Element = element
        self.WebDriver = web_driver
        self.EpisodeURL = None
        self.ResolvedURL = None
        self.DownloadURL = None
        self.ServersDownloadURLs = None
        self.DestinationFileName = None
        self.IndexFraction = ''
        self.Title = ''
        self.Season = 0
        self.EpisodeNo = 0
        self.DownloadStatus = StatusTypeEnum.DOWNLOAD_PENDING
        self.EpisodeCategory = AnimeCategoryEnum.NONE

    def updateIndexFraction(self, index, total):
        self.IndexFraction = ' ({numerator}/{denominator}) '.format(numerator=index, denominator=total)

    def extractDetailsFromHtmlElement(self):
        if self.Element:
            self.EpisodeURL = self.Element[Constants.IDF_HREF].strip()
            episode_text = self.Element.find(Constants.IDF_DIV).text.strip().replace('EP', '')
            if episode_text.isdigit():
                self.EpisodeNo = int(episode_text)
            else:
                try:
                    self.EpisodeNo = float(episode_text)
                except Exception:
                    self.EpisodeNo = episode_text
            category = self.Element.find('div', {'class': 'cate'})
            if category:
                self.EpisodeCategory = AnimeCategoryEnum.translateToEnum(category.text)

    def navigateToResolvedURL(self):
        while self.WebDriver.current_url != self.ResolvedURL:
            self.WebDriver.execute_script(Constants.SCRIPT_GO_BACK)

    def getDownloadLinks(self):
        self.ServersDownloadURLs = CaseInsensitiveDict()
        try:
            self.WebDriver.get(Constants.BASE_URL + self.EpisodeURL)
            self.Title = self.WebDriver.find_element_by_class_name(Constants.CLASS_DIV_TITLE).text
            self.Title = HelperFunctions.transformFileName(self.Title)
            download_div_master = self.WebDriver.find_element_by_class_name(Constants.CLASS_DIV_DOWNLOAD_ANIME)
            anchor_elem = HelperFunctions.findAnchorElementHref(download_div_master)
            self.ResolvedURL = anchor_elem[Constants.IDF_HREF].strip()
            self.WebDriver.get(self.ResolvedURL)
            download_div_links = self.WebDriver.find_elements_by_class_name(Constants.CLASS_DIV_DOWNLOAD_VIA_SERVER)

            for download_link in download_div_links:
                download_anchor = HelperFunctions.findAnchorElementHref(download_link)
                server = Constants.REGEX_REPLACE_DOWNLOAD.sub('', download_anchor.text).strip().strip('\n').strip()
                if server not in self.ServersDownloadURLs:
                    self.ServersDownloadURLs[server] = []
                self.ServersDownloadURLs[server].append(download_link)
        except Exception, e:
            print e

    def download(self, server_list, anime_directory, series_name):
        episode_vid_quality_url_map = {}
        for server in server_list:
            if server.ServerName not in self.ServersDownloadURLs:
                continue
            for server_link in self.ServersDownloadURLs[server.ServerName]:
                try:
                    HelperFunctions.closeWindows(self.WebDriver)
                    self.navigateToResolvedURL()
                    anchor = server_link.find_element_by_tag_name(Constants.IDF_ANCHOR)
                    url = anchor.get_attribute(Constants.IDF_HREF)
                    self.WebDriver.execute_script(Constants.SCRIPT_ELEM_CLICK, anchor)
                    server_vid_quality_url_map = server.navigateServer(self.WebDriver, url)
                    if server_vid_quality_url_map:
                        for quality, url in server_vid_quality_url_map.iteritems():
                            if quality not in episode_vid_quality_url_map:
                                episode_vid_quality_url_map[quality] = []
                            episode_vid_quality_url_map[quality].append(url)
                    self.WebDriver.switch_to_window(self.WebDriver.window_handles[0])
                except Exception, ex:
                    Logger.addExceptionLog(ex.message, __name__)
        self.DownloadStatus = StatusTypeEnum.DOWNLOAD_PENDING
        sorted_keys = sorted(episode_vid_quality_url_map.keys(), reverse=True)
        for key in sorted_keys:
            for url in episode_vid_quality_url_map[key]:
                self.DownloadStatus = self.downloadAndSaveFile(url, anime_directory, series_name)
                if self.DownloadStatus == StatusTypeEnum.DOWNLOAD_SUCCESS:
                    HelperFunctions.closeWindows(self.WebDriver)
                    break
            if self.DownloadStatus == StatusTypeEnum.DOWNLOAD_SUCCESS:
                break

    def downloadAndSaveFile(self, url, anime_directory, series_name):
        self.DestinationFileName = Constants.SAVE_FORMAT.format(name=series_name, ep_no=str(self.EpisodeNo))
        destination_file_path = os.path.join(anime_directory, self.DestinationFileName)
        status = FileOps.downloadFileFromUrl(url, destination_file_path, self.DestinationFileName + self.IndexFraction)
        if status != StatusTypeEnum.DOWNLOAD_SUCCESS:
            Logger.addLogToCL('ERROR while downloading file from "{0}" at "{1}"'.format(url, destination_file_path))
        return status

    def __str__(self):
        return self.Title
