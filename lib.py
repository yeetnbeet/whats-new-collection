import datetime
from shpy import ProductsPy,CollectionPy

def get_month_ago():
    time = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    return str(time)

def products_from_month_ago(month_ago):
    p = ProductsPy()
    p.PRODUCT_LIST = []
    ids = []
    p.getAllProductsByStatus(status="active&limit=250&published_at_min="+month_ago)
    for item in p.PRODUCT_LIST:
        print(item["title"])
        ids.append(item["id"])
    return ids

def older_products(month_ago):
    p = ProductsPy()
    p.PRODUCT_LIST = []
    ids = []
    p.getAllProductsByStatus(status="active&limit=250&collection_id=404829798645&published_at_max="+month_ago)
    for item in p.PRODUCT_LIST:
        print(item["title"])
        ids.append(item["id"])
    return ids

def remove_old_products(oldproducts):
    collection = CollectionPy()
    for product in oldproducts:
        r = collection.removeFromCollection(product,404829798645)


def add_new_products(newproducts):
    collection = CollectionPy()
    for product in newproducts:
        collection.addItemToExistingCollection(product,404829798645)

    

