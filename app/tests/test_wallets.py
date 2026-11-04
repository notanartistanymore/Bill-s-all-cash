import uuid
import pytest

from app.tests.helpers import create_wallet, get_wallet, operate


def test_create_wallet(client):
    response = client.post(
        f"/api/v1/wallets/", json={"wallet_name": "cash", "initial_balance": 50}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["wallet_name"] == "cash"
    assert body["wallet_balance"] == 50
    assert uuid.UUID(body["wallet_uuid"])


def test_create_wallet_with_default_balance(client):
    response = client.post(f"/api/v1/wallets/", json={"wallet_name": "cash"})
    assert response.status_code == 201
    body = response.json()
    assert body["wallet_balance"] == 0


def test_create_wallet_with_taken_name(client):
    create_wallet(client, "cash", 50)
    response = client.post(f"/api/v1/wallets/", json={"wallet_name": "cash"})
    assert response.status_code == 409


def test_create_wallet_with_negative_balance(client):
    response = client.post(
        f"/api/v1/wallets/", json={"wallet_name": "cash", "initial_balance": -50}
    )
    assert response.status_code == 422


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


@pytest.mark.parametrize("balance", [2_147_483_648, 5_000_000_000])
def test_bigint_balance_round_trip(client, balance):
    wallet = create_wallet(client, balance=balance)

    assert wallet["wallet_balance"] == balance
    assert get_wallet(client, wallet["wallet_uuid"]).json()["wallet_balance"] == balance


def test_deposit_crosses_integer_limit(client):
    wallet = create_wallet(client, balance=2_147_483_647)

    response = operate(client, wallet["wallet_uuid"], "DEPOSIT", 1)
    assert response.status_code == 200
    assert response.json()["wallet_balance"] == 2_147_483_648

    response = operate(client, wallet["wallet_uuid"], "WITHDRAW", 75)
    assert response.status_code == 200
    assert response.json()["wallet_balance"] == 2_147_483_573
