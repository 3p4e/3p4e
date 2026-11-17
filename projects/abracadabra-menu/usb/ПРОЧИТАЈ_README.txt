ABRACADABRA - дигитално мени / digital menu (works fully offline, no internet needed)

See УПАТСТВО_INSTRUCTIONS.html for the full user guide (Macedonian + English).
TV 1: open TV1.html      TV 2: open TV2.html     (copy this whole folder to the USB stick, keep files together)
Classic look instead: TV1_classic.html / TV2_classic.html
Edit prices: open admin.html in a browser on a computer, change items, press save, then
  copy the generated menu-data.js over the one on the USB stick (menu-data.js is the menu).
URL options: ?mode=day|night (auto: night 19:00-06:00)  &cine=<minutes> (cinematic every N min, 0 = off)

On the TV: plug USB -> open the TV's "Media/USB/Browser" app -> open TV1.html (or TV2.html).
Smart-TV browsers sometimes block local video autoplay or file access. If so, use a cheap
Android TV box / Fire Stick / mini PC with Chrome in kiosk mode:
  chrome --kiosk --autoplay-policy=no-user-gesture-required --allow-file-access-from-files file:///E:/ABRACADABRA_MENU/TV1.html
Needs a 1920x1080 (16:9) screen. Videos are H.264 MP4.
