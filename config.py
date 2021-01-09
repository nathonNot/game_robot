client_id = "TzuIpLtlkv3NWz1Wu6jCGFsm"
client_secret = "awxZs2L7wiFqmoL4QrNX1zWozPlLTeii"

pri_key = '''
MIICWwIBAAKBgQCQFA4YVQZatJAyO7TsuzkWE8dz17qi8GuOCnegKbKd6alLXkDz
KhVG3kd3GijouHtlqsm2zFCK7K+I5MUu8Fuk23OEwIVZn9StltjLzJ1hB1AZC1/N
CoCFZG5T2+AaQolrw8LvPS5jH2TuYQf7oLDHR88BKJgV/tZlr22Jicqm0wIDAQAB
AoGAMP6A5IlVRdcNCef/2Fi6SuWi96OuleYHzR+GGnLTiJuCtFxy3b27yoOf7cJ5
ktnZLHNtcLn90aA2+OhCnXmiz+M9PNArzfvtDoAKMlM9UEpBjGW/QYPkcHgnKOs9
utAr4OnPB9PFdvCuwya4P8AL/7kpjSW+4zQpUT459BlJFxECQQDYUnQQgyR3CZiG
Pj9vPfmmFmogpZpJTG9zAuOjOCxa5BQvV4iKhk6pkQAaVsjc7WMobEIhLqXn/I8E
ldsqIPj1AkEAqoFZULpjke8CQm0rmr2UdbhU74KKYzeS2KKKc/2TdQUzTqvBdY2+
VCyc0Ok6BWctBHfsu4FR6YpDYsg3QwvjpwJAEHeuaDdjhkBPwSBp+dDw+UjJiXSx
2xSbg1jb9WfoUH7+XmA+f7UbteLY7ChhIBheLQyYuCfx70gVpxa1WW6rJQJAEahR
mpWi6CMLZduub1kAvew4B5HKSRohQAQdOIPjOHQwaw5Ie6cRNeBk4RG2K4cS12qf
/o8W74udDObVKkFZ8wJAPL8bRWv0IWTlvwM14mKxcVf1qCuhkT8GgrG/YP/8fcW8
SiT+DifcA7BVOgQjgbTchSfaA+YNe7A9qiVmA+G4GQ==
'''

base_url = "https://fuakorm.com"
ws_url = "ws://127.0.0.1:8000"
# base_url = "http://127.0.0.1:8000"

import json
from loguru import logger
import lib.version_authentication as va
import datetime
from lib import global_data as gbd
import win32api
import win32con

def log_init(level="DEBUG"):
    logger.add(
        "log\\runtime_{time}.log", retention="10 days", rotation="5 MB", level=level
    )


def init_config():
    with open("config\\config.json", "r") as f:
        gbd.config_dc = json.loads(f.read())
    if gbd.config_dc == "" or gbd.config_dc is None:
        logger.error("未找到配置文件")
        return
    log_init(gbd.config_dc["log_level"])
    version_data = va.get_version()
    if version_data == None:
        logger.error("版本号异常")
        win32api.MessageBox(0, "版本号异常，请更新重试", "版本异常",win32con.MB_OK)
        return
    version = version_data.get("version")
    t_version = gbd.config_dc.get("version")
    if check_version(t_version,version):
        logger.error("版本号异常")
        win32api.MessageBox(0, "版本号异常，请更新重试", "版本异常",win32con.MB_OK)
        return
    end_time = version_data.get("end_time")
    if end_time == None:
        logger.error("时间异常")
        return
    time_now = datetime.datetime.now()
    time_now = time_now.year * 10000 + time_now.month * 100 + time_now.day
    if time_now > end_time:
        logger.error("有效期结束")
        return
    logger.info("当前程序版本号：：：" + gbd.config_dc["version"])
    return True

def check_version(t_version,version):
    t_version_int = t_version.split(".")
    version_int = version.split(".")
    for index,v in enumerate(version_int):
        if index <= len(t_version_int):
            if int(v) > int(t_version_int[index]):
                return True
    return False