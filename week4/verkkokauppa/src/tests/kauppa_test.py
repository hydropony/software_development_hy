import unittest
from unittest.mock import Mock, ANY
from kauppa import Shop
from viitegeneraattori import ReferenceGenerator
from varasto import Warehouse
from tuote import Product
from kirjanpito import ledger

class TestShop(unittest.TestCase):
    def setUp(self):
        self.bank_mock = Mock()
        self.reference_generator_mock = Mock()

        # always return value 42
        self.reference_generator_mock.new.return_value = 42

        self.warehouse_mock = Mock()

        # create implementation for balance method
        def warehouse_balance(product_id):
            if product_id == 1:
                return 10

        # create implementation for get_product method
        def warehouse_get_product(product_id):
            if product_id == 1:
                return Product(1, "milk", 5)

        # apply implementations
        self.warehouse_mock.balance.side_effect = warehouse_balance
        self.warehouse_mock.get_product.side_effect = warehouse_get_product

        # initialize shop
        self.shop = Shop(self.warehouse_mock, self.bank_mock, self.reference_generator_mock)

    def test_bank_transfer_is_called_when_purchase_is_made(self):
        # make purchases
        self.shop.start_shopping()
        self.shop.add_to_cart(1)
        self.shop.account_payment("pekka", "12345")

        # verify that bank_transfer method was called
        self.bank_mock.bank_transfer.assert_called()
        # for now we don't care about the arguments passed to the call

    def test_bank_transfer_called_with_correct_parameters(self):
        self.shop.start_shopping()
        self.shop.add_to_cart(1)
        self.shop.account_payment("pekka", "12345")

        self.bank_mock.bank_transfer.assert_called_with(
            "pekka",
            42,
            "12345",
            ANY,
            5
        )
    
    def test_bank_transfer_called_with_correct_parameters_two_products(self):
        def warehouse_balance(product_id):
            if product_id == 1 or product_id == 2:
                return 10

        def warehouse_get_product(product_id):
            if product_id == 1:
                return Product(1, "milk", 5)
            elif product_id == 2:
                return Product(2, "bread", 3)
            
        self.warehouse_mock.balance.side_effect = warehouse_balance
        self.warehouse_mock.get_product.side_effect = warehouse_get_product

        self.shop = Shop(self.warehouse_mock, self.bank_mock, self.reference_generator_mock)

        self.shop.start_shopping()
        self.shop.add_to_cart(2)
        self.shop.add_to_cart(1)
        self.shop.account_payment("pekka", "12345")

        self.bank_mock.bank_transfer.assert_called_with(
            "pekka",
            42,
            "12345",
            ANY,
            8
        )

    def test_new_customer(self):
        def warehouse_balance(product_id):
            if product_id == 1 or product_id == 2:
                return 10

        def warehouse_get_product(product_id):
            if product_id == 1:
                return Product(1, "milk", 5)
            elif product_id == 2:
                return Product(2, "bread", 3)
            
        self.warehouse_mock.balance.side_effect = warehouse_balance
        self.warehouse_mock.get_product.side_effect = warehouse_get_product

        self.shop = Shop(self.warehouse_mock, self.bank_mock, self.reference_generator_mock)

        self.shop.start_shopping()
        self.shop.add_to_cart(1)
        self.shop.add_to_cart(1)
        self.shop.account_payment("pekka", "12345")
        self.shop.start_shopping()
        self.shop.add_to_cart(2)
        self.shop.account_payment("jere", "99999") 

        self.bank_mock.bank_transfer.assert_called_with(
            "jere",
            42,
            "99999",
            ANY,
            3
        )

    def test_new_reference_number_for_each_payment(self):
        self.shop.start_shopping()
        self.shop.add_to_cart(1)
        self.shop.account_payment("pekka", "12345")

        self.reference_generator_mock.new.assert_called()

        self.reference_generator_mock.new.reset_mock()

        self.shop.start_shopping()
        self.shop.add_to_cart(1)
        self.shop.account_payment("jere", "99999") 

        self.reference_generator_mock.new.assert_called()


    def test_remove_from_cart_returns_product_to_warehouse(self):            
        self.shop.start_shopping()
        self.shop.add_to_cart(1)
        self.shop.remove_from_cart(1)

        self.warehouse_mock.return_to_warehouse.assert_called()

    def test_add_to_cart_only_when_product_in_stock(self):
        def warehouse_balance(product_id):
            if product_id == 1:
                return 0

        self.warehouse_mock.balance.side_effect = warehouse_balance

        self.shop.start_shopping()
        self.shop.add_to_cart(1)
        self.shop.account_payment("jere", "99999") 

        self.bank_mock.bank_transfer.assert_called_with(
            "jere",
            42,
            "99999",
            ANY,
            0
        )

        self.warehouse_mock.take_from_warehouse.assert_not_called()
    
    def test_ledger_records_transactions(self):
        ledger.add_transaction("took from warehouse Product(id=1, name='milk', price=5)")
        self.assertIn("took from warehouse Product(id=1, name='milk', price=5)", ledger.transactions)
