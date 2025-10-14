FROM node:24
WORKDIR /node_angular
RUN apt-get update && apt-get install -y xdg-utils
CMD ["sleep", "infinity"]

RUN mkdir -p /root/.continue

RUN rm -f /root/.continue/config.yaml && \
    ln -s /workspace/.continue/config.yaml /root/.continue/config.yaml

