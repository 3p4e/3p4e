import os, re, shutil

D = '/a0/usr/projects/vast/media/origami_clips'
seed_map = {
    '800': 'or_01_corruption_revealed',
    '801': 'or_02_hunter_descends',
    '802': 'or_03_thousand_cranes',
    '803': 'or_04_stain_devours',
    '804': 'or_05_tar_tide',
    '805': 'or_06_blade_splits_tide',
    '806': 'or_07_colossus_against_cathedral',
    '807': 'or_08_sphere_of_annihilation',
    '808': 'or_09_thousandfold_dawn',
    '809': 'or_10_final_unfold',
    '810': 'or_11_spear_pierce',
    '811': 'or_12_annihilation_ascension',
}

os.chdir(D)
for f in os.listdir('.'):
    if not f.endswith('.mp4'):
        continue
    m = re.search(r'_(\d{3})_', f)
    if not m:
        print('NO_SEED', f)
        continue
    beat = seed_map.get(m.group(1))
    if not beat:
        print('UNMAPPED', f)
        continue
    dst = beat + '.mp4'
    if os.path.exists(dst):
        print('EXISTS_SKIP', f)
        continue
    shutil.move(f, dst)
    print(m.group(1), '->', dst)

print('===FINAL===')
for f in sorted(os.listdir('.')):
    if f.endswith('.mp4'):
        print(f)
