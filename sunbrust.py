import os
import re
import json
import pandas as pd

from datetime import datetime
from pyecharts.charts import Sunburst
from pyecharts import options as opts

# set current working env
TEST = False
data_path = r'data/Price Intelligence/'
output_path = r'output/'
wd = r'D:\UNIVERSITY UTARA MALAYSIA\Datathon 2020 - Documents\datathon2020'
os.chdir(wd)

rx_csv = re.compile(r'.*\.csv$')

filenames = os.listdir(data_path)
filenames = [os.path.join(wd, data_path, name)
             for name in filenames if rx_csv.match(name)]

level = 3  # 6 to disable level limit, {1-5} to enable level limiting
pi_all = pd.DataFrame()


def best_cat_det(item_cat, item_cat_det, item_title):
    '''
    Find the best category detail with the following condition:
    1. no 'home/...'
    2. no '.../<title>'
    3. end with '.../<item_category>
    4. fuzzy match with category
    5. shorter if possible
    '''
    rx_cat = re.compile(r';|,\s')
    categories = re.split(rx_cat, item_cat.lower())

    def slim(category, cat_det):
        rx1 = re.compile(r'^home/(.+)')
        rx2 = re.compile(
            r'^(.+/(\w+\s)?{}((-|\s)\w+)?)(/.+)?$'.format(category))
        rx3 = re.compile(r'^(.+/{})(/.+)?$'.format(category))
        rx4 = re.compile(r'^(.+/{})/.+$'.format(category))
        rx5 = re.compile(r'^([^/]+' + r'/[^/]+' * (level - 1) + r')/.+')
        if(rx2.match(cat_det)):
            cat_det = re.sub(rx1, r'\g<1>', cat_det)
            cat_det = re.sub(rx2, r'\g<1>', cat_det)
            cat_det = re.sub(rx3, r'\g<1>', cat_det)
            cat_det = re.sub(rx4, r'\g<1>', cat_det)
            if len(re.findall(r'/', cat_det)) > (level - 1):
                cat_det = re.sub(rx5, r'\g<1>', cat_det)
        else:
            cat_det = ''

        return cat_det

    return max([slim(category, item_cat_det) for category in categories])


for file in filenames:
    pi = pd.read_csv(file)
    if TEST:
        if file == filenames[0]:
            pi_all = pi.head(100).iloc[:, 2:5]
            break
    else:
        pi_all = pi_all.append(pi.iloc[:, 2:5])  # Concatenate all files HERE

cats = pi_all\
    .apply(lambda r: best_cat_det(r.item_category,
                                  r.item_category_detail,
                                  r.title), axis=1)\
    .apply(lambda r: r.split('/'))

data = []
for cat in cats:
    d = data
    for item in cat:
        lst = list(filter(lambda x: x['name'] == item, d))
        if len(lst) == 0:  # if item does not exist, add new dict, else value increse
            d.append(dict(name=item, value=1, children=[]))
        else:
            lst[0]['value'] += 1
        idx = d.index(list(filter(lambda x: x['name'] == item, d))[0])
        d = d[idx]['children']


def rm_mt_child(elm):
    '''
    delete children with empty list
    '''
    if isinstance(elm, list):
        for item in elm:
            rm_mt_child(item)
    else:
        rm_mt_child(elm['children'])
        if len(elm['children']) == 0:
            elm.pop('children')


rm_mt_child(data)

# -----------------------------------------------------------
# Begin HERE to load json instead recalculate all over again
# -----------------------------------------------------------
SAVE = False
if SAVE:
    with open(os.path.join(output_path, 'output_file.json'), 'w+') as fout:
        json.dump(data, fout)
else:
    with open(os.path.join(output_path, 'output_file.json'), 'r+') as fout:
        data = json.load(fout)
    # print(data)


def top_n(n, lst, add_other=True):
    '''
    only show top n in sunburst
    '''
    values = [d['value'] for d in lst]
    idx = sorted(range(len(values)), key=lambda i: values[i])[-n:]
    top = dict(name='top 5', children=[])
    other = dict(name='other', children=[])
    value = 0
    for i, d in enumerate(lst):
        if i not in idx:
            value += d['value']
            other['children'].append(d)
        else:
            top['children'].append(d)
    # other['value'] = value

    # top = sorted(top, key=lambda i: i['value'], reverse=True)
    # top.append(other) if add_other else None
    return [top, other]


data = top_n(5, data, True)

# Fill color


def fill_color(elm, color):
    '''
    delete children with empty list
    '''
    if isinstance(elm, list):
        for item in elm:
            fill_color(item, color)
    else:
        try:
            fill_color(elm['children'], color)
        except:
            pass
        elm['itemStyle'] = dict(color=color)


fill_color(data[1], "#aaaaaa")
fill_color(data[0], "#ca8622")
fill_color(data[0]['children'][0], "#c23531")
fill_color(data[0]['children'][1], "#2f4554")
fill_color(data[0]['children'][2], "#61a0a8")
fill_color(data[0]['children'][3], "#d48265")
fill_color(data[0]['children'][4], "#749f83")

SAVE = True
if SAVE:
    c = (
        Sunburst(init_opts=opts.InitOpts(width="1000px", height="600px"))
        .add(
            "",
            data_pair=data,
            highlight_policy="ancestor",
            radius=[0, "95%"],
            sort_="asc",
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Total Number of Sales by Categories \n(Top 5 and others)"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False, formatter="{b}"))
        .render(os.path.join(output_path, "html_files", "top5_other_categories.html"))
    )
print('done')
