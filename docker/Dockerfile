FROM ubuntu:16.04

MAINTAINER Nik Spirin (@spirinus)

RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    build-essential \
    bzip2 \
    curl \
    g++ \
    git \
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
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh

ENV PATH /opt/conda/bin:$PATH

RUN pip install --upgrade pip

RUN pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.2.0-cp27-none-linux_x86_64.whl && \
    pip install Keras==2.0.4

RUN conda install -y -c anaconda graphviz=2.38.0 && \
    pip install pydot==1.1.0 && \
    conda install pillow

COPY notebooks /root/notebooks

RUN mkdir /root/shared

# TensorBoard
EXPOSE 6006
# IPython
EXPOSE 8888

#WORKDIR "/notebooks"

CMD bash -c "jupyter notebook --port=8888 --ip=* --notebook-dir='/root'"
