# -*- coding:utf-8 -*-
import re

RPF = ['R', 'P', 'F']
ROUGEs = ['ROUGE-1', 'ROUGE-2', 'ROUGE-3', 'ROUGE-4', 'ROUGE-L', 'ROUGE-W-1.2', 'ROUGE-SU4']

def get_ROUGE_from_file(srcpath):
    res_dict = {}
    with open(srcpath, "r") as fh:
        lines = fh.read()
        for ROUGE in ROUGEs:
            for a_RPF in RPF:
                searchObj = re.search(ROUGE + r' Average_' + a_RPF + r': (.*?) .*', lines, re.M | re.I)
                if searchObj:
                    res_dict[ROUGE + '-' + a_RPF] = searchObj.group(1);
                else:
                    raise Exception('ROUGE 正在处理中，请耐心等待')
    return res_dict

