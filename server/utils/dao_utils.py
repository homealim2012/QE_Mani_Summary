# -*- coding: utf-8 -*-
from sqlalchemy import text, orm, func, or_, and_, distinct
from server.utils import convert_utils
import re

class DAO:

    def __init__(self,db_session,clazz):
        self.db_session = db_session
        self.clazz = clazz

    def querySQL(self, sqltext):
        resultProxy = self.db_session.execute(sqltext);
        result_set = resultProxy.fetchall();
        resultProxy.close();
        return result_set;

    def get_condition_for_query(self, clazz, field, filter, ownerid=''):
        content = filter['content']
        field_type = filter['type']
        if filter.get('contentType', 'value') == 'text':
            return text(field + ' ' + field_type + ' ' + content);
        elif field_type.strip() == 'equal' or field_type.strip() == '==':
            return getattr(clazz, field) == content;
        elif field_type.strip() == '<':
            return getattr(clazz, field) < content;
        elif field_type.strip() == '<=':
            return getattr(clazz, field) <= content;
        elif field_type.strip() == '>':
            return getattr(clazz, field) > content;
        elif field_type.strip() == '!=':
            return getattr(clazz, field) != content;
        elif field_type.strip() == '>=':
            return getattr(clazz, field) >= content;
        elif field_type.strip() == 'self':
            return getattr(clazz, field) == int(ownerid);
        elif field_type.strip() == 'like':
            return getattr(clazz, field).like(content);
        elif field_type.strip() == 'in':
            return getattr(clazz, field).in_(content);
        else:
            return text(field + ' ' + field_type + ' ' + content);

    def add_filter_for_query(self, query_obj, query_set, ownerid='',arr_outerjoin={}, mode = 0):
        clazz = self.clazz
        if (query_set.__contains__('filter') and len(query_set['filter']) > 0):
            for a_filter in query_set['filter']:
                if a_filter.__contains__('or'):
                    query_obj = query_obj.filter(self.get_or_conditions(a_filter['or'], arr_outerjoin, ownerid, mode));
                elif a_filter['field'].find('$') > -1 or a_filter['field'].find('.') > -1:
                    [f_key_name, attr_name] = re.split("\\$|\\.", a_filter['field']);
                    f_key_class = getattr(clazz, f_key_name).property.entity.class_;
                    if mode == 1:
                        query_obj = query_obj.filter(self.get_condition_for_query(f_key_class, attr_name, a_filter, ownerid))
                    else:
                        query_obj = query_obj.filter(getattr(clazz, f_key_name).
                            has(self.get_condition_for_query(f_key_class, attr_name, a_filter, ownerid)));
                    #arr_outerjoin.append({'f_cls': f_key_class, 'on': getattr(clazz, f_key_name)});
                    arr_outerjoin[getattr(clazz, f_key_name)] = f_key_class
                else:
                    query_obj = query_obj.filter(
                        self.get_condition_for_query(clazz, a_filter['field'], a_filter, ownerid));

        return query_obj;

    def get_or_conditions(self, ori_conditions, arr_outerjoin, ownerid='', mode=0):
        clazz = self.clazz
        or_conditions = [];
        for ori_condition in ori_conditions:
            for a_filter in ori_condition:
                and_conditions = [];
                if a_filter.__contains__('or'):
                    and_conditions.append(self.get_or_conditions(a_filter['or'], ownerid));
                elif a_filter['field'].find('$') > -1 or a_filter['field'].find('.') > -1:
                    [f_key_name, attr_name] = re.split("\\$|\\.", a_filter['field']);
                    f_key_class = getattr(clazz, f_key_name).property.entity.class_;
                    if mode == 1:
                        and_conditions.append(self.get_condition_for_query(f_key_class, attr_name, a_filter, ownerid))
                    else:
                        and_conditions.append(getattr(clazz, f_key_name).has(
                            self.get_condition_for_query(f_key_class, attr_name, a_filter, ownerid)));
                    #arr_outerjoin.append({'f_cls': f_key_class, 'on': getattr(clazz, f_key_name)});
                    arr_outerjoin[getattr(clazz, f_key_name)] = f_key_class
                else:
                    and_conditions.append(self.get_condition_for_query(clazz, a_filter['field'], a_filter, ownerid));
            or_conditions.append(and_(*and_conditions));
        return or_(*or_conditions);

    def add_orderBy_for_query(self, query_obj, query_set, arr_outerjoin = {}):
        clazz = self.clazz
        if (query_set.__contains__('orderBy') and len(query_set['orderBy']) > 0):
            for x in query_set['orderBy']:
                if type(x) == dict:
                    if x['field'].find('$') > -1 or x['field'].find('.') > -1:
                        [f_key_name, attr_name] = re.split("\\$|\\.", x['field']);
                        f_key_class = getattr(clazz, f_key_name).property.entity.class_;
                        this_column = getattr(f_key_class, attr_name)
                        arr_outerjoin[getattr(clazz, f_key_name)] = f_key_class
                        #arr_outerjoin.append({'f_cls': f_key_class, 'on': getattr(clazz, f_key_name)});
                    else:
                        this_column = getattr(clazz, x['field'])
                    if x['type'] == 'desc':
                        query_obj = query_obj.order_by(this_column.desc())
                    elif x['type'] == 'asc':
                        query_obj = query_obj.order_by(this_column.asc())
                else:
                    if x.find('$') > -1 or x.find('.') > -1:
                        [f_key_name, attr_name] = re.split("\\$|\\.", x);
                        f_key_class = getattr(clazz, f_key_name).property.entity.class_;
                        this_column = getattr(f_key_class, attr_name)
                        arr_outerjoin[getattr(clazz, f_key_name)] = f_key_class
                        #arr_outerjoin.append({'f_cls': f_key_class, 'on': getattr(clazz, f_key_name)});
                    else:
                        this_column = getattr(clazz, x)
                    query_obj = query_obj.order_by(this_column);
        return query_obj;

    def add_limits_for_query(self, query_obj, query_set):
        if (query_set.__contains__('limits') and len(query_set['limits']) > 0):
            if (query_set['limits'][1] != -1):
                query_obj = query_obj.limit(query_set['limits'][1]).offset(query_set['limits'][0]);
        return query_obj;

    def add_outer_join_for_query(self, query_obj, arr_outerjoin):
        for outerjoin in arr_outerjoin:
            query_obj = query_obj.outerjoin(arr_outerjoin[outerjoin], outerjoin);
        return query_obj;

    def get_query_columns(self, query_set, clazz, arr_outerjoin={}):
        arr_columns = [];
        for a_column in query_set['columns']:
            column_field = a_column['field'] if type(a_column) == dict else a_column;

            if column_field.find('$') > -1 or column_field.find('.') > -1:
                [f_key_name, attr_name] = re.split("\\$|\\.", column_field);
                f_key_class = getattr(clazz, f_key_name).property.entity.class_;
                arr_columns.append(getattr(f_key_class, attr_name));
                #arr_outerjoin.append({'f_cls': f_key_class, 'on': getattr(clazz, f_key_name)});
                arr_outerjoin[getattr(clazz, f_key_name)] = f_key_class
            else:
                arr_columns.append(getattr(clazz,column_field));
        return arr_columns

    def query_for_columns(self, query_set, ownerid=''):
        try:
            clazz = self.clazz
            db_session = self.db_session
            arr_outerjoin = {};
            arr_columns = self.get_query_columns(query_set, clazz, arr_outerjoin);
            query_obj = db_session.query(*arr_columns).select_from(clazz).distinct();
            query_obj = self.add_filter_for_query(query_obj, query_set, ownerid, arr_outerjoin, mode=1);
            query_obj = self.add_orderBy_for_query(query_obj, query_set, arr_outerjoin);
            query_obj = self.add_outer_join_for_query(query_obj, arr_outerjoin);
            totalLength = query_obj.count()

            query_obj = self.add_limits_for_query(query_obj, query_set);
            result_set = query_obj.all();
            dataLength = query_obj.count();

            result_dict = {'status': 'ok', 'msg': 'ok', 'code': 0,
                           'dataLength': dataLength, 'totalLength': totalLength, 'data': []}
            for a_result in result_set:
                a_result_dict = {};
                for index, a_column in enumerate(query_set['columns']):
                    value = a_result[index];
                    column_name = a_column['name'] if type(a_column) == dict else a_column;
                    a_result_dict[column_name] = convert_utils.convert_objlist2dict(value);

                result_dict['data'].append(a_result_dict);
            return result_dict
        except Exception as e:
            db_session.rollback()
            raise e

    def query(self, query_set, db_session=None, ownerid=''):
        try:
            clazz = self.clazz
            db_session = self.db_session
            query_obj = db_session.query(clazz);
            query_obj = self.add_filter_for_query(query_obj, query_set, ownerid);
            query_obj = self.add_orderBy_for_query(query_obj, query_set);
            query_obj = self.add_limits_for_query(query_obj, query_set);
            result_set = query_obj.all();
            dataLength = query_obj.count();

            count_query_obj = db_session.query(func.count('*')).select_from(clazz);
            count_query_obj = self.add_filter_for_query(count_query_obj, query_set, ownerid);
            totalLength = count_query_obj.scalar();

            result_dict = {'status': 'ok', 'msg': 'ok', 'code': 0,
                           'dataLength': dataLength, 'totalLength': totalLength, 'data': []}
            for a_result in result_set:
                a_result_dict = {};
                for a_column in query_set['columns']:
                    column_field = a_column['field'] if type(a_column) == dict else a_column;

                    if column_field.find('.') > -1 or column_field.find('$') > -1:
                        [obj_name, attr_name] = re.split("\\$|\\.", column_field)
                        if getattr(a_result, obj_name) != None:
                            value = getattr(getattr(a_result, obj_name), attr_name);
                        else:
                            value = None;
                    else:
                        value = getattr(a_result, column_field)

                    column_name = a_column['name'] if type(a_column) == dict else a_column;
                    a_result_dict[column_name] = convert_utils.convert_objlist2dict(value);

                result_dict['data'].append(a_result_dict);
            return result_dict
        except Exception as e:
            db_session.rollback()
            raise e

    def edit(self, edit_set, is_modify_time=False, is_update_all=False):
        clazz = self.clazz
        db_session = self.db_session
        try:
            data_list = edit_set['data'];
            for a_edit in data_list:
                update_dict = {};
                for data in a_edit['fields']:
                    if data.__contains__('content'):
                        update_dict[data['field']] = data['content'];
                    else:
                        update_dict[data['field']] = 'null';

                if is_modify_time:
                    update_dict['modifyTime'] = 'now()';

                update_obj = db_session.query(clazz);
                is_has_id = False
                for edit_id in a_edit:
                    if edit_id.find('id') > -1:
                        is_has_id = True;
                        a_id, id_name = a_edit[edit_id], edit_id;
                        update_obj = update_obj.filter(getattr(clazz, id_name) == a_id);
                        break;

                if not is_update_all and not is_has_id:
                    db_session.rollback()
                    res = {'status': 'fail', 'reason': '更新需要指定某些项数据'}
                    return res;

                update_obj = self.add_filter_for_query(update_obj, a_edit);
                update_obj = self.add_filter_for_query(update_obj, edit_set);
                update_obj.update(update_dict)
            db_session.commit()
            res = {'status': 'ok'}
            return res
        except Exception as e:
            db_session.rollback()
            raise e

    def rm(self, id_set, is_rm_all=False):
        clazz = self.clazz
        db_session = self.db_session
        try:
            is_has_id = False
            rm_obj = db_session.query(clazz);
            for id_name in id_set:
                if id_name.find('id') > -1:
                    rm_obj = rm_obj.filter(getattr(clazz, id_name).in_(id_set[id_name]));
                    is_has_id = True;
                    break;
            if not is_rm_all and not is_has_id:
                db_session.rollback()
                res = {'status': 'fail', 'reason': '删除需要指定某些项数据'}
                return res;
            rm_obj = self.add_filter_for_query(rm_obj, id_set);
            rm_obj.delete(synchronize_session=False);
            db_session.commit()
            res = {'status': 'ok'}
            return res
        except Exception as e:
            db_session.rollback()
            raise e

    def add(self, add_set, primary_key_name='id'):
        db_session = self.db_session
        try:
            insert_data = [];
            data_set = add_set['data'];
            for data in data_set:
                ins = self.clazz()
                for key in data:
                    setattr(ins, key, data[key]);
                insert_data.append(ins);

            db_session.add_all(insert_data);
            db_session.commit()

            return_list = [];
            for a_insert_data in insert_data:
                return_list.append(getattr(a_insert_data, primary_key_name));

            res = {'status': 'ok', primary_key_name: return_list}
            return res
        except Exception as e:
            db_session.rollback()
            raise e
