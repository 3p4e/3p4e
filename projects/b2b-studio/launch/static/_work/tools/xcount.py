# X (Twitter) weighted length, twitter-text v3 config: chars in the ranges below weigh 1, everything else 2;
# URLs count 23. Also prints plain len() for bios/titles.
import re, sys, unicodedata
R = [(0, 4351), (8192, 8205), (8208, 8223), (8242, 8247)]
URL = re.compile(r'(?<![@\w])(?:https?://)?(?:www\.)?[a-z0-9-]+\.(?:mk|com|org|net)(?:/\S*)?', re.I)
def xlen(s):
    s = unicodedata.normalize('NFC', s); n = 0
    for m in URL.finditer(s): n += 23
    s2 = URL.sub('', s)
    for ch in s2: n += 1 if any(a <= ord(ch) <= b for a, b in R) else 2
    return n
if __name__ == '__main__':
    t = sys.stdin.read().rstrip('\n'); print('x', xlen(t), 'len', len(t), 'hashtags', len(re.findall(r'#\w+', t)))
