# coding: utf-8
import os;
import pymysql
import sqlacodegen.main
import sys

no_views = True
no_constraints = True
no_indexes = True
no_joined = True
no_inflect = True
no_classes = False
use_cmd = True

filePath = 'po.py'
#select tablename from pg_tables where schemaname = 'public' order by tablename
url = 'mysql+mysqlconnector://user:user@localhost:3306/auto_summary'
tables = ['result']

if __name__ == '__main__':
    genstr = 'sqlacodegen ';
    if no_views:
        genstr += ' --noviews ';
    if no_constraints:
        genstr += ' --noconstraints ';
    if no_indexes:
        genstr += ' --noindexes ';
    if no_joined:
        genstr += ' --nojoined ';
    if no_inflect:
        genstr += ' --noinflect ';
    if no_classes:
        genstr += ' --noclasses ';
    genstr += ' --outfile ' + filePath;
    genstr += ' ' + url + ' ';
    if len(tables) > 0:
        genstr += ' --tables ' + ','.join(tables);
    #print(genstr);
    if use_cmd:
        temp = genstr.split(' ')[1:]
        genarr = []
        for a_temp in temp:
            if not a_temp == '':
                genarr.append(a_temp)
        sys.argv.extend(genarr)
        sqlacodegen.main.main()
    else:
        os.system(genstr)

    f = open(filePath, 'r', encoding='utf-8')
    contents = f.read()
    f.close()
    contents = contents.replace('Base = declarative_base()', 'Base = object');
    contents = contents.replace('metadata = Base.metadata', '');
    f = open(filePath, 'w', encoding='utf-8');
    f.write(contents);
    f.close();
