import datetime
import decimal
from sqlalchemy import text, orm, func
from server.entities.inherit.sum import po,re

def convert_obj2dict(value):
    if value is None:
        return None
    elif isinstance(value, re.Base) or isinstance(value, po.Base):
        return value.to_dict();
    elif type(value) == datetime.datetime:
        return value.strftime('%Y-%m-%d %H:%M:%S');
    elif type(value) == datetime.time:
        return value.strftime('%H:%M:%S');
    elif type(value) == str or type(value) == int or type(value) == float or type(value) == bool:
        return value;
    elif isinstance(value, decimal.Decimal):
        return float(value);
    elif type(value) == list:
        return convert_objlist2dict(value);
    raise RuntimeError('unknown type:' + str(type(value)))

def convert_objlist2dict(obj_list):
    if isinstance(obj_list, orm.dynamic.Query):
        obj_list = obj_list.all();
    if type(obj_list) == list or isinstance(obj_list, orm.collections.InstrumentedList):
        return [convert_obj2dict(obj) for obj in obj_list];
    else:
        return convert_obj2dict(obj_list);

