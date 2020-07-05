import enum

class LogCategoryEnum(enum.IntEnum):
	NONE = 0
	GM_ACCOUNT = 1	# 개인 운영자 계정
	GM_MANAGE = 2 #타 운영자 계정 포함


class LogGmAccountEnumWhat(enum.IntEnum):
	NONE=0
	SIGN = 1
	PASSWORD = 2


class LogGmAccountEnumHowSignGmAccount(enum.IntEnum):
	NONE=0
	REGIST = 1
	LOG_IN = 2
	LOG_OUT = 3
	LOCKED = 4
	DORMANT = 5
	ACTIVATE = 6

class LogGmAccountEnumHowPwGmAccount(enum.IntEnum):
	NONE=0
	PW_CHANGE = 1
	PW_RESET = 2

class LogGmManageEnumWhat(enum.IntEnum):
	NONE = 0
	PERMISSION = 1

class LogGmAccountEnumHowPermission(enum.IntEnum):
	NONE = 0
	EDIT = 1
