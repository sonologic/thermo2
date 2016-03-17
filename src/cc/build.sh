#!/bin/sh

set -e

rm -Rf build
mkdir build
cd build
cmake ..
make thermo2cli
