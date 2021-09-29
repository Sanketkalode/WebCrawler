import os

import lxml.html
import requests
import csv
from bs4 import UnicodeDammit
from requests.exceptions import ConnectionError


def extract(url):
    try:
        response = requests.get(url)
        doc = lxml.html.fromstring(UnicodeDammit(response.content).unicode_markup)
        return doc
    except ConnectionError:
        raise ConnectionError(url)


def get_base_url(url):
    base_url = ''

    if '.in/' in url:
        base_url = url.split('.in/')[0] + '.in/'
    elif '.com/' in url:
        base_url = url.split('.com/')[0] + '.com/'

    return base_url


def get_url_list(base_url, top_node):
    new_list = []

    href_list = top_node.xpath('//a')
    for href in href_list:
        if href.get('href') and href.text_content():
            if base_url in href.get('href') and base_url != href.get('href') and url_exclusion(href.get('href')) and href.get('href').endswith(('.cms','.html')):
                new_list.append(href.get('href'))
            continue

    return new_list


def store_in_csv(url_list, depth, url, url_set):
    try:
        file = open('tempurl.csv', mode='a')
        fieldnames = ['depth', 'parent_url', 'url']
        url_writer = csv.DictWriter(file, fieldnames=fieldnames)

        url_writer.writeheader()
        for u in url_list:
            if u not in url_set:
                url_writer.writerow({'depth': depth, 'parent_url': url, 'url': u})
                url_set.add(u)
        file.close()
    except Exception as e:
        print(e.args)


def read_csv(depth):
    url_list = []
    try:
        file = open('tempurl.csv', mode='r')
        reader = csv.DictReader(file)
        for row in reader:
            if row['depth'] == str(depth):
                url_list.append(row['url'])

        file.close()
    except Exception as e:
        print(e)
    return url_list


def url_exclusion(url):
    exclusion_list = ['/videos', '/photogallery','photos', 'opinion', 'astrology', 'destinations', 'articleshow']
    for el in exclusion_list:
        if el in url:
            return False
    return True


def clean_file(base_dir):
    in_file = open('tempurl.csv', 'r')
    filename = './save/' + base_dir + '/urlcsv.csv'
    out_file = open(filename, 'a')

    lines = in_file.readlines()

    for line in lines:
        st = line.split(',')
        if st[0].isdigit():
            out_file.write(line)

    in_file.close()
    out_file.close()
    os.remove('tempurl.csv')
