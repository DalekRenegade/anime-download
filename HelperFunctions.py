import re
import string
from urlparse import urlparse

import requests
from sortedcontainers import SortedSet

import Constants
from Enums import DownloadByEnum


def parse_string_to_number(st):
    flag, num = False, float('nan')
    st = st.strip()
    if st.isdigit():
        num = int(st)
        flag = True
    else:
        try:
            num = float(st)
            flag = num >= 0
        except:
            pass
    return num, flag


def resolveSpecialCharSeparatedStr(eps_str):
    episodes_to_download = SortedSet()
    episodes_split = eps_str.strip().split(',')
    for i in range(len(episodes_split)):
        ep_str = episodes_split[i].strip()
        if ep_str.isdigit():
            episodes_to_download.add(int(ep_str))
        else:
            ep_str_hyphen_split = ep_str.strip().split('-')
            num1, flag1 = parse_string_to_number(ep_str_hyphen_split[0])
            num2, flag2 = parse_string_to_number(ep_str_hyphen_split[1])
            if flag1 and flag2:
                for num in range(num1, num2 + 1):
                    episodes_to_download.add(num)
            elif flag1:
                episodes_to_download.add(num1)
            elif flag2:
                episodes_to_download.add(num2)
    return episodes_to_download


def resolveHyphenatedStringRange(hyphen_str):
    resolved_list = SortedSet()
    ep_str_hyphen_split = hyphen_str.split('-')
    ep_hyphen_0, ep_hyphen_1 = ep_str_hyphen_split[0].strip(), ep_str_hyphen_split[1].strip()

    if ep_hyphen_0.isdigit() and ep_hyphen_1.isdigit():
        for eps in range(int(ep_hyphen_0), int(ep_hyphen_1) + 1):
            resolved_list.add(eps)
    elif ep_hyphen_0.isdigit() and ep_hyphen_1 == '':
        resolved_list.add(int(ep_hyphen_0))
        resolved_list.add('+')
    elif ep_hyphen_1.isdigit() and ep_hyphen_0 == '':
        for eps in range(0, int(ep_hyphen_1) + 1):
            resolved_list.add(eps)
    return resolved_list


def resolveEpisodes2Dict(eps_str):
    episodes_dict = dict()
    episodes_split = eps_str.strip().split(',')
    for ep_str in episodes_split:
        num, flag = parse_string_to_number(ep_str)
        separator_dict = dict()
        if flag:
            separator_dict[DownloadByEnum.EXACT] = SortedSet()
            separator_dict[DownloadByEnum.EXACT].add(num)
        elif '-' in ep_str:
            separator_dict = resolveSeparator2Dict(ep_str, '-')
        elif Constants.RANGE_EXCLUDE in ep_str:
            separator_dict = resolveSeparator2Dict(ep_str, Constants.RANGE_EXCLUDE, False)

        for key, val in separator_dict.items():
            if key == DownloadByEnum.RANGE_BETWEEN or key == DownloadByEnum.EXACT:
                if key not in episodes_dict:
                    episodes_dict[key] = SortedSet()
                episodes_dict[key].update(val)
            elif key == DownloadByEnum.RANGE_GREATER_THAN:
                if key not in episodes_dict:
                    episodes_dict[key] = val
                else:
                    episodes_dict[key] = min(episodes_dict[key], val)
            elif key == DownloadByEnum.RANGE_LESS_THAN:
                if key not in episodes_dict:
                    episodes_dict[key] = val
                else:
                    episodes_dict[key] = max(episodes_dict[key], val)
    return episodes_dict


def resolveSeparator2Dict(ep_str, separator, include_partial_range=True):
    episodes_dict = dict()
    ep_str_sep_split = ep_str.split(separator)
    num1, flag1 = parse_string_to_number(ep_str_sep_split[0])
    num2, flag2 = parse_string_to_number(ep_str_sep_split[1])
    if flag1 and flag2:
        elem = (num1, num2) if num1 < num2 else (num2, num1)
        episodes_dict[DownloadByEnum.RANGE_BETWEEN] = SortedSet()
        episodes_dict[DownloadByEnum.RANGE_BETWEEN].add(elem)
    elif flag1:
        episodes_dict[DownloadByEnum.RANGE_GREATER_THAN] = num1
        if include_partial_range:
            episodes_dict[DownloadByEnum.EXACT] = SortedSet()
            episodes_dict[DownloadByEnum.EXACT].add(num1)
    elif flag2:
        episodes_dict[DownloadByEnum.RANGE_LESS_THAN] = num2
        if include_partial_range:
            episodes_dict[DownloadByEnum.EXACT] = SortedSet()
            episodes_dict[DownloadByEnum.EXACT].add(num2)
    return episodes_dict


def listToDict(input_list, key, dict_type=None):
    ret_dict = dict_type if dict_type is not None else dict()
    for l in input_list:
        ret_dict[getattr(l, key)] = l
    return ret_dict


def transformFileName(name):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    transformed_file_name = ''.join(c for c in name if c in valid_chars)
    transformed_file_name = re.sub(' +', ' ', transformed_file_name)
    return transformed_file_name.strip().title()


def extractNumbersFromString(string_with_numbers, num_data_type=int, aggregate_function=max):
    try:
        num_map = map(num_data_type, re.findall("\d+", string_with_numbers))
        return aggregate_function(num_map)
    except Exception, e:
        return None


def compareUrls(url1, url2):
    match = url1 == url2
    if not match:
        try:
            url1_parsed = urlparse(url1)
            url2_parsed = urlparse(url2)
            url1_parsed = url1_parsed._replace(scheme='')
            url2_parsed = url2_parsed._replace(scheme='')
            match = url1_parsed.geturl() == url2_parsed.geturl()
        except Exception, e:
            match = False
    return match


def validateUrl(url):
    try:
        r = requests.head(url, verify=False)
        return r.status_code == requests.codes.ok
    except Exception, e:
        print e.message
    return False


def getCountdownValue(web_driver):
    countdown_timer_element = web_driver.find_element_by_id(Constants.ELEM_ID_COUNTDOWN)
    countdown_time = int(countdown_timer_element.get_attribute(Constants.IDF_TEXT_CONTENT))
    return countdown_time


def hasIsLoadingButton(web_driver):
    present = True
    try:
        web_driver.find_elements_by_class_name(Constants.CLASS_BTN_LOADING)
    except Exception, e:
        present = False
    return present


def findAnchorElementHref(parent_element):
    from BeautifulSoup import BeautifulSoup
    soup = BeautifulSoup(parent_element.get_attribute(Constants.IDF_INNER_HTML))
    anchor_element = soup.find(Constants.IDF_ANCHOR, href=True)
    return anchor_element


def closeWindows(web_driver, has_custom_url=False):
    idx = len(web_driver.window_handles) - 1
    while idx > (1 if has_custom_url else 0):
        idx_window = web_driver.window_handles[idx]
        web_driver.switch_to_window(idx_window)
        web_driver.close()
        idx -= 1
    if has_custom_url:
        web_driver.switch_to_window(web_driver.window_handles[1])
    else:
        web_driver.switch_to_window(web_driver.window_handles[0])
