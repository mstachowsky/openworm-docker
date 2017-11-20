FROM ubuntu:16.04

MAINTAINER David Lung "lungdm@gmail.com"

ARG USR=ow
ENV USER=$USR


ARG NVIDIA_VERSION=375.82



ARG INTEL_SDK_SILENT_CONFIG=silent-intel-sdk.cfg

#ARG NVIDIA_RUN_FILE=NVIDIA-Linux-x86_64-375.82.run
#ARG INTEL_SDK_OPENCL_VERSION=intel_sdk_for_opencl_2017_7.0.0.2511_x64
#ARG INTEL_SDK_OPENCL=$INTEL_SDK_OPENCL_VERSION.tgz



RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get dist-upgrade -y





RUN mkdir /etc/sudoers.d

RUN export uid=1000 gid=1000 && \
    mkdir -p /home/$USER && \
    echo "$USER:x:${uid}:${gid}:$USER,,,:/home/$USER:/bin/bash" >> /etc/passwd && \
    echo "$USER:x:${uid}:" >> /etc/group && \
    echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER && \
    chmod 0440 /etc/sudoers.d/$USER && \
    chown ${uid}:${gid} -R /home/$USER


ENV DEBIAN_FRONTEND noninteractive # TODO: change


#RUN useradd -ms /bin/bash $USER


RUN apt-get install -y apt-utils \
  wget \
  nano \
  htop \
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
  linux-source linux-headers-$(uname -r) \
  maven openjdk-8-jdk \
  python-setuptools python-yaml libnuma1 \
  openmpi-bin  libopenmpi-dev

RUN apt-get install -y --no-install-recommends xubuntu-desktop 

#RUN sudo apt-get install nvidia-opencl-dev


USER $USER
ENV HOME /home/$USER
WORKDIR $HOME


RUN wget http://us.download.nvidia.com/XFree86/Linux-x86_64/$NVIDIA_VERSION/NVIDIA-Linux-x86_64-$NVIDIA_VERSION.run
RUN sudo service lightdm stop && \
  cd $HOME && \
  sudo chmod +x NVIDIA-Linux-x86_64-$NVIDIA_VERSION.run && \
  sudo ./NVIDIA-Linux-x86_64-$NVIDIA_VERSION.run -s -N --no-kernel-module 


RUN wget http://registrationcenter-download.intel.com/akdlm/irc_nas/vcp/11705/intel_sdk_for_opencl_2017_7.0.0.2511_x64.tgz
COPY ./$INTEL_SDK_SILENT_CONFIG $HOME/$INTEL_SDK_SILENT_CONFIG
RUN cd $HOME && \
  sudo tar xvf intel_sdk_for_opencl_2017_7.0.0.2511_x64.tgz && \
  cd $HOME/intel_sdk_for_opencl_2017_7.0.0.2511_x64 && \
  sudo ./install.sh --silent $HOME/$INTEL_SDK_SILENT_CONFIG

RUN sudo rm $HOME/intel_sdk_for_opencl_2017_7.0.0.2511_x64.tgz && \
  sudo rm $HOME/NVIDIA-Linux-x86_64-$NVIDIA_VERSION.run && \
  sudo rm $HOME/$INTEL_SDK_SILENT_CONFIG

RUN sudo service lightdm start






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


RUN git clone https://github.com/NeuroML/jNeuroML.git && \
  cd jNeuroML && \
  git checkout development && \
  sudo python getNeuroML.py development
  
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
ENV C302_HOME=$HOME/CElegansNeuroML/CElegans/pythonScripts/c302
ENV SIBERNETIC_HOME=$HOME/sibernetic
ENV PYTHONPATH=$PYTHONPATH:$C302_HOME:$SIBERNETIC_HOME



COPY ./master_openworm.py $HOME/master_openworm.py

#RUN sudo chown -R $USER:$USER $HOME
