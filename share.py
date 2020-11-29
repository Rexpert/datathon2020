import os
from googletrans import Translator

input_path = r'output/wip'
output_path = r'output/wip_output'
# EDIT THIS -----------------------------------------------------------------------------
wd = r'D:\UNIVERSITY UTARA MALAYSIA\Datathon 2020 - Documents\datathon2020'
filename = r'2.txt'
os.chdir(wd)


with open(os.path.join(input_path, filename), 'r+', encoding='utf-8') as f:
    titles = [line.rstrip('\n') for line in f]

TEST = False
if TEST:
    titles = titles[:10]

counter = 0
limit = len(titles) / 2
en = []
other = []
translator = Translator()

for i, title in enumerate(titles):
    while True:
        try:
            lang = translator.detect(title).lang
            print('now: ' + str(i))
        except:
            print('__________retrying ' + str(i))
            translator = Translator()
            if counter > limit:
                break
            counter += 1
            continue
        break
    if lang == 'en':
        en.append(title)
    else:
        other.append(title)


with open(os.path.join(output_path, "en_" + filename), 'w+', encoding='utf-8') as f:
    for s in en:
        f.write(s + '\n')
with open(os.path.join(output_path, "other_" + filename), 'w+', encoding='utf-8') as f:
    for s in other:
        f.write(s + '\n')

print('job done')
