#!/usr/bin/env sh
# Builds dist/ABRACADABRA_MENU_USB.zip: the menu board as a self-contained, offline folder for a USB stick.
# Contents: the boards, admin page, menu-data.js, assets (fonts, stills, 13 video clips), TV launchers and README from usb/.
set -e
cd "$(dirname "$0")"
OUT=$(mktemp -d)/ABRACADABRA_MENU
mkdir -p "$OUT/preview" dist
cp -r assets cinematic-board.html index.html admin.html menu-data.js "$OUT/"
cp screen*_*.png cinematic_summon.png "$OUT/preview/"
cp usb/* "$OUT/"
rm -f dist/ABRACADABRA_MENU_USB.zip
(cd "$(dirname "$OUT")" && zip -qr "$OLDPWD/dist/ABRACADABRA_MENU_USB.zip" ABRACADABRA_MENU)
echo "built dist/ABRACADABRA_MENU_USB.zip"
