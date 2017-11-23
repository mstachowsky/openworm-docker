#!/bin/bash

set -e

NVIDIA_VERSION=375.82

cd $HOME

wget http://us.download.nvidia.com/XFree86/Linux-x86_64/$NVIDIA_VERSION/NVIDIA-Linux-x86_64-$NVIDIA_VERSION.run
chmod +x NVIDIA-Linux-x86_64-$NVIDIA_VERSION.run
service lightdm stop
./NVIDIA-Linux-x86_64-$NVIDIA_VERSION.run -s -N --no-kernel-module 
service lightdm start

rm NVIDIA-Linux-x86_64-$NVIDIA_VERSION.run

# Fix broken link
mv /usr/lib/x86_64-linux-gnu/libGL.so /usr/lib/x86_64-linux-gnu/libGL.so.BAK
ln -s /usr/lib/libGL.so.1 /usr/lib/x86_64-linux-gnu/libGL.so