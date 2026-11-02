from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import uuid

from app.schemas import WalletResponse, WalletCreateRequest
import app.services.wallets as services_wallets

from app.database import get_db

router = APIRouter()


@router.get("/api/v1/wallets/{wallet_uuid}", response_model=WalletResponse)
def get_balance(wallet_uuid: uuid.UUID, db: Session = Depends(get_db)):
    try:
        return services_wallets.get_wallet(db=db, wallet_uuid=wallet_uuid)
    except services_wallets.WalletNotFound:
        raise HTTPException(status_code=404, detail="Wallet not found!")


@router.post("/api/v1/wallets", response_model=WalletResponse, status_code=201)
def create_wallet(payload: WalletCreateRequest, db: Session = Depends(get_db)):
    try:
        return services_wallets.create_wallet(
            db=db,
            wallet_name=payload.wallet_name,
            initial_balance=payload.initial_balance,
        )
    except services_wallets.WalletNameTaken:
        raise HTTPException(status_code=409, detail="Wallet name already exists!")
