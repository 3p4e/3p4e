import json
import re

MENU = '/a0/usr/projects/vast/projects/abracadabra-menu/menu-data.js'
OUT = '/a0/usr/projects/vast/projects/abracadabra-menu/clip_specification.json'

with open(MENU, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('window.MENU_DATA =')
brace_count = 0
in_string = False
string_char = None
escape = False
end = -1
for i, ch in enumerate(content[start:]):
    if escape:
        escape = False
        continue
    if ch == '\\':
        escape = True
        continue
    if not in_string and ch in ('"', "'"):
        in_string = True
        string_char = ch
        continue
    if in_string and ch == string_char:
        in_string = False
        string_char = None
        continue
    if not in_string:
        if ch == '{':
            brace_count += 1
        elif ch == '}':
            brace_count -= 1
            if brace_count == 0:
                end = start + i + 1
                break

menu_data_str = content[start:end][len('window.MENU_DATA ='):].strip()
menu_data_str = menu_data_str.replace('null', 'null')
menu_data_str = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', menu_data_str)
menu_data_str = re.sub(r',\s*}', '}', menu_data_str)
menu_data_str = re.sub(r',\s*]', ']', menu_data_str)
menu_data = json.loads(menu_data_str)

print('Categories:', len(menu_data['categories']))

clips = []
item_id = 0

for cat in menu_data['categories']:
    screen = cat.get('screen', 1)
    cat_name = cat.get('name', '')
    cat_id = cat.get('id', '')
    for item in cat.get('items', []):
        name = item.get('name', '')
        price = item.get('price')
        badge = item.get('badge', '')
        available = item.get('available', True)
        if price is None or price == '' or available is False:
            continue
        item_id += 1
        cat_lower = cat_name.lower()
        name_lower = name.lower()

        if 'burger' in cat_lower or '\u0431\u0443\u0440\u0433\u0435\u0440' in cat_lower:
            if '\u0432\u0435\u0433\u0435' in name_lower:
                magic_theme, gesture = 'garden_bloom', 'vine_weave'
            elif '\u0447\u0438\u043a\u0435\u043d' in name_lower or '\u043f\u0438\u043b\u0435\u0448' in name_lower:
                magic_theme, gesture = 'phoenix_feather', 'feather_flutter'
            else:
                magic_theme, gesture = 'forge_fire', 'hammer_strike'
        elif '\u0441\u0435\u043d\u0434\u0432\u0438\u0447' in cat_lower or '\u0442\u043e\u0441\u0442' in cat_lower:
            magic_theme, gesture = 'alchemy_press', 'press_seal'
        elif '\u0432\u0440\u0430\u043f' in cat_lower or 'wrap' in cat_lower:
            magic_theme, gesture = 'spiral_binding', 'spiral_bind'
        elif '\u0441\u043a\u0430\u0440\u0430' in cat_lower or '\u0440\u0430\u0436\u043d\u0438\u0447' in name_lower or '\u043a\u0435\u0431\u0430\u043f\u0447\u0435' in name_lower:
            magic_theme, gesture = 'dragon_breath', 'flame_breathe'
        elif '\u043f\u043e\u0445\u043e\u0432\u0430' in cat_lower or '\u0444\u0440\u0438' in name_lower or '\u043f\u043e\u043c\u0444\u0440\u0438\u0442' in name_lower or '\u0447\u0438\u043f\u0441' in name_lower:
            magic_theme, gesture = 'lightning_cut', 'arc_slash'
        elif '\u0432\u0430\u0444\u043b' in cat_lower or '\u0432\u0430\u0444\u043b\u0430' in name_lower:
            magic_theme, gesture = 'crystal_lattice', 'lattice_weave'
        elif '\u0434\u0435\u0441\u0435\u0440\u0442' in cat_lower or '\u0441\u043b\u0430\u0434\u043a' in name_lower or '\u043d\u0443\u0442\u0435\u043b' in name_lower or '\u043c\u0430\u0440\u043c\u0435\u043b\u0430\u0434' in name_lower or '\u0444\u044a\u0441\u0442\u0430\u043a' in name_lower or '\u0441\u0443\u0442\u043b\u0438\u0458\u0430\u0448' in name_lower:
            magic_theme, gesture = 'sugar_sorcery', 'chocolate_write'
        elif '\u043a\u0430\u0444\u0435' in cat_lower or '\u0435\u0441\u043f\u0440\u0435\u0441\u043e' in name_lower or '\u043a\u0430\u043f\u0443\u0447\u0438\u043d\u043e' in name_lower or '\u043c\u0430\u043a\u0438\u0458\u0430\u0442\u043e' in name_lower or '\u0444\u0440\u0430\u043f' in name_lower or '\u043d\u0435\u0441-\u043a\u0430\u0444\u0435' in name_lower:
            magic_theme, gesture = 'dark_elixir', 'brew_conjure'
        elif '\u043f\u0438\u0458\u0430\u043b\u043e' in cat_lower or '\u043c\u0438\u043b\u043a\u0448\u0435\u0458\u043a' in name_lower or '\u0441\u043c\u0443\u0442\u0438' in name_lower or '\u0447\u0430\u0458' in name_lower or '\u0431\u0430\u0431\u043b' in name_lower or '\u0441\u043e\u043a' in name_lower or '\u0432\u043e\u0434\u0430' in name_lower:
            magic_theme, gesture = 'potion_mastery', 'vortex_stir'
        elif '\u0441\u0430\u043b\u0430\u0442' in cat_lower:
            magic_theme, gesture = 'fresh_conjuration', 'seed_unfurl'
        else:
            magic_theme, gesture = 'unknown', 'cast'

        ascii_name = (name_lower.replace(' ', '_')
                                .replace('+', '')
                                .replace('\u045a', 'lj')
                                .replace('\u0459', 'lj')
                                .replace('\u045f', 'dz')
                                .replace('\u045c', 'kj')
                                .replace('\u0453', 'gj')
                                .encode('ascii', 'ignore').decode('ascii'))
        ascii_name = re.sub(r'[^a-z0-9_]', '', ascii_name) or ('item%d' % item_id)
        clip_id = cat_id + '_' + ascii_name

        clips.append({
            'id': clip_id,
            'item_id': item_id,
            'name': name,
            'category': cat_name,
            'category_id': cat_id,
            'screen': screen,
            'price': price,
            'badge': badge,
            'magic_theme': magic_theme,
            'gesture': gesture,
            'day_clip': 'wand_' + clip_id + '_day.mp4',
            'night_clip': 'wand_' + clip_id + '_night.mp4',
            'duration_sec': 4.0,
            'combos': [],
        })

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump({'generated': '2026-11-18', 'project': 'abracadabra-menu', 'total_clips': len(clips), 'clips': clips}, f, ensure_ascii=False, indent=2)

print('Total priced items needing clips:', len(clips))
print('Saved:', OUT)
print('')
for c in clips:
    print('  %-28s %-30s s%d  %s / %s' % (c['id'], c['name'], c['screen'], c['magic_theme'], c['gesture']))
