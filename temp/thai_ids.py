import json, os, glob
base = 'data/recipes/intl/thai'
ids = sorted(os.path.basename(f)[:-5] for f in glob.glob(base + '/*.json'))
open('temp/thai_ids.txt', 'w', encoding='utf-8').write('\n'.join(ids))
print(len(ids))
