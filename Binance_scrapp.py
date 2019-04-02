from peewee import *
import requests
import datetime

db = PostgresqlDatabase(database='peweetest', user='postgres', password='11',
                        host='localhost')


class Coins(Model):
    id = PrimaryKeyField(null=False)
    symbol = CharField(unique=True)
    price_change = FloatField()
    percent_price_change = FloatField()
    weighted_avg_price = FloatField()
    prev_close_price = FloatField()
    last_price = FloatField()
    last_qty = FloatField()
    bid_price = FloatField()
    ask_price = FloatField()
    open_price = FloatField()
    high_price = FloatField()
    low_price = FloatField()
    volume = FloatField()
    quote_volume = FloatField()
    open_time = TimestampField()
    close_time = TimestampField()
    first_id = IntegerField()
    last_id = IntegerField()
    count = IntegerField()

    class Meta:
        db_table = 'coins'
        database = db


if __name__ == "__main__":
    db.connect()
    Coins.create_table()

    data = requests.get('https://api.binance.com/api/v1/ticker/24hr').json()

    for coin in data:
        exist = Coins.select().where(Coins.symbol==coin['symbol'])

        if exist:
            print('Обновление цены {}'.format(coin['symbol']))
            Coins.update(
                last_price=coin['lastPrice'],
                last_qty=coin['lastQty'],
                bid_price=coin['bidPrice'],
                ask_price=coin['askPrice'],
            ).where(Coins.symbol == coin['symbol']).execute()
        else:
            print('Добавление записи {}'.format(coin['symbol']))
            Coins.create(
                symbol=coin['symbol'],
                price_change=coin['priceChange'],
                percent_price_change=coin['priceChangePercent'],
                weighted_avg_price=coin['weightedAvgPrice'],
                prev_close_price=coin['prevClosePrice'],
                last_price=coin['lastPrice'],
                last_qty=coin['lastQty'],
                bid_price=coin['bidPrice'],
                ask_price=coin['askPrice'],
                open_price=coin['openPrice'],
                high_price=coin['highPrice'],
                low_price=coin['lowPrice'],
                volume=coin['volume'],
                quote_volume=coin['quoteVolume'],
                open_time=int(coin['openTime'] / 1000),
                close_time=int(coin['closeTime'] / 1000),
                first_id=coin['firstId'],
                last_id=coin['lastId'],
                count=coin['count'],
            )
    sorted_coins = Coins.select().order_by(Coins.volume.desc())

    print('Сортировка монет по количеству за 24 часа')
    for coin in sorted_coins:
        print(coin.symbol, coin.volume)

    print('@' * 30)
    bnd_count = Coins.select().where(Coins.symbol.endswith('BNB')).count()
    print('Количество монет с BNB {}'.format(bnd_count))

