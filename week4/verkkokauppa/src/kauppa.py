from ostoskori import ShoppingCart

class Shop:
    def __init__(self, warehouse, bank, reference_generator):
        self._warehouse = warehouse
        self._bank = bank
        self._reference_generator = reference_generator
        self._shop_account = "33333-44455"


    def start_shopping(self):
        self._shopping_cart = ShoppingCart()

    def remove_from_cart(self, id):
        product = self._warehouse.get_product(id)
        self._shopping_cart.remove(product)
        self._warehouse.return_to_warehouse(product)

    def add_to_cart(self, id):
        if self._warehouse.balance(id) > 0:
            product = self._warehouse.get_product(id)
            self._shopping_cart.add(product)
            self._warehouse.take_from_warehouse(product)

    def account_payment(self, name, account_number):
        reference = self._reference_generator.new()
        amount = self._shopping_cart.price()

        return self._bank.bank_transfer(name, reference, account_number, self._shop_account, amount)
