file_name = []
module_dc = {}

hwnd_list = []
main_window_no_flush = False
main_window_hwnd = []

this_screen = None

Exit = False

threa_sleep_time = 0.5

threads = {}

class UserData:

    user_id = 0

    user_name = ""

    user_pass = ""
    
    vip_end_time = None

    def __init__(self,**kwargs):
        self.user_id = kwargs.get("id")
        self.user_name = kwargs.get("user_name")
        self.user_pass = kwargs.get("user_password")
        self.vip_end_time = kwargs.get("vip_end_time")
    
    @classmethod
    def is_vip(cls):
        if cls.vip_end_time == None:
            return False
        import datetime
        now = datetime.datetime.now()
        if now > cls.vip_end_time:
            return False
        return True     

user_data = None

main_log_info_call_back = None

socket_client = None

call_back = None

MainWindow = None

config_dc = None

key_range_list = []
