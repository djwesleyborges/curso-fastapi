from fastapi.testclient import TestClient

from main import app

client = TestClient(app=app)


def test_deve_listar_contas_a_pagar_e_receber():
    response = client.get("/contas_a_pagar_e_receber")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "descricao": "Salário",
            "valor": "5000",
            "tipo": "Receita"
        },
        {
            "id": 2,
            "descricao": "Salário",
            "valor": "5000",
            "tipo": "Receita"
        }
    ]


def test_deve_criar_conta_a_pagar_e_receber():
    nova_conta = {
        "descricao": "Salário",
        "valor": "5000",
        "tipo": "Receita"
    }
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 3

    response = client.post("/contas_a_pagar_e_receber", json=nova_conta)
    assert response.status_code == 201
    assert response.json() == nova_conta_copy
