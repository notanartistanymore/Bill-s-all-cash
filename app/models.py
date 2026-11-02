from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

import uuid

from app.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    wallet_uuid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    wallet_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    wallet_balance: Mapped[int] = mapped_column(nullable=False)
