# QE_Mani_Summary

####���ģ�
Using Query Expansion in Manifold Ranking for Query-Oriented Multi-Document Summarization

#### �������
python3
mysql5.7
jenkins
docker
redis
ROUGE-1.5.5(Perl)

#### ��װ
1.  docker�ϰ�װJenkins

    ���ؾ���docker pull jenkins/jenkins
    
    ��װ��docker run -d -p $PORT:8080 -p 50000:50000 -v $DATA_DIR:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker -v /etc/localtime:/etc/localtime -v /usr/lib/x86_64-linux-gnu/libltdl.so.7:/usr/lib/x86_64-linux-gnu/libltdl.so.7 --name $CON_NAME jenkins/jenkins
   
    Ȩ�����⣺https://blog.csdn.net/u014595589/article/details/107028711

3.  ���ݿ����ã�������ݿ�����Ϊsqlite��ֻ��Ҫ�������ݿ�����(database)��ͬʱ��Ҫ��data/*.db���س���
    ������ݿ�����Ϊmysql��Ҫ�ο�setup/mysql.txt, ʹ��setup/auto_summary.sql �����ݿ���г�ʼ��
    ����docker inspect $CON_NAME �����ҵ����������ϳ��ڵ�ַ

4.  Redis���ü�setup/redis.txt, ���δ����������߻�������FILE�ļ�����Ҫ����

5.  Jenkins����git��Ŀ������Ŀ��Jenkins�ű����Ƶ�Jenkins�����ű��У�model/data������Ӧ���س�����������Ҫ���ù���·��

6.  Rouge���������Ѿ����ã������windows��ʹ��Rouge���ο���https://blog.csdn.net/u014595589/article/details/71192441

7.  �μ�model/readme.txt��������������������ƶ�

8.  ����Ԥ�����Ѿ���ɣ�����ο����ɲ��� model/source/preprocessing/readme.txt

#### �����ļ� conf/*.yaml
����ͨ�����û������� conf �����������ļ���
1��db: mysql���ݿ�����
       type���ݿ����ͣ�֧��mysql��sqlite
2��redis: redis���ݿ�����
3��cache: load �Ƿ������� ��1�� 0��
          type ��������  ��FILE�ļ� REDIS redis���棩

#### ����̳�

��ҳ���������棺
1���ȴ�������񣬽ű��� envs/Jenkins ��
2���ٴӦ�þ��񣬽ű���Jenkins��

ģ�Ͱ棺
�μ�model/readme.txt , ���� model/main.py������Ҫ����mysql���ݿ�

#### ��ҳ���û���½
�û����� ai
���룺 auto-jia
