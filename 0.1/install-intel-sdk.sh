#!/bin/bash

set -e

INTEL_SDK_SILENT_CONFIG=silent-intel-sdk.cfg

cd $HOME

wget http://registrationcenter-download.intel.com/akdlm/irc_nas/vcp/11705/intel_sdk_for_opencl_2017_7.0.0.2511_x64.tgz
tar xvf intel_sdk_for_opencl_2017_7.0.0.2511_x64.tgz
cd intel_sdk_for_opencl_2017_7.0.0.2511_x64
./install.sh --silent $HOME/$INTEL_SDK_SILENT_CONFIG

cd $HOME
rm intel_sdk_for_opencl_2017_7.0.0.2511_x64.tgz
rm $INTEL_SDK_SILENT_CONFIG
