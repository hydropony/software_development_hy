from tuote import Product
from kirjanpito import ledger as default_ledger


class Warehouse:
    def __init__(self, ledger=default_ledger):
        self._ledger = ledger
        self._stock = {}
        self._initialize_products()

    def get_product(self, id): #test
        products = self._stock.keys()

        for product in products:
            if product.id == id:
                return product

        return None

    def balance(self, id): #test
        product = self.get_product(id)

        return self._stock[product]

    def take_from_warehouse(self, product): #test
        stock_balance = self.balance(product.id)

        self._stock[product] = stock_balance - 1

        self._ledger.add_transaction(f"took from warehouse {product}")

    def return_to_warehouse(self, product): #$test
        stock_balance = self.balance(product.id)

        self._stock[product] = stock_balance + 1

        self._ledger.add_transaction(f"returned to warehouse {product}")

    def _initialize_products(self):
        self._stock[Product(1, "Koff Portteri", 3)] = 100
        self._stock[Product(2, "Fink Bräu I", 1)] = 25
        self._stock[Product(3, "Sierra Nevada Pale Ale", 5)] = 30
        self._stock[Product(4, "Mikkeller not just another Wit", 7)] = 40
        self._stock[Product(5, "Weihenstephaner Hefeweisse", 4)] = 15


warehouse = Warehouse()
