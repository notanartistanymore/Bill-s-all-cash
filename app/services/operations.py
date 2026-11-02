from sqlalchemy import select
from sqlalchemy.orm import Session
import app.models as models
import uuid
import app.exceptions as exceptions
from app.schemas import OperationType


def add_operation(
    db: Session, wallet_uuid: uuid.UUID, operation_type: OperationType, amount: int
):
    wallet = db.scalar(
        select(models.Wallet)
        .where(models.Wallet.wallet_uuid == wallet_uuid)
        .with_for_update()
    )
    if wallet is None:
        raise exceptions.WalletNotFound
    if operation_type is OperationType.DEPOSIT:
        wallet.wallet_balance += amount
    else:
        if amount > wallet.wallet_balance:
            db.rollback()
            raise exceptions.InsufficientFunds
        wallet.wallet_balance -= amount

    db.commit()
    db.refresh(wallet)
    return wallet
