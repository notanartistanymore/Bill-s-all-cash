from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from app.main import app
from app.tests.helpers import create_wallet, get_wallet, operate


def run_parallel(wallet_uuid, operation_type, amount, times):
    def send(_):
        return operate(TestClient(app), wallet_uuid, operation_type, amount)

    with ThreadPoolExecutor(max_workers=times) as pool:
        return list(pool.map(send, range(times)))


def test_concurrent_deposits_are_not_lost(real_client):
    wallet = create_wallet(real_client, balance=0)

    responses = run_parallel(wallet["wallet_uuid"], "DEPOSIT", 10, times=20)

    assert all(r.status_code == 200 for r in responses)
    balance = get_wallet(real_client, wallet["wallet_uuid"]).json()["wallet_balance"]
    assert balance == 200


def test_concurrent_withdrawals_never_go_negative(real_client):
    wallet = create_wallet(real_client, balance=100)

    responses = run_parallel(wallet["wallet_uuid"], "WITHDRAW", 30, times=10)

    statuses = sorted(r.status_code for r in responses)
    assert statuses == [200] * 3 + [409] * 7
    balance = get_wallet(real_client, wallet["wallet_uuid"]).json()["wallet_balance"]
    assert balance == 10
