import re
import os
import math
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Scatter, Line
from statsmodels.api import OLS, WLS, add_constant
import scipy.stats as st

TEST = False
SEED = 1234
data_path = r'data/Price Intelligence/'
output_path = r'output/'
wd = r'D:\UNIVERSITY UTARA MALAYSIA\Datathon 2020 - Documents\datathon2020'
os.chdir(wd)

rx_csv = re.compile(r'.*\.csv$')

filenames = os.listdir(data_path)
filenames = [os.path.join(wd, data_path, name)
             for name in filenames if rx_csv.match(name)]

pi_all = pd.DataFrame()
for file in filenames:
    pi = pd.read_csv(file)
    if TEST:
        if file == filenames[0]:
            pi_all = pi.head(1000).iloc[:, [2, 6, 7]]
            break
    else:
        # Concatenate all files HERE
        pi_all = pi_all.append(pi.iloc[:, [2, 6, 7]])

rx_cat = re.compile(r'.*/{}/.*'.format(r'mother & baby'))
prices = pi_all.loc[pi_all.item_category_detail.str.contains(
    rx_cat), ['price_ori', 'price_actual']]

Y = prices.price_actual
X = prices.price_ori
X = add_constant(X)
ols = OLS(Y, X).fit()
prices['price_actual_ols'] = ols.fittedvalues

# https://stats.stackexchange.com/questions/246085/how-to-determine-weights-for-wls-regression-in-r
# https://stats.stackexchange.com/questions/97832/how-do-you-find-weights-for-weighted-least-squares-regression
w = 1 / (OLS(abs(ols.resid), ols.fittedvalues).fit().fittedvalues ** 2)

wls = WLS(Y, X, weights=w).fit()
prices['price_actual_wls'] = wls.fittedvalues

# https://select-statistics.co.uk/calculators/sample-size-calculator-population-proportion/
me = 0.01  # margin of error
p = 0.05  # sample proportion
ci = 0.95  # confidence interval
N = len(prices)  # population size
# z score for two tail norm dist
z = st.norm.ppf((1 + ci) / 2)
x = (z ** 2) * p * (1 - p) / (me ** 2)
n = N * x / (x + N - 1)
n = math.ceil(n)  # final sample size

# take sample for plotting chart only to save resources
# regression modelling still using the population data
prices = prices.sample(n=n, random_state=SEED)

scatter = (
    Scatter(init_opts=opts.InitOpts())
    .add_xaxis(xaxis_data=prices.price_ori.to_list())
    .add_yaxis(
        series_name="Original Data points",
        y_axis=prices.price_actual.to_list(),
        symbol_size=5,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_series_opts()
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="value",
            name="Original Price",
            name_location="middle",
            name_gap=25,
            splitline_opts=opts.SplitLineOpts(is_show=True)
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name_location="middle",
            name="Actual Price",
            name_gap=40,
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        legend_opts=opts.LegendOpts(pos_top="bottom"),
        title_opts=opts.TitleOpts("Prediction on Actual Price with Original Price on Mother & Baby category \nusing Weighted Least Squares Regression",
                                  subtitle="1", item_gap=100, title_textstyle_opts=opts.TextStyleOpts(align='middle'))
    )
)

line = (
    Line()
    .set_series_opts()
    .add_xaxis(xaxis_data=prices.price_ori.to_list())
    .add_yaxis(
        series_name="WLS prediction",
        y_axis=prices.price_actual_wls.to_list(),
        # symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    )
)

scatter.overlap(line)
scatter.render(os.path.join(output_path, 'html_files', 'scatter.html'))
