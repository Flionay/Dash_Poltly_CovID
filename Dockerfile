FROM python:3.8.2
MAINTAINER angyi_jq@163.com
COPY ../CovIdVis /covIdVis
WORKDIR /covIdVis/

EXPOSE 8888
RUN pip install -r requirement.txt