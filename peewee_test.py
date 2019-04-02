from peewee import *
import datetime


db = PostgresqlDatabase(database='peweetest', user='postgres', password='11',
                        host='localhost')


class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "categories"
        order_by = ('created_at',)


class Product(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
    price = FloatField(default=None)
    category = ForeignKeyField(Category, related_name='fk_cat_prod', on_update='cascade', on_delete='cascade')
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "products"
        order_by = ('created_at',)


def add_category(name):
    row = Category(name=name.lower().strip(),)
    row.save()


def add_product(name, price, category_name):
    cat_exist = True
    try:
        category = Category.select().where(Category.name == category_name.lower().strip()).get()
    except DoesNotExist as de:
        cat_exist = False
    if cat_exist:
        row = Product(
            name=name.lower().strip(),
            price=price,
            category=category
        )
        row.save()


def find_all_categories():
    return Category.select()


def find_all_products():
    return Product.select()


def find_product(name):
    return Product.get(Product.name == name.lower().strip())


def update_category(id, new_name):
    category = Category.get(Category.id == id)
    category.name = new_name
    category.save()


def delete_category(name):
    category = Category.get(Category.name == name)
    category.delete_instance()

if __name__ == "__main__":
    # try:
    #     db.connect()
    #     Category.create_table()
    # except InternalError as px:
    #     print(str(px))
    # try:
    #     Product.create_table()
    # except InternalError as px:
    #     print(str(px))
    #     db.connect()
    #     add_category('books')
    #     add_category('Electronic Appliances')
    #     add_product('c++', 24.5, 'books')
    #     add_product('juicer', 224.25, 'Electronic Appliances')
    # products = find_all_products()
    # product_data = []
    # for product in products:
    #     product_data.append({
    #         'title': product.name,
    #         'price': product.price,
    #         'category': product.category.name
    #     })
    # print(product_data)
    # p = find_product('c++')
    # print(p.category.name)
    delete_category('books')

