file_name = []
module_dc = {}

hwnd_list = []

this_screen = None

Exit = False

threa_sleep_time = 0.5

threads = {}

class UserData:

    user_id = 0

    user_name = ""

    user_pass = ""
    
    def __init__(self,**kwargs):
        self.user_id = kwargs.get("id")
        self.user_name = kwargs.get("user_name")
        self.user_pass = kwargs.get("user_password")


user_data = None

main_log_info_call_back = None

socket_client = None

call_back = None

MainWindow = None

config_dc = None