from enum import *


class PlatformType(IntEnum):
    NONE = 0
    JUST_EMAIL = 1
    FACE_BOOK = 2
    GOOGLE = 3
    KAKAO = 4

    @classmethod
    def ToChoices(cls):
        ret = []
        for ele in cls:
            ret +=  [( ele.name , ele.value ),]
        return ret
    pass

class AuthState(IntEnum):
    NONE = 0
    LOGIN_REQ = auto()
    LOGIN_COMPLETE = auto()
    LOGIN_EXPIRED = auto()
    pass