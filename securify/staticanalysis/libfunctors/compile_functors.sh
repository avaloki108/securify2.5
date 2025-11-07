#!/usr/bin/env bash
set -euo pipefail

g++ -std=c++17 -O2 -fPIC -c functors.cpp -o functors.o
g++ -shared -o libfunctors.so functors.o
rm functors.o
