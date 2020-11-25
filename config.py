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
# base_url = "http://127.0.0.1:8000"


import json
from loguru import logger
import lib.version_authentication as va
import datetime

def log_init(level="DEBUG"):
    logger.add(
        "log\\runtime_{time}.log", retention="10 days", rotation="5 MB", level=level
    )


def init_config():
    with open("config\\config.json", "r") as f:
        config = json.loads(f.read())
    if config == "" or config is None:
        logger.error("未找到配置文件")
        return
    log_init(config["log_level"])
    version_data = va.get_version()
    if version_data == None:
        logger.error("版本号异常")
        return
    version = version_data.get("version")
    end_time = version_data.get("end_time")
    if end_time == None:
        logger.error("时间异常")
        return
    time_now = datetime.datetime.now()
    time_now = time_now.year * 1000 + time_now.month * 100 + time_now.day
    if time_now > end_time:
        logger.error("有效期结束")
        return
    logger.info("当前程序版本号：：：" + config["version"])
    return True
    