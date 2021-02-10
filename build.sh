#!/bin/bash

rm -fr build 2>  /dev/null

mkdir build
cd build

mkdir DEBIAN
cat << EOF > DEBIAN/control
Package: justastupidgame
Version: 1.0
Section: custom
Priority: optional
Architecture: all
Essential: no
Maintainer: Jakob Kirsch
Depends: python3, python3-pygame
Description: justastupidgame built from commit $(git rev-parse HEAD | tr -d '\n')
EOF

mkdir opt
mkdir opt/justastupidgame
cp ../LICENSE opt/justastupidgame/
cp ../main.py opt/justastupidgame/ -r
cp ../mods opt/justastupidgame/ -r
cp ../textures opt/justastupidgame/ -r
cp ../threads opt/justastupidgame/ -r
cp ../tile opt/justastupidgame/ -r
cp ../utils opt/justastupidgame/ -r
cp ../watchdog opt/justastupidgame/ -r
cp ../world opt/justastupidgame/ -r
mkdir usr
mkdir usr/bin
ln -s /opt/justastupidgame/main.py usr/bin/justastupidgame

cd ..
dpkg-deb --build build
mv build.deb justastupidgame.deb

rm -fr build
