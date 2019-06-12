import ast
import Constants
import json
import math
import requests
from collections import namedtuple
from Enums import StatusTypeEnum, AnimeCategoryEnum
from tqdm import tqdm


def readFile(file_name, is_json=True):
    with open(file_name) as fp:
        if is_json:
            data = json.load(fp)
        else:
            data = fp.readlines()
    return data


def writeFile(file_name, data, is_json=True):
    new_data = data
    with open(file_name, 'w') as fp:
        if is_json:
            new_data = json.dumps(data, indent=4)
        fp.write(new_data)


def readFromJsonFile(json_file_name, json_root_key, sort_key=None, return_named_tuple=True):
    json_data = readFile(json_file_name)
    if json_data and len(json_data.keys()) > 0:
        json_data = json_data[json_root_key]
    if sort_key:
        json_data.sort(key=sort_key, reverse=True)
    for idx, datum in enumerate(json_data):
        if Constants.TEXT_CATEGORY in datum:
            datum[Constants.TEXT_CATEGORY] = AnimeCategoryEnum.translateToEnum(datum[Constants.TEXT_CATEGORY])
        elif Constants.TEXT_ENABLED in datum:
            datum[Constants.TEXT_ENABLED] = ast.literal_eval(datum[Constants.TEXT_ENABLED])
        if return_named_tuple:
            json_data[idx] = namedtuple('dict', datum.keys())(**datum)
    return json_data


def writeToJsonFile(json_file_name, data, json_root_key):
    if not type(data) is dict or len(data.keys) == 0:
        data = {json_root_key: data}
    writeFile(json_file_name, data)


def downloadFileFromUrl(url, destination_file_path, destination_file_desc):
    if not url:
        return StatusTypeEnum.DOWNLOAD_SKIPPED
    download_status = StatusTypeEnum.DOWNLOAD_PENDING
    try:
        r = requests.get(url, stream=True)
        if 200 <= r.status_code < 300:
            total_size = int(r.headers.get(Constants.REQUEST_HEADER_PARAM, 0))
            wrote = 0
            with open(destination_file_path, 'wb') as f:
                download_status = StatusTypeEnum.DOWNLOAD_STARTED
                for data in tqdm(r.iter_content(Constants.BUFFER_SIZE),
                                 total=math.ceil(total_size // Constants.BUFFER_SIZE),
                                 unit=' KB', unit_scale=True, desc=destination_file_desc):
                    wrote = wrote + len(data)
                    f.write(data)
            if (total_size != 0 and wrote != total_size) or wrote < Constants.MIN_VIDEO_SIZE:
                download_status = StatusTypeEnum.DOWNLOAD_FAILED
            else:
                download_status = StatusTypeEnum.DOWNLOAD_SUCCESS
        else:
            download_status = StatusTypeEnum.DOWNLOAD_FAILED
    except Exception, ex:
        download_status = StatusTypeEnum.DOWNLOAD_FAILED
    return download_status
