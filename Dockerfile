FROM py3-autosum-envs
ADD . /home/auto_summary_python
RUN echo "Asia/Shanghai" > /etc/timezone
ENV LANGUAGE="en_US.UTF-8" \
   LANG=en_US:zh_CN.UTF-8 \
   LC_ALL=C
WORKDIR /home/auto_summary_python
ENTRYPOINT ["/venv/bin/python3", "run.py"]