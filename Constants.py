import os
import re
from collections import OrderedDict
from os.path import expanduser


CHROME_WEB_DRIVER_PATH = r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe'
CUSTOM_SAVE_LOCATION_BASE_DIR = 'D:/Downloads/'
USER_DIR_HOME = expanduser("~")
USER_DIR_VIDEOS = os.path.join(USER_DIR_HOME, 'Videos')
SAVE_FORMAT = '{name} - {ep_no}.mp4'
USE_CUSTOM_SAVE_LOCATION = True

MIN_VIDEO_SIZE = 1000000    # 1 MB
SLEEP_TIME_SHORT = 2
SLEEP_TIME_LONG = 10
BUFFER_SIZE = 1024
RANGE_EXCLUDE = '>'

BASE_URL = 'https://www5.gogoanime.tv'
REQUEST_HEADER_PARAM = 'content-length'

ARGS_HELP_TEXT = OrderedDict({
        'DOWNLOAD BY IDS  :': 'python AnimeDownload.py -i <anime_ids> [-e <episodes>]',
        'DOWNLOAD BY URL  :': 'python AnimeDownload.py -u <url> [-e <episodes>]',
        'LIST ANIMES      :': 'python AnimeDownload.py -l [<a/all/d/dub/dubbed/s/sub/subbed>]'
    })

TEXT_CATEGORY = 'category'
TEXT_ENABLED = 'enabled'
TEXT_EPISODES = 'episodes'
TEXT_ID = 'id'
TEXT_PRIORITY = 'priority'
TEXT_RELEASED = 'released'
TEXT_SERVER = 'server'
TEXT_STATUS = 'status'
TEXT_VIDEO = 'video'

DOWNLOAD_ALL = '*'

FILE_SERVER_LIST = 'ServerList.json'
FILE_ANIME_LIST = 'AnimeList.json'

SERVER_LIST_JSON_ROOT_KEY = 'server_list'
ANIME_LIST_JSON_ROOT_KEY = 'anime_list'

NEW_ANIME_FORMAT = '{{"category": "{cat}", "url": "{url}", "episodes": "{ep}", "id": {id}, "name": "{name}"}}'

class SortKeys:
    SORT_KEY_SERVER_OBJECT_LIST = staticmethod(lambda k: (k.Priority, k.ServerName))
    SORT_KEY_ANIME_LIST = staticmethod(lambda k: k[TEXT_ID])
    SORT_KEY_SERVER_LIST = staticmethod(lambda k: (k[TEXT_PRIORITY], k[TEXT_SERVER]))

REGEX_REPLACE_DOWNLOAD = re.compile(re.escape('DOWNLOAD'), re.IGNORECASE)

ELEM_ID_COUNTDOWN = 'countdown'
ELEM_ID_DOWNLOAD = 'download'
ELEM_ID_UL_EPS_LIST = 'episode_related'
ELEM_ID_UL_EPS_PAGE = 'episode_page'

CLASS_DIV_ANIME_NAME = 'anime_info_body_bg'
CLASS_DIV_DOWNLOAD_ANIME = 'download-anime'
CLASS_DIV_DOWNLOAD_VIA_SERVER = 'dowload'

CLASS_BTN_LOADING = 'is-loading'
CLASS_DIV_TITLE = 'title_name'
CLASS_P_ANIME_DETAILS = 'type'
CLASS_P_DOWNLOAD = 'control'

SCRIPT_ELEM_CLICK = "arguments[0].click();"
SCRIPT_GO_BACK = "window.history.go(-1);"
SCRIPT_GO_FORWARD = "window.history.go(1);"

IDF_ANCHOR = 'a'
IDF_DIV = 'div'
IDF_H1 = 'h1'
IDF_HREF = 'href'
IDF_INNER_HTML = 'innerHTML'
IDF_LI = 'li'
IDF_TEXT_CONTENT = 'textContent'
IDF_UL = 'UL'
