from kirjanpito import ledger as default_ledger


class Bank:
    def __init__(self, ledger=default_ledger):
        self._ledger = ledger

    def bank_transfer(self, name, reference_number, from_account, to_account, amount):
        self._ledger.add_transaction(
            f"bank transfer: from account {from_account} to account {to_account} reference {reference_number} amount {amount}e"
        )

        # here would be code that connects to the bank's web API
        return True


bank = Bank()
