# QE_Mani_Summary

####论文：
Using Query Expansion in Manifold Ranking for Query-Oriented Multi-Document Summarization

#### 软件环境
python3
mysql5.7
jenkins
docker
redis
ROUGE-1.5.5(Perl)

#### 安装
1.  docker上安装Jenkins

    下载镜像：docker pull jenkins/jenkins
    
    安装：docker run -d -p $PORT:8080 -p 50000:50000 -v $DATA_DIR:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker -v /etc/localtime:/etc/localtime -v /usr/lib/x86_64-linux-gnu/libltdl.so.7:/usr/lib/x86_64-linux-gnu/libltdl.so.7 --name $CON_NAME jenkins/jenkins
   
    权限问题：https://blog.csdn.net/u014595589/article/details/107028711

3.  数据库配置，如果数据库类型为sqlite则只需要配置数据库名称(database)，同时需要将data/*.db挂载出来
    如果数据库类型为mysql需要参考setup/mysql.txt, 使用setup/auto_summary.sql 对数据库进行初始化
    借助docker inspect $CON_NAME 可以找到容器网络上出口地址

4.  Redis配置见setup/redis.txt, 如果未开启缓存或者缓存类型FILE文件则不需要配置

5.  Jenkins配置git项目，将项目中Jenkins脚本复制到Jenkins构建脚本中，model/data的数据应挂载出来，根据需要配置挂载路径

6.  Rouge在容器中已经配置，如果在windows下使用Rouge，参考：https://blog.csdn.net/u014595589/article/details/71192441

7.  参见model/readme.txt第三条构建词语矩阵相似度

8.  数据预处理已经完成，如需参考，可参阅 model/source/preprocessing/readme.txt

#### 配置文件 conf/*.yaml
可以通过配置环境变量 conf 来设置配置文件名
1、db: mysql数据库配置
       type数据库类型，支持mysql和sqlite
2、redis: redis数据库配置
3、cache: load 是否开启缓存 （1是 0否）
          type 缓存类型  （FILE文件 REDIS redis缓存）

#### 部署教程

网页服务容器版：
1、先搭建环境镜像，脚本在 envs/Jenkins 中
2、再搭建应用镜像，脚本在Jenkins中

模型版：
参见model/readme.txt , 运行 model/main.py，不需要配置mysql数据库

#### 网页版用户登陆
用户名： ai
密码： auto-jia
