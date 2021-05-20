#!/usr/bin/env python
# coding: utf-8

"""
    Simple map analysis for COVID-19 in Taiwan
"""
import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Map
from pyecharts import options as opts
from opencc import OpenCC


# get the data from the public website

url = 'https://covid-19.nchc.org.tw/'
html = requests.get(url,verify=False)


# restruct the data for rendering the map

text = html.text
soup = BeautifulSoup(text, 'lxml')
city_list = soup.find_all('button',{'class':'btn btn-success btn-lg'})
city_confirmed = {}
cc = OpenCC('t2s')

for i in city_list:
    s = i.get_text().split()
    s[0] = cc.convert(s[0])
    s[1] = int(s[1].split('+')[0])
    city_confirmed[s[0]] = s[1]
print(city_confirmed)

# visualization function

def confirmed_maps():
    map_chart = Map()
    map_chart.add(
    '疫情地圖',
    [list(i) for i in zip(city_confirmed.keys(),city_confirmed.values())],
    maptype='台湾',
    is_map_symbol_show=True,
    label_opts=opts.LabelOpts(is_show=False)
    )
    
    map_chart.set_global_opts(
        title_opts=opts.TitleOpts(
            title='台灣'
        ),
        visualmap_opts=opts.VisualMapOpts(
            is_piecewise=True,
            pieces = [
            {"min":1, "max":50, "label": "1-50人", "color":"#FFE6BE"},
            {"min":51, "max":100, "label": "51-100人", "color":"#FFB769"},
            {"min":101, "max":300, "label": "101-300人", "color":"#FF8F66"},
            {"min":301, "max":1000, "label": "301-1000人", "color":"#ED514E"}
        ]
        )
    )
    map_chart.render('confirmed_map.html')

confirmed_maps()

