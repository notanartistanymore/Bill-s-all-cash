from sqlalchemy import BigInteger, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

import uuid

from app.database import Base


class Wallet(Base):
    __tablename__ = "wallets"
    __table_args__ = (
        CheckConstraint("wallet_balance >= 0", name="ck_wallets_balance_non_negative"),
    )

    wallet_uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    wallet_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    wallet_balance: Mapped[int] = mapped_column(BigInteger, nullable=False)
