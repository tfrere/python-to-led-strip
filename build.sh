#!/bin/bash

# conda activate env
echo "conda activate env"
eval "$(conda shell.bash hook)"
conda activate audio-2-led

echo "cleaning old build files"
rm -Rf build
rm -Rf dist
rm -Rf **/*.pyc
echo "building new one"
pyinstaller --onefile main.py -n python-to-led-strip
