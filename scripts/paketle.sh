#!/bin/sh
# Claude uygulamasına yüklenecek zip'i üretir: dist/zihin-haritasi.zip (içinde klasör kökte).
set -e
cd "$(dirname "$0")/../skills"
rm -f ../dist/zihin-haritasi.zip
zip -rq -X ../dist/zihin-haritasi.zip zihin-haritasi -x '*/__pycache__/*' '*.DS_Store'
echo "dist/zihin-haritasi.zip"
