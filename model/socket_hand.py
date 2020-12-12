from loguru import logger
from model.form_main import MainForm
from lib.global_data import MainWindow

class FunctionManager:
    
    def __init__(self):
        logger.info("初始化websocket回调")
        self.func_dc = {}

    def __call__(self, func_name, *args, **kwargs):
        def register(cls):
            self.func_dc[func_name] = cls
            return cls
        return register


function_manager = FunctionManager()

@function_manager(func_name="hand_test")
def hand_test(data):
    print(data)


@function_manager(func_name="citan_table_syn")
def on_citan_table_syn(data):
    MainWindow.main_widget.set_data_signal.emit(data)
    MainWindow.main_widget.ref_data.connect(MainWindow.main_widget.on_ref_data)
    MainWindow.main_widget.ref_data.emit()
    MainWindow.main_widget.ref_data.disconnect(MainWindow.main_widget.on_ref_data)
