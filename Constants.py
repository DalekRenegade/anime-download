# Paths
CHROME_WEB_DRIVER_PATH = r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe'

# Constant Literals
BUFFER_SIZE = 1024
STAR = '*'
HYPHEN = '-'
COMMA = ','

# HTML Elements/Attributes/Parameters
SOUP_BASE_ELEM_GET_ATTR = 'innerHTML'
SOUP_ANCHOR_ELEM_FIND_ATTR = 'a'
SOUP_VIDEO_ELEM_SRC_ATTR = 'src'

IDENTIFIER_URL = 'href'
IDENTIFIER_IFRAME = 'iframe'
REQUEST_HEADER_PARAM = 'content-length'

SCRIPT_ELEM_CLICK = "arguments[0].click();"

VIDEO_OVERLAY_PLAY_BTN_CLASS = 'vjs-big-play-button'
CSS_SELECTOR_PAUSE_BTN = '#video-js > div.vjs-control-bar > button.vjs-play-control.vjs-control.vjs-button.vjs-playing'
CSS_SELECTOR_QUALITY_BTN = '#video-js > div.vjs-control-bar > div.vjs-quality-container > button'
CSS_SELECTOR_HD_QUALITY = '#video-js > div.vjs-control-bar > div.vjs-quality-container > div > ul > li:nth-child(1) > a'

XPATH_EPISODE_LIST = '//*[@id="catlist-listview"]/ul/li'
XPATH_VIDEO_ELEM = '//*[@id="video-js_html5_api"]'
XPATH_VIDEO_ELEM_WITH_INNER_SRC = '//*[@id="video-js_html5_api"]'

# SOUP_VIDEO_ELEM_GET_ATTR = 'outerHTML'
# SOUP_VIDEO_ELEM_FIND_ATTR = 'source'
# IDENTIFIER_TITLE = 'title'
# IFRAME_ID = 'frameNewAnimeuploads0'

# Regular Expressions
REGEX_SEASON = r'Season (\d+)'
REGEX_EPISODE = r'Episode (\d+)'
