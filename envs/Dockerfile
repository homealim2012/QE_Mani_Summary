FROM python:3.7-alpine

MAINTAINER jiaquanye@buaa.edu.cn

COPY requirements.txt /requirements.txt
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add --no-cache --virtual temp-apks expat-dev make gcc g++ perl-dev && \
    apk add --no-cache db-dev && \
    echo -e "yes" | perl -MCPAN -e 'notest install XML::Parser' && \
    perl -MCPAN -e 'notest install XML::DOM' && \
    perl -MCPAN -e 'notest install DB_File' && \
    pip install --no-cache-dir --disable-pip-version-check -r /requirements.txt --trusted-host mirrors.163.com -i http://mirrors.163.com/pypi/simple && \
    apk del temp-apks && \
    apk add --no-cache perl