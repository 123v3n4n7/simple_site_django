import csv
from peewee import *


db = PostgresqlDatabase(database='test', user='postgres', password='11',
                        host='localhost')


class Coin(Model):
    name = CharField()
    link = TextField()
    price = CharField()

    class Meta:
        database = db


def csv_reader(file):
    headers = ['name', 'link', 'price']
    reader = csv.DictReader(file, fieldnames=headers)

    coins = list(reader)

    # 1 способ записи в таблицу (ДОЛГИЙ)
    # for row in coins:
    #     coin = Coin(name=row['name'], url=row['link'], price=row['price'])
    #     coin.save()

    # 2 способ записи в таблицу
    # with db.atomic():
    #     for row in coins:
    #         Coin.create(**row)

    # 3 способ(ЛУЧШИЙ) разбивает список на куски и записывает в их БД,
    # сокращается количество итераций в цикле
    with db.atomic():
        for index in range(0, len(coins), 100):
            Coin.insert_many(coins[index:index+100]).execute()


def main():
    db.connect()
    db.create_tables([Coin])

    with open('cmc.csv') as file:
        csv_reader(file)


if __name__ == "__main__":
    main()
