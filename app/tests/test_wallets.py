import uuid

from app.tests.helpers import create_wallet, get_wallet, operate


def test_get_wallet(client):
    wallet = create_wallet(client, balance=70)
    response = get_wallet(client, wallet["wallet_uuid"])

    assert response.status_code == 200
    assert response.json() == wallet


def test_get_wallet_not_found(client):
    response = get_wallet(client, uuid.uuid4())

    assert response.status_code == 404


def test_deposit(client):
    wallet = create_wallet(client, balance=100)
    response = operate(client, wallet["wallet_uuid"], "DEPOSIT", 50)
    assert response.status_code == 200
    assert response.json()["wallet_balance"] == 150


def test_deposit_negative(client):
    wallet = create_wallet(client, balance=100)
    response = operate(client, wallet["wallet_uuid"], "DEPOSIT", -50)
    assert response.status_code == 422
    assert get_wallet(client, wallet["wallet_uuid"]).json()["wallet_balance"] == 100


def test_withdraw(client):
    wallet = create_wallet(client, balance=100)
    response = operate(client, wallet["wallet_uuid"], "WITHDRAW", 50)
    assert response.status_code == 200
    assert response.json()["wallet_balance"] == 50


def test_withdraw_insufficient_funds(client):
    wallet = create_wallet(client, balance=100)
    response = operate(client, wallet["wallet_uuid"], "WITHDRAW", 200)
    assert response.status_code == 409
    assert get_wallet(client, wallet["wallet_uuid"]).json()["wallet_balance"] == 100
