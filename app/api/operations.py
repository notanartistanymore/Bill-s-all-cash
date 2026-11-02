from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session

import uuid

from app.schemas import WalletResponse, WalletOperationRequest
import app.services.operations as services_operations
from app.database import get_db
import app.exceptions as exceptions

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
    except exceptions.WalletNotFound:
        raise HTTPException(status_code=404, detail="WalletNotFound!")
    except exceptions.InsufficientFunds:
        raise HTTPException(status_code=409, detail="InsufficientFunds")
