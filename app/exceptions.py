class WalletNotFound(Exception):
    """Wallet not found."""


class WalletNameTaken(Exception):
    """Waleet name already taken."""


class InsufficientFunds(Exception):
    """Not enough money for withdraw."""
