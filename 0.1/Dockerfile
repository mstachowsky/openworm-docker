FROM ubuntu:16.04

MAINTAINER David Lung "lungdm@gmail.com"

RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get dist-upgrade -y


RUN mkdir /etc/sudoers.d

RUN export uid=1000 gid=1000 && \
    mkdir -p /home/ow && \
    echo "ow:x:${uid}:${gid}:ow,,,:/home/ow:/bin/bash" >> /etc/passwd && \
    echo "ow:x:${uid}:" >> /etc/group && \
    echo "ow ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ow && \
    chmod 0440 /etc/sudoers.d/ow && \
    chown ${uid}:${gid} -R /home/ow


ENV DEBIAN_FRONTEND noninteractive # TODO: change


#RUN useradd -ms /bin/bash ow


RUN apt-get install -y apt-utils \
  build-essential \
  make \
  git \
  automake \
  autoconf \
  g++ \
  rpm \
  libtool \
  libncurses5-dev \
  zlib1g-dev \
  bison \
  flex \
  lsb-core \
  sudo \
  xorg \
  openbox \
  x11-xserver-utils \
  libxext-dev libncurses-dev python-dev mercurial \
  freeglut3-dev libglu1-mesa-dev libglew-dev python-dev python-lxml python-numpy python-scipy python-matplotlib python-tk \
  kmod dkms \
  linux-source linux-headers-$(uname -r)

RUN apt-get install -y --no-install-recommends xubuntu-desktop 

#RUN sudo apt-get install nvidia-opencl-dev



COPY ./NVIDIA-Linux-x86_64-375.82.run /home/ow/NVIDIA-Linux-x86_64-375.82.run
RUN service lightdm stop && \
  cd /home/ow && \
  chmod +x NVIDIA-Linux-x86_64-375.82.run && \
  ./NVIDIA-Linux-x86_64-375.82.run -s -N --no-kernel-module 


COPY ./intel_sdk_for_opencl_2017_7.0.0.2511_x64.tgz /home/ow/intel_sdk_for_opencl_2017_7.0.0.2511_x64.tgz
RUN cd /home/ow && \
  tar xvf intel_sdk_for_opencl_2017_7.0.0.2511_x64.tgz
COPY ./silent-intel-sdk.cfg /home/ow/intel_sdk_for_opencl_2017_7.0.0.2511_x64/silent-intel-sdk.cfg
RUN cd /home/ow/intel_sdk_for_opencl_2017_7.0.0.2511_x64 && \
  ./install.sh --silent silent-intel-sdk.cfg


RUN service lightdm start

USER ow
ENV HOME /home/ow
WORKDIR $HOME




RUN mkdir neuron && \
  cd neuron && \
  git clone https://github.com/nrnhines/iv.git && \
  git clone https://github.com/nrnhines/nrn.git && \
  cd iv && \
  ./build.sh && \
  ./configure --prefix=`pwd` && \
  make && \
  sudo make install && \
  cd ../nrn && \
  ./build.sh && \
  ./configure --prefix=`pwd` --with-iv=$HOME/neuron/iv --with-nrnpython=/usr/bin/python && \
  make && \
  sudo make install && \
  cd src/nrnpython && \
  sudo python setup.py install


RUN sudo mv /usr/lib/x86_64-linux-gnu/libGL.so /usr/lib/x86_64-linux-gnu/libGL.so.BAK && \
  sudo ln -s /usr/lib/libGL.so.1 /usr/lib/x86_64-linux-gnu/libGL.so


RUN sudo apt-get install maven openjdk-8-jdk -y


RUN git clone https://github.com/NeuroML/jNeuroML.git && \
  cd jNeuroML && \
  git checkout development && \
  sudo python getNeuroML.py development
  
RUN sudo apt-get install -y python-setuptools python-yaml libnuma1

RUN git clone https://github.com/lungd/pyNeuroML.git && \
  cd pyNeuroML && \
  sudo python setup.py install

RUN git clone https://github.com/openworm/PyOpenWorm.git && \
  cd PyOpenWorm && \
  git checkout dev && \
  sudo python setup.py install

RUN git clone https://github.com/lungd/CElegansNeuroML.git && \
  cd CElegansNeuroML && \
  git checkout tmp

RUN git clone https://github.com/lungd/sibernetic.git && \
  cd sibernetic && \
  git checkout v0.1 && \
  make clean && make all


ENV JNML_HOME=$HOME/neuroml_dev/jNeuroML
ENV PATH=$PATH:$JNML_HOME
ENV IV=$HOME/neuron/iv
ENV N=$HOME/neuron/nrn
ENV CPU=x86_64
ENV PATH=$PATH:$IV/$CPU/bin:$N/$CPU/bin
ENV NEURON_HOME=$N/$CPU
ENV PYTHONPATH=$PYTHONPATH:$HOME/sibernetic
ENV C302_HOME=$HOME/CElegansNeuroML/CElegans/pythonScripts/c302

