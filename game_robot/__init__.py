from .jiuyin.script.TuanLian import TuanLian
from .jiuyin.script.NeiGong import NeiGong

import lib.global_data

lib.global_data.module_dc["团练"] = TuanLian()
lib.global_data.module_dc["内功"] = NeiGong()


