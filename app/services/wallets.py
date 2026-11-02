from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import uuid

import app.models as models
import app.exceptions as exceptions


def create_wallet(db: Session, wallet_name: str, initial_balance: int) -> models.Wallet:
    wallet = models.Wallet(wallet_name=wallet_name, wallet_balance=initial_balance)
    db.add(wallet)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise exceptions.WalletNameTaken
    db.refresh(wallet)
    return wallet


def get_wallet(db: Session, wallet_uuid: uuid.UUID) -> models.Wallet:
    wallet = db.get(models.Wallet, wallet_uuid)
    if wallet is None:
        raise exceptions.WalletNotFound
    return wallet
