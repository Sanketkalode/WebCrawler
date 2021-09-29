import json

from operations import get_base_url, extract, store_in_csv, read_csv, get_url_list, clean_file


def main_previous():
    data = get_previous_data()
    if data['exit_code'] == 0:
        return

    base_url = get_base_url(data['url'])
    if data['current_url']:
        store_in_csv(data['url_list'], data['dp'], data['current_url'], data['url_set'])
    else:
        store_in_csv(data['url_list'], data['dp'], data['url'], data['url_set'])
    data['counter'] = + len(data['url_list'])
    if data['counter'] > data['limit']:
        return

    while data['dp'] < data['depth']:
        urls = read_csv(data['dp'] - 1)
        for url in urls:
            node = extract(url)
            new_url_list = get_url_list(base_url, node)
            store_in_csv(new_url_list, data['dp'], url, data['url_set'])
            data['counter'] += len(new_url_list)
            if data['counter'] > data['limit']:
                break
        data['dp'] += 1
        if data['depth'] == data['dp'] and data['counter'] < data['limit']:
            data['depth'] += 1

    clean_file(data['base_dir'])
    return


def get_previous_data():
    file = open('./save/data.txt', mode='r')
    data = json.load(file)
    file.close()
    return data
