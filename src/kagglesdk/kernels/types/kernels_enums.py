import enum


class KernelExecutionType(enum.Enum):
    KERNEL_EXECUTION_TYPE_UNSPECIFIED = 0
    SAVE_AND_RUN_ALL = 1
    INTER_ACTIVE = 2
    QUICK_SAVE = 3


class KernelsListSortType(enum.Enum):
    HOTNESS = 0
    COMMENT_COUNT = 1
    DATE_CREATED = 2
    DATE_RUN = 3
    RELEVANCE = 4
    SCORE_ASCENDING = 5
    SCORE_DESCENDING = 6
    VIEW_COUNT = 7
    VOTE_COUNT = 8


class KernelsListViewType(enum.Enum):
    KERNELS_LIST_VIEW_TYPE_UNSPECIFIED = 0
    PROFILE = 1
    UPVOTED = 2
    EVERYONE = 3
    COLLABORATION = 4
    FORK = 5
    BOOKMARKED = 6
    RECENTLY_VIEWED = 7
    PUBLIC_AND_USERS_PRIVATE = 8


class KernelWorkerStatus(enum.Enum):
    QUEUED = 0
    RUNNING = 1
    COMPLETE = 2
    ERROR = 3
    CANCEL_REQUESTED = 4
    CANCEL_ACKNOWLEDGED = 5
    NEW_SCRIPT = 6
