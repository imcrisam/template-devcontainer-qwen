FROM ubuntu:latest
WORKDIR /app
RUN apt-get update && apt-get install -y xdg-utils

RUN mkdir -p /root/.continue/index

RUN rm -f /root/.continue/config.yaml && \
ln -s /workspace/.continue/config.yaml /root/.continue/config.yaml

RUN rm -f /root/.continue/index/globalContext.json && \
ln -s /workspace/.continue/globalContext.json /root/.continue/index/globalContext.json


CMD ["sleep", "infinity"]