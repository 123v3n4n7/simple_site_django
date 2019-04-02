import requests
import csv


def get_html(url):
    response = requests.get(url)
    return response.text


def write_csv(data):
    with open('sites_list.csv', 'a') as file:
        order = ['name', 'link', 'description', 'traffic', 'percent']
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)


def main():
    url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page=1'
    response = get_html(url)
    data = response.strip().split('\n')[1:]
    for row in data:
        columns = row.strip().split('\t')
        name = columns[0]
        link = columns[1]
        description = columns[2]
        traffic = columns[3]
        percent = columns[4]

        data = {'name': name, 'link': link, 'description': description,
                'traffic': traffic, 'percent': percent}

        write_csv(data)

if __name__ == "__main__":
    main()
