import datetime
import os
import time


KAVENEGAR_API = "696D55316F69456C7A324269526B73637455746668736E394C2F776B4A5A35754D6C3941443739706F6D633D"
TELEGRAM_API = "1017478270:AAHDBewuiD-Bn2KqgAJ5NaoE4NGpebHmZ6Y"
SERVER_URL = "http://localhost:8000/"
CREATOR_PHONE = "+989350633006"
CREATOR_EMAIL = "rezazeiny1998@gmail.com"
CREATOR_ID = 95341489


PYTHON_PATH = os.path.realpath(__file__)
PYTHON_DIRECTORY = "/".join(PYTHON_PATH.split("/")[:-1])

CURRENT_DATETIME = str(datetime.datetime.now()).replace(" ", "=").replace(":", "-").split(".")[0]
# CURRENT_DATETIME = "2019-10-02=15-13-19"
CURRENT_TIME = str(int(time.time()))


class Colors:
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NO_UNDERLINE = '\033[24m'
    NEGATIVE = '\033[7m'
    POSITIVE = '\033[27m'
    BLACK_F = '\033[30m'
    RED_F = '\033[31m'
    GREEN_F = '\033[32m'
    YELLOW_F = '\033[33m'
    BLUE_F = '\033[34m'
    MAGENTA_F = '\033[35m'
    CYAN_F = '\033[36m'
    WHITE_F = '\033[37m'
    EXTENDED_F = '\033[38m'
    DEFAULT_F = '\033[39m'
    BLACK_B = '\033[40m'
    RED_B = '\033[41m'
    GREEN_B = '\033[42m'
    YELLOW_B = '\033[43m'
    BLUE_B = '\033[44m'
    MAGENTA_B = '\033[45m'
    CYAN_B = '\033[46m'
    WHITE_B = '\033[47m'
    EXTENDED_B = '\033[48m'
    DEFAULT_B = '\033[49m'
    BRIGHT_BLACK_F = '\033[90m'
    BRIGHT_RED_F = '\033[91m'
    BRIGHT_GREEN_F = '\033[92m'
    BRIGHT_YELLOW_F = '\033[93m'
    BRIGHT_BLUE_F = '\033[94m'
    BRIGHT_MAGENTA_F = '\033[95m'
    BRIGHT_CYAN_F = '\033[96m'
    BRIGHT_WHITE_F = '\033[97m'
    BRIGHT_BLACK_B = '\033[100m'
    BRIGHT_RED_B = '\033[101m'
    BRIGHT_GREEN_B = '\033[102m'
    BRIGHT_YELLOW_B = '\033[103m'
    BRIGHT_BLUE_B = '\033[104m'
    BRIGHT_MAGENTA_B = '\033[105m'
    BRIGHT_CYAN_B = '\033[106m'
    BRIGHT_WHITE_B = '\033[107m'
