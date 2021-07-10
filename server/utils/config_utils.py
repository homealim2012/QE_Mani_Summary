#!/usr/bin/env python2
#-*- coding: utf8 -*-
from easydict import EasyDict as edict
import yaml,os

def update_config(source,target):
    for key in target:
        if key not in source or (type(target[key]) != dict and type(target[key]) != edict) or \
                (type(source[key]) != dict and type(source[key]) != edict):
            source[key]=target[key]
        else:
            update_config(source[key],target[key])

def load_config(path):
    pdir=os.path.dirname(path)
    with open(path, encoding='UTF-8') as f:
        cf=edict(yaml.load(f))
    if 'include' in cf and cf.include and len(cf.include)>0:
        for ipath in cf['include']:
            newpath = os.path.join(pdir, ipath)
            try:
                assert os.path.isfile(newpath)
                with open(newpath) as f:
                    update_config(cf,yaml.load(f))
            except Exception:
                print('failed to load config from {}'.format(newpath))
    return cf

def write_config(path,config):
    with open(path) as f:
        yaml.dump(config,f)