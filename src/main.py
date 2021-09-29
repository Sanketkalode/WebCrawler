import csv
import os
import sys

from exit_ops import save_data
from file_operation import get_url_dir, update_main_csv, create_dir
from operations import extract, get_url_list, store_in_csv, read_csv, clean_file
from previous import main_previous


def crawler(base_dir, base_url, url, limit):

    depth = 3
    dp = 1
    counter = 0
    new_url_list = []
    u = ''
    try:
        url_set = set()
        node = extract(url)

        url_list = get_url_list(base_url, node)
        store_in_csv(url_list, dp, url, url_set)
        counter = len(url_list)

        dp = 2

        while dp <= depth:
            urls = read_csv(dp - 1)
            for u in urls:
                node = extract(u)
                new_url_list = get_url_list(base_url, node)
                store_in_csv(new_url_list, dp, u, url_set)
                counter += len(new_url_list)
                print("Counter: "+counter)
                if counter > limit:
                    break
            dp += 1
            if depth == dp and counter < limit:
                depth += 1

        clean_file(base_dir)
        return counter, len(url_set)
    except Exception as ex:
        data = dict(exit_code=1, error_message=ex, url=url, counter=counter, url_list=new_url_list,
                    limit=limit, depth=depth, dp=dp, current_url=u)
        save_data(data)
        sys.exit(1)


def main(url, limit=200):
    if not os.path.isdir('save'):
        create_dir('save')
    if os.path.exists('data.txt'):
        main_previous()

    # Check whether previous execution is completed
    try:
        main_url_csv = open('./save/main_url_csv.csv', mode='r')
    except FileNotFoundError:
        main_url_csv = open('./save/main_url_csv.csv', mode='w')
        main_url_csv.close()
        main_url_csv = open('./save/main_url_csv.csv', mode='r')

    csv_reader = csv.reader(main_url_csv, delimiter=',')
    for row in csv_reader:
        if row[0] == url and row[1] == str(limit):
            print("Url already scrapped")
            sys.exit(0)
    main_url_csv.close()

    # main program execution
    base_url, base_dir = get_url_dir(url)

    visit, scrapped = crawler(base_dir, base_url, url, limit)
    update_main_csv(url, limit, visit, scrapped)
    data={
        'exit_code':0
    }
    save_data(data)


if __name__ == '__main__':
    url = "https://timesofindia.indiatimes.com/world/south-asia/former-afghanistan-officials-announce-govt-in-exile-saleh-to-lead/articleshow/86617729.cms"
    main(url, 100)
