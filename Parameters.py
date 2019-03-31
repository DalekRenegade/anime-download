import os
import AnimeList
from os.path import expanduser
from Enums import DownloadTypeEnum

# BASE_URL = 'https://www.watchcartoononline.io/anime/gintama-2015'
BASE_URL = AnimeList.SOA_3
SERIES_NAME = 'SOA3'

TYPE_OF_DOWNLOAD = DownloadTypeEnum.ALL

USE_CUSTOM_SAVE_LOCATION = True

DOWNLOAD_TITLES = ['']
DOWNLOAD_EPISODES_NOS = '3,8,11,15,18,20,21,23'
DOWNLOAD_SEASON_EPISODE = {1: '*', 2: '*'}

USER_HOME = expanduser("~")
CUSTOM_SAVE_LOCATION = os.path.join('D:/Downloads/', SERIES_NAME)
DEFAULT_SAVE_LOCATION = os.path.join(USER_HOME, 'Videos', SERIES_NAME)
if USE_CUSTOM_SAVE_LOCATION:
    SAVE_LOCATION = CUSTOM_SAVE_LOCATION
else:
    SAVE_LOCATION = DEFAULT_SAVE_LOCATION

if TYPE_OF_DOWNLOAD == DownloadTypeEnum.ALL:
    SAVE_FORMAT = '{title}.mp4'
elif TYPE_OF_DOWNLOAD == DownloadTypeEnum.BY_SEASON:
    SAVE_FORMAT = SERIES_NAME + ' - Season {s_no} Episode {ep_no}.mp4'
elif TYPE_OF_DOWNLOAD == DownloadTypeEnum.BY_EPISODE:
    SAVE_FORMAT = SERIES_NAME + ' - {ep_no}.mp4'
else:
    SAVE_FORMAT = '{title}.mp4'
