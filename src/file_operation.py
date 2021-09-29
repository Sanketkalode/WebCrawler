import os

from operations import get_base_url


def create_dir(name, path=None):
    if path:
        os.mkdir(path + '/' + name)
    else:
        os.mkdir(name)


def get_url_dir(url):
    base_url = get_base_url(url)

    list_dir = os.listdir('./save')

    flag = False
    base_dir = base_url.split('//')[1]
    if base_dir.startswith('www'):
        base_dir = base_dir.split('.')[1]
    else:
        base_dir = base_dir.split('.')[0]

    for ld in list_dir:
        if ld == base_dir:
            flag = True
            break

    if not flag:
        create_dir('./save/' + base_dir)

    return base_url, base_dir


def update_main_csv(url, limit, visit, scrapped):
    main_url_csv = open('./save/main_url_csv.csv', mode='a')

    line = url + ',' + str(limit) + ',' + str(visit) + ',' + str(scrapped)

    main_url_csv.write(line+'\n')

    main_url_csv.close()
