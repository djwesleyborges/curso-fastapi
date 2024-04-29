from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from main import app
from shared import Base
from shared.dependencies import get_db

client = TestClient(app=app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_deve_listar_contas_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/contas_a_pagar_e_receber",
                json={"descricao": "Aluguel", "valor": 1000.5, "tipo": "PAGAR"})
    client.post("/contas_a_pagar_e_receber",
                json={"descricao": "Salário", "valor": 5000, "tipo": "RECEBER"})

    response = client.get("/contas_a_pagar_e_receber")
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, "descricao": "Aluguel", "valor": 1000.5, "tipo": "PAGAR"},
        {'id': 2, "descricao": "Salário", "valor": 5000, "tipo": "RECEBER"}
    ]


def test_deve_criar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        "descricao": "Salário",
        "valor": 333,
        "tipo": "RECEBER"
    }
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 1

    response = client.post("/contas_a_pagar_e_receber", json=nova_conta)
    assert response.status_code == 201
    assert response.json() == nova_conta_copy


def test_deve_retornar_erro_quando_exceder_a_descricao():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        "descricao": "SalárioSalárioSalárioSalárioSalárioSalárioSalário",
        "valor": 333,
        "tipo": "RECEBER"
    }

    response = client.post("/contas_a_pagar_e_receber", json=nova_conta)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "descricao"]


def test_deve_retornar_erro_quando_a_descricao_for_menor_do_que_o_necessario():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        "descricao": "Ola",
        "valor": 333,
        "tipo": "RECEBER"
    }

    response = client.post("/contas_a_pagar_e_receber", json=nova_conta)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "descricao"]


def test_deve_retornar_erro_quando_o_tipo_for_invalido():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        "descricao": "Salário",
        "valor": 333,
        "tipo": "INVALIDO"
    }

    response = client.post("/contas_a_pagar_e_receber", json=nova_conta)
    assert response.status_code == 422


def test_deve_retornar_erro_quando_valor_for_zero_ou_menor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        "descricao": "Salário",
        "valor": 0,
        "tipo": "RECEBER"
    }

    response = client.post("/contas_a_pagar_e_receber", json=nova_conta)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "valor"]
