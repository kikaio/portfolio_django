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

