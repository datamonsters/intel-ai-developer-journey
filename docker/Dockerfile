FROM ubuntu:16.04

MAINTAINER Nik Spirin (@spirinus)

RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    build-essential \
    bzip2 \
    curl \
    g++ \
    git \
    vim \
    libfreetype6-dev \
    libpng12-dev \
    libzmq3-dev \
    pkg-config \
    python \
    python-dev \
    rsync \
    software-properties-common \
    unzip \
    wget \
    apt-utils

RUN wget --quiet https://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh

ENV PATH /opt/conda/bin:$PATH

RUN pip install --upgrade pip

RUN pip install tensorflow==1.2.0 && \
    pip install Keras==2.0.4

RUN conda install graphviz=2.38.0 pillow seaborn && \
    pip install pydot==1.1.0

COPY notebooks /root/notebooks
RUN mkdir /root/shared

EXPOSE 8888
EXPOSE 9000

CMD bash -c "jupyter notebook --port=8888 --ip=* --notebook-dir='/root'"
