from enum import Enum


class InputCategoryEnum(Enum):
    NONE = 0
    ID = 1
    URL = 2


class DownloadByEnum(Enum):
    EXACT = 0
    RANGE_LESS_THAN = 1
    RANGE_GREATER_THAN = 2
    RANGE_BETWEEN = 3


class AiringStatusEnum(Enum):
    UNKNOWN = 0
    COMPLETED = 1
    ONGOING = 2

    @staticmethod
    def translateToEnum(str_val=None):
        if not str_val:
            return AiringStatusEnum.UNKNOWN
        str_val = str_val.strip().lower()
        if str_val in ['complete', 'completed', 'finish', 'finished', 'end', 'ended']:
            return AiringStatusEnum.COMPLETED
        if str_val in ['ongoing', 'airing', 'running']:
            return AiringStatusEnum.ONGOING
        return AiringStatusEnum.UNKNOWN


class AnimeCategoryEnum(Enum):
    NONE = 0
    ALL = 1
    DUBBED = 2
    SUBBED = 3
    COMBINED = 4

    @staticmethod
    def translateToEnum(str_val=None):
        if not str_val:
            return AnimeCategoryEnum.NONE
        str_val = str_val.strip().lower()
        if str_val in ['a', 'all']:
            return AnimeCategoryEnum.ALL
        if str_val in ['d', 'dub', 'dubbed']:
            return AnimeCategoryEnum.DUBBED
        if str_val in ['s', 'sub', 'subbed']:
            return AnimeCategoryEnum.SUBBED
        if str_val in ['c', 'combine', 'combined']:
            return AnimeCategoryEnum.COMBINED
        return AnimeCategoryEnum.NONE


class StatusTypeEnum(Enum):
    DOWNLOAD_SKIPPED = 1
    DOWNLOAD_PENDING = 2
    DOWNLOAD_STARTED = 4
    DOWNLOAD_FAILED = 8
    DOWNLOAD_SUCCESS = 16


class VideoQualityTypeEnum(Enum):
    _DEFAULT = 0
    _240P = 240
    _360P = 360
    _480P = 480
    _720P = 720
    _1080P = 1080

    @staticmethod
    def translateToEnum(str_val=None):
        if not str_val:
            return VideoQualityTypeEnum._DEFAULT
        str_val = str_val.strip().lower()
        if str(VideoQualityTypeEnum._240P) in str_val:
            return VideoQualityTypeEnum._240P
        if str(VideoQualityTypeEnum._360P) in str_val:
            return VideoQualityTypeEnum._360P
        if str(VideoQualityTypeEnum._480P) in str_val:
            return VideoQualityTypeEnum._480P
        if str(VideoQualityTypeEnum._720P) in str_val:
            return VideoQualityTypeEnum._720P
        if str(VideoQualityTypeEnum._1080P) in str_val:
            return VideoQualityTypeEnum._1080P
        return VideoQualityTypeEnum._DEFAULT
