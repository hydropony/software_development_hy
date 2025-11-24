class ShoppingCart:
    def __init__(self):
        self._products = []

    def add(self, product):
        self._products.append(product)

    def remove(self, product):
        self._products = list(
            filter(lambda p: p.id != product.id, self._products)
        )

    def price(self):
        prices = map(lambda p: p.price, self._products)

        return sum(prices)
