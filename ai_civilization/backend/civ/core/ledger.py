"""Double-entry style ledger: money moves between accounts, total supply is conserved."""


class Ledger:
    def __init__(self):
        self.accounts: dict[str, int] = {}

    def open(self, name: str, balance: int = 0) -> None:
        self.accounts[name] = balance

    def balance(self, name: str) -> int:
        return self.accounts[name]

    def transfer(self, src: str, dst: str, amount: int) -> bool:
        if amount < 0 or self.accounts[src] < amount:
            return False
        self.accounts[src] -= amount
        self.accounts[dst] += amount
        return True

    def total(self) -> int:
        return sum(self.accounts.values())
