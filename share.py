import os
import time
from multiprocessing import Pool
from googletrans import Translator

input_path = r'output/wip'
output_path = r'output/wip_output'
wd = r'D:\UNIVERSITY UTARA MALAYSIA\Datathon 2020 - Documents\datathon2020'
os.chdir(wd)


def core(n):
    filename = r'{}.txt'.format(n)
    with open(os.path.join(input_path, filename), 'r+', encoding='utf-8') as f:
        titles = [line.rstrip('\n') for line in f]
    # titles = titles[:10]
    counter = 0
    limit = len(titles) / 2
    en = []
    other = []
    translator = Translator()
    for i, title in enumerate(titles):
        while True:
            try:
                lang = translator.detect(title).lang
                print('Task {} - now: {}'.format(n, i))
            except:
                print('Task {} - __________retrying: {}'.format(n, i))
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
    with open(os.path.join(output_path, "en_{}".format(filename)), 'w+', encoding='utf-8') as f:
        for s in en:
            f.write(s + '\n')
    with open(os.path.join(output_path, "other_{}".format(filename)), 'w+', encoding='utf-8') as f:
        for s in other:
            f.write(s + '\n')


def sub_task(n):
    print('Run task {} ({})...'.format(n, os.getpid()))
    start = time.time()
    core(n)
    end = time.time()
    print('Task {} runs {.2f} seconds.'.format(n, (end - start)))


if __name__ == '__main__':
    start_main = time.time()
    print('Parent process {}.'.format(os.getpid()))
    n = 10
    p = Pool(n)
    for i in range(n):
        p.apply_async(sub_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    end_main = time.time()
    print('All tasks run {0.2f} seconds.'.format(end_main - start_main))
