# Runs ON the India server. Builds /opt/stacks/ai-studio-pitch/h3_block.conf for nginx's geo module from the free DB-IP country
# database (CC BY 4.0, https://db-ip.com): every IPv4/IPv6 range of a country where MiniMax H3 outputs may NOT be displayed
# (licence "Applicable Territory" = worldwide minus EU, UK, South Korea, USA) maps to 1. Refresh monthly (cron).
import csv, gzip, ipaddress, urllib.request, datetime, os, sys
EU = "AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE".split()
EU_OUTER = "GF GP MQ RE YT MF".split()                       # EU outermost regions
UK = "GB GI JE GG IM".split(); US = "US PR GU VI AS MP UM".split(); KR = ["KR"]
BLOCK = set(EU + EU_OUTER + UK + US + KR)
d = datetime.date.today(); url = None
for m in (d, d.replace(day=1) - datetime.timedelta(days=1)):
    u = f"https://download.db-ip.com/free/dbip-country-lite-{m:%Y-%m}.csv.gz"
    try: data = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (bigdogma geo list)"}), timeout=120).read(); url = u; break
    except Exception as e: print("miss", u, e)
if not url: sys.exit("no DB-IP file")
out = ["# generated %s from %s (DB-IP Lite, CC BY 4.0) - countries where MiniMax H3 outputs may not be displayed" % (d, url)]
v4, v6 = [], []
for a, b, cc in csv.reader(gzip.decompress(data).decode().splitlines()):
    if cc not in BLOCK: continue
    for net in ipaddress.summarize_address_range(ipaddress.ip_address(a), ipaddress.ip_address(b)): (v4 if net.version == 4 else v6).append(net)
nets = list(ipaddress.collapse_addresses(v4)) + list(ipaddress.collapse_addresses(v6))   # merge neighbours: far fewer entries for nginx
out += [f"{n} 1;" for n in nets]; n = len(nets)
if n < 50000: sys.exit(f"only {n} networks - refusing to replace the list")   # a truncated download must never open the gate
# write in place (same inode): the file is bind-mounted into the nginx container, a renamed file would not be seen there
import shutil; tmp = "/opt/stacks/ai-studio-pitch/h3_block.conf.tmp"; open(tmp, "w").write("\n".join(out) + "\n"); shutil.copyfile(tmp, "/opt/stacks/ai-studio-pitch/h3_block.conf"); os.remove(tmp)
print("blocked networks", n)
