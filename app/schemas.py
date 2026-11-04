from pydantic import BaseModel, Field
from enum import Enum
import uuid


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletCreateRequest(BaseModel):
    wallet_name: str = Field(min_length=1, max_length=100)
    initial_balance: int = Field(
        default=0, ge=0, description="Initial balance in cents"
    )


class WalletResponse(BaseModel):
    wallet_uuid: uuid.UUID
    wallet_name: str
    wallet_balance: int = Field(description="Balance in cents")


class WalletOperationRequest(BaseModel):
    operation_type: OperationType
    amount: int = Field(gt=0, description="Amount in cents")
