########################################################################################################
# Build container: $ docker build -t openworm .                                                        #
# Run container: $ docker run -ti --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix openworm   #
########################################################################################################

FROM ubuntu:16.04
MAINTAINER David Lung "lungdm@gmail.com"

# Install dependencies
RUN apt-get update && apt-get install -y git maven wget cmake build-essential libxtst-dev python-dev python-pip python-numpy python-tk python-lxml libfreetype6-dev libfreetype6 libpng12-dev libxml2-dev libxslt1-dev libxft-dev openjdk-8-jdk libncurses-dev sudo
RUN apt-get install -y pkg-config

RUN useradd -ms /bin/bash developer

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && mkdir -p /etc/sudoers.d && \
    mkdir -p /home/developer && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown root:root /usr/bin/sudo && chmod 4755 /usr/bin/sudo
    #chown ${uid}:${gid} -R /home/developer


# Install neuron
WORKDIR /home/developer/neuron
RUN wget http://www.neuron.yale.edu/ftp/neuron/versions/v7.4/iv-19.tar.gz
RUN tar -xzvf iv-19.tar.gz -C .
RUN mv iv-19 iv
WORKDIR iv
RUN ./configure --prefix=`pwd`
RUN make
RUN make install

WORKDIR /home/developer/neuron
RUN wget http://www.neuron.yale.edu/ftp/neuron/versions/v7.4/nrn-7.4.tar.gz
RUN tar -xzvf nrn-7.4.tar.gz -C .
RUN mv nrn-7.4 nrn
WORKDIR nrn
RUN ./configure --prefix=`pwd` --with-iv=/home/developer/neuron/iv --with-nrnpython=/usr/bin/python
RUN make
RUN make install
WORKDIR src/nrnpython
RUN python setup.py install

ENV IV=/home/developer/neuron/iv
ENV N=/home/developer/neuron/nrn
ENV NEURON_HOME=/home/developer/neuron/nrn/x86_64/
# for this concrete example, we assume hostcpu is x86_64
ENV CPU=x86_64
ENV PATH="$IV/$CPU/bin:$N/$CPU/bin:$PATH"



# Install openworm/CElegansNeuroML
WORKDIR /home/developer/openworm
RUN git clone https://github.com/openworm/CElegansNeuroML.git
WORKDIR CElegansNeuroML
RUN python setup.py install
RUN pip install libNeuroML
RUN pip install xlrd

# Install openworm/PyOpenWorm
WORKDIR /home/developer/openworm
RUN git clone https://github.com/openworm/PyOpenWorm.git
WORKDIR PyOpenWorm
RUN python setup.py install

WORKDIR /home/developer
USER root
