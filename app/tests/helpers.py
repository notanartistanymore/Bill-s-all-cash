URL = "/api/v1/wallets"


def create_wallet(client, name="cash", balance=0):
    response = client.post(URL, json={"wallet_name": name, "initial_balance": balance})
    assert response.status_code == 201
    return response.json()


def operate(client, wallet_uuid, operation_type, amount):
    return client.post(
        f"{URL}/{wallet_uuid}/operation",
        json={"operation_type": operation_type, "amount": amount},
    )


def get_wallet(client, wallet_uuid):
    return client.get(f"{URL}/{wallet_uuid}")
