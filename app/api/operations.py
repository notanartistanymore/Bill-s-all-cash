from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session

import uuid

from app.schemas import WalletResponse, WalletOperationRequest
import app.services.wallets as services_wallets
import app.services.operations as services_operations
from app.database import get_db

router = APIRouter()


@router.post("/api/v1/wallets/{wallet_uuid}/operation", response_model=WalletResponse)
def add_operation(
    wallet_uuid: uuid.UUID,
    payload: WalletOperationRequest,
    db: Session = Depends(get_db),
):
    try:
        return services_operations.add_operation(
            db,
            wallet_uuid=wallet_uuid,
            operation_type=payload.operation_type,
            amount=payload.amount,
        )
    except services_wallets.WalletNotFound:
        raise HTTPException(status_code=404, detail="Wallet not found!")
    except services_operations.InsufficientFunds:
        raise HTTPException(status_code=400, detail="InsufficientFunds")
