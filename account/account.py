class Account:
    def __init__(self, file_path):
        self.file_path = file_path

        with open(file_path) as f:
            self.balance = int(f.read())
            f.close()

    def _commit(self):
        with open(self.file_path, "w") as f:
            f.write(str(self.balance))
            f.close()

    def commit(func):
        def inner(self, *args):
            r = func(self, *args)
            self._commit()
            return r

        return inner

    @commit
    def withdraw(self, amount):
        self.balance -= amount

    @commit
    def deposit(self, amount):
        self.balance += amount


class Checking(Account):
    def __init__(self, file_path, fee):
        Account.__init__(self, file_path)
        self.fee = fee

    def transfer(self, amount):
        self.withdraw(amount + self.fee)
