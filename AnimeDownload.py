import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sortedcontainers import SortedDict

import CommandLineInterop
import FileOps
from AnimeInfo import AnimeInfo
from Enums import InputCategoryEnum, AiringStatusEnum
from Servers import *


def fetchListedServers():
    try:
        list_servers_from_file = FileOps.readFromJsonFile(json_file_name=Constants.FILE_SERVER_LIST,
                                                          json_root_key=Constants.SERVER_LIST_JSON_ROOT_KEY,
                                                          sort_key=Constants.SortKeys.SORT_KEY_SERVER_LIST,
                                                          return_named_tuple=False)
        server_object_list = []
        for server_from_file in list_servers_from_file:
            server_name = server_from_file[Constants.TEXT_SERVER].strip().replace(' ', '_')
            if server_from_file[Constants.TEXT_ENABLED] and server_name in globals():
                server = globals()[server_name](server_from_file)
                server_object_list.append(server)
        server_object_list.sort(key=Constants.SortKeys.SORT_KEY_SERVER_OBJECT_LIST, reverse=True)
        if not server_object_list:
            Logger.addLogToCL('Server list not found! Exiting...')
            Logger.addInfoLog('Server list not found! Execution terminated...', src=__name__)
            sys.exit(1)
    except Exception, ex:
        Logger.addExceptionLog(ex.message, __name__)
        Logger.addLogToCL(ex.message, __name__)
        sys.exit(1)
    return server_object_list


def fetchListedAnimes():
    try:
        anime_list = FileOps.readFromJsonFile(json_file_name=Constants.FILE_ANIME_LIST,
                                              json_root_key=Constants.ANIME_LIST_JSON_ROOT_KEY,
                                              sort_key=Constants.SortKeys.SORT_KEY_ANIME_LIST)
        anime_dict = HelperFunctions.listToDict(anime_list, Constants.TEXT_ID, SortedDict())
        anime_url_list = set()
        for key in anime_dict.keys():
            prev_len = len(anime_url_list)
            anime_url_list.add(anime_dict[key].url)
            if prev_len == len(anime_url_list):
                anime_dict.pop(key, None)
        if not anime_dict:
            Logger.addLogToCL('Anime list not found! Exiting...')
            Logger.addInfoLog('Anime list not found! Execution Terminated...', __name__)
            sys.exit(1)
    except Exception, ex:
        Logger.addExceptionLog(ex.message, __name__)
        Logger.addLogToCL(ex.message, __name__)
        sys.exit(1)
    return anime_dict, list(anime_url_list)


if __name__ == '__main__':
    driver = None
    try:
        server_object_list = fetchListedServers()
        anime_dict, anime_url_list = fetchListedAnimes()
        anime_input_params = CommandLineInterop.extractParametersFromArgv(sys.argv[1:], anime_dict)
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--log-level=3")
        driver = webdriver.Chrome(Constants.CHROME_WEB_DRIVER_PATH, chrome_options=options)
        driver.set_window_position(-2000, 0)
        by_id = anime_input_params.InputCategory == InputCategoryEnum.ID

        for idx, input_anime in enumerate(anime_input_params.AnimeReference):
            url = anime_dict[input_anime].url if by_id else input_anime
            Logger.addLogToCL('Processing {0} of {1}...'.format(idx + 1, len(anime_input_params.AnimeReference)),
                              new_line=False)
            if anime_input_params.Episodes:
                episodes = anime_input_params.Episodes
            else:
                episodes = anime_dict[input_anime].episodes + Constants.RANGE_EXCLUDE
            anime = AnimeInfo(web_driver=driver, url=url, id=input_anime if by_id else 0,
                              anime_category=anime_dict[input_anime].category if by_id else None)

            if not anime.fetchAnimeInfo():
                continue
            Logger.addLogToCL('{0} ...'.format(anime.SeriesName), new_line=False)
            if not anime.fetchAnimeEpisodesList():
                Logger.addLogToCL('Error. No episode list...')
                continue
            if (anime_input_params.AddNewAnime or (anime.AiringStatus == AiringStatusEnum.ONGOING and anime.ID == 0)) \
                    and anime.URL not in anime_url_list:
                anime.identifyCategory()
                anime.addAsNewAnime()
            if anime.identifyEpisodesToDownload(episodes):
                Logger.addLogToCL('Identified {0} episodes. Downloading...'.format(len(anime.DownloadEpisodeList)))
                downloaded, failed = anime.downloadEpisodes(server_object_list)
                if failed:
                    Logger.addLogToCL('\nFailed to download the following from {name}{id}: {eps}\n'
                                      .format(name=anime.SeriesName, eps=failed,
                                              id='(id = {0})'.format(anime.ID) if anime.ID > 0 else ''))
                anime.updateJson(downloaded)
            else:
                Logger.addLogToCL('Skipped. Nothing to download.')
            anime.cleanupDirectory()
    except Exception, ex:
        Logger.addExceptionLog(ex.message, __name__)
    finally:
        if driver:
            driver.quit()
    print 'Completed...'
