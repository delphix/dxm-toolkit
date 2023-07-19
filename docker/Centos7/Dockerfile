FROM centos:7

RUN yum -y install bzip2-devel libffi-devel \
    && yum -y groupinstall "Development Tools" \
    && yum -y install ncurses-devel readline-devel sqlite-devel xz-devel


RUN yum -y install zlib-devel libtool perl-core 

RUN cd /root \
    && curl https://ftp.openssl.org/source/openssl-1.1.1q.tar.gz -o openssl-1.1.1q.tar.gz \
    && tar -xzvf openssl-1.1.1q.tar.gz \
    && cd openssl-1.1.1q \
    && ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib \
    && make \
    && make install


RUN cd /usr/local/ssl \
    && ln -s /etc/pki/tls/certs certs \
    && ln -s /etc/pki/tls/private private \
    && ln -s /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem cert.pem


RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv
RUN echo 'export PYENV_ROOT="/root/.pyenv"' >> ~/.bashrc \
    && echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> ~/.bashrc

RUN exec "$SHELL"
RUN export CONFIGURE_OPTS="--with-openssl=/usr/local/ssl --with-openssl-rpath=auto --with-ssl-default-suites=openssl" \
    && $HOME/.pyenv/bin/pyenv install 3.11.1
RUN $HOME/.pyenv/bin/pyenv global 3.11.1

RUN yum -y install ca-certificates

SHELL ["/bin/bash", "-c"]

ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/bin:$PATH

RUN source ~/.bashrc \
    && pip3 install pyinstaller

RUN mkdir -p /github/workspace
RUN mkdir -p /github/home
RUN mkdir -p /github/workflow
COPY entrypoint.sh /entrypoint.sh
WORKDIR /github/workspace
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
