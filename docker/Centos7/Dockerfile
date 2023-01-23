FROM centos:7

RUN yum -y install openssl-devel bzip2-devel libffi-devel \
    && yum -y groupinstall "Development Tools" \
    && yum -y install ncurses-devel readline-devel sqlite-devel xz-devel
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv
RUN echo 'export PYENV_ROOT="/root/.pyenv"' >> ~/.bashrc \
    && echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> ~/.bashrc

RUN exec "$SHELL"
RUN $HOME/.pyenv/bin/pyenv install 3.9.16
RUN $HOME/.pyenv/bin/pyenv global 3.9.16


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
