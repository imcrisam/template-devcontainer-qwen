FROM node:24
WORKDIR /app
RUN apt-get update && apt-get install -y xdg-utils

RUN mkdir -p /root/.continue

RUN rm -f /root/.continue/config.yaml && \
ln -s /workspace/.continue/config.yaml /root/.continue/config.yaml


CMD ["sleep", "infinity"]