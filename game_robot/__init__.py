from .jiuyin.script.TuanLian import TuanLian
from .jiuyin.script.NeiGong import NeiGong
from .jiuyin.script.CaiJi import CaiJi
from .jiuyin.script.ShaShou import ShaShou


import lib.global_data

lib.global_data.module_dc["团练"] = TuanLian()
lib.global_data.module_dc["内功"] = NeiGong()
lib.global_data.module_dc["采集"] = CaiJi()
lib.global_data.module_dc["杀手"] = ShaShou()

