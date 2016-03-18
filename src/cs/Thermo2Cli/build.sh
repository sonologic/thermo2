#!/bin/sh

set -e

xbuild /p:Configuration=Debug
xbuild /p:Configuration=Release

