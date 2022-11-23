FROM opensuse/leap:latest

USER root
RUN zypper in -y python3 \
    && zypper in -y python3-devel \
    && zypper in -y python3-pip \
    && zypper in -y git \ 
    && zypper in -y gcc \
    && zypper in -y zlib-devel \
    && zypper in -y openssl-devel \
    && zypper in -y libffi-devel \
    && zypper in -y libbz2-1 libbz2-devel

ENV CFLAGS "-std=gnu99"

RUN pip3 install wheel \
    && pip3 install pyinstaller \
    && pip3 install jeepney

RUN mkdir -p /github/workspace
RUN mkdir -p /github/home
RUN mkdir -p /github/workflow
COPY entrypoint.sh /entrypoint.sh
WORKDIR /github/workspace
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
