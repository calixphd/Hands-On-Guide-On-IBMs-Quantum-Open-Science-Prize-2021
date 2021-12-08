FROM ubuntu:20.10

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get install -y build-essential wget python3-dev \
    libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
    libffi-dev -y

RUN mkdir /tmp/Python39 \
    && cd /tmp/Python39 \
    && wget https://www.python.org/ftp/python/3.9.2/Python-3.9.2.tar.xz \
    && tar xvf Python-3.9.2.tar.xz \
    && cd /tmp/Python39/Python-3.9.2 \
    && ./configure \
    && make altinstall


RUN apt-get install curl -y

RUN ln -s /usr/local/bin/python3.9 /usr/bin/python
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py

RUN apt-get install git -y

RUN pip install --upgrade pip

RUN pip install jupyter --upgrade
RUN pip install jupyterlab --upgrade
RUN pip install jupyterlab-git

RUN unlink /usr/bin/python
RUN ln -s /usr/local/bin/python3.9 /usr/bin/python


RUN pip install qiskit
RUN pip install numpy scipy matplotlib ipython pandas sympy nose seaborn
RUN pip install scikit-learn

RUN cd ~ && curl -sL https://deb.nodesource.com/setup_14.x -o nodesource_setup.sh \
    && sh nodesource_setup.sh \
    && apt install nodejs -y


ENV MAIN_PATH=/usr/local/bin/jpl_config
ENV LIBS_PATH=${MAIN_PATH}/libs
ENV CONFIG_PATH=${MAIN_PATH}/config
ENV NOTEBOOK_PATH=${MAIN_PATH}/notebooks

EXPOSE 8888

CMD cd ${MAIN_PATH} && sh config/run_jupyter.sh
