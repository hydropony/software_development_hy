from kauppa import Shop
from kirjanpito import ledger
from varasto import warehouse
from pankki import bank
from viitegeneraattori import reference_generator

def main():
    # use pre-created "default" warehouse, bank and reference generator objects
    shop = Shop(warehouse, bank, reference_generator)

    # shop handles one customer at a time in the following way:
    shop.start_shopping()
    shop.add_to_cart(1)
    shop.add_to_cart(3)
    shop.add_to_cart(3)
    shop.remove_from_cart(1)
    shop.account_payment("Pekka Mikkola", "1234-12345")

    # next customer
    shop.start_shopping()

    for _ in range(0, 24):
        shop.add_to_cart(5)

    shop.account_payment("Arto Vihavainen", "3425-1652")

    # ledger
    for transaction in ledger.transactions:
        print(transaction)


if __name__ == "__main__":
    main()

#12
