import requests
from lib.version_authentication import decode_data
import config
from lib import global_data as gbd

def do_register(user_name, user_pas):
    data = {"user_name": user_name, "user_pass": user_pas}
    res = requests.post(
        config.base_url + "/api/user/create_user", json=data
    )
    return decode_data(res.text)


def do_login(user_name, user_pas):
    data = {
        "user_name": user_name, 
        "user_pass": user_pas,
        "version":gbd.config_dc["version"]
        }
    res = requests.post(
        config.base_url + "/api/user/get_user",
        json=data
    )
    return decode_data(res.text)
