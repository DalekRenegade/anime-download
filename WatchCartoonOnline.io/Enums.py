from enum import Enum


class DownloadTypeEnum(Enum):
    ALL = 1
    BY_SEASON = 2
    BY_EPISODE = 4
    BY_TITLE = 8


class StatusTypeEnum(Enum):
    DOWNLOAD_SKIP = 1
    DOWNLOAD_PENDING = 2
    DOWNLOAD_STARTED = 4
    DOWNLOAD_FAILED = 8
    DOWNLOAD_SUCCESS = 16

# Future work
# ErrorTypeEnum = Enum(NOT_INITIATED=1, INTERRUPT_NETWORK=2, INTERRUPT_USER=4)
