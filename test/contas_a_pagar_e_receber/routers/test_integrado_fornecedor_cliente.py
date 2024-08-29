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

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)


# Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_deve_listar_fornecedores():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/fornecedor-cliente", json={"nome": "Fornecedor 1"})
    client.post("/fornecedor-cliente", json={"nome": "Fornecedor 2"})

    response = client.get("/fornecedor-cliente")
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, "nome": "Fornecedor 1"},
        {'id': 2, "nome": "Fornecedor 2"}
    ]


def test_deve_listar_por_id_fornecedore():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/fornecedor-cliente",
                           json={"nome": "Fornecedor 1"})
    id_fornecedor = response.json()["id"]

    response_get = client.get(f"/fornecedor-cliente/{id_fornecedor}")
    assert response_get.status_code == 200
    assert response_get.json() == {
        "id": id_fornecedor,
        "nome": "Fornecedor 1"
    }


def test_deve_retornar_nao_encontrado_para_id_nao_existente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response_get = client.get(f"/fornecedor-cliente/100")
    assert response_get.status_code == 404
    assert response_get.json() == {"message": "Fornecedor não encontrado"}


def test_deve_criar_fornecedor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/fornecedor-cliente",
                           json={"nome": "Fornecedor 1"})
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "nome": "Fornecedor 1"
    }


def test_deve_alterar_fornecedor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/fornecedor-cliente",
                           json={"nome": "Fornecedor 1"})
    id_fornecedor = response.json()["id"]

    response = client.put(f"/fornecedor-cliente/{id_fornecedor}",
                          json={"nome": "Fornecedor 2"})
    assert response.status_code == 200
    assert response.json() == {
        "id": id_fornecedor,
        "nome": "Fornecedor 2"
    }


def test_deve_retornar_erro_nao_encontrado_para_id_nao_existente_na_atualizacao():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.put(f"/fornecedor-cliente/100",
                          json={"nome": "Fornecedor 2"})
    assert response.status_code == 404


def test_deve_remover_fornecedor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/fornecedor-cliente",
                           json={"nome": "Fornecedor 1"})
    id_fornecedor = response.json()["id"]

    response = client.delete(f"/fornecedor-cliente/{id_fornecedor}")
    assert response.status_code == 204
    response_get_all = client.get("/fornecedor-cliente")
    assert len(response_get_all.json()) == 0


def test_deve_retornar_erro_nao_encontrado_para_id_nao_existente_na_remocao():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.delete(f"/fornecedor-cliente/100")
    assert response.status_code == 404
    assert response.json() == {"message": "Fornecedor não encontrado"}


def test_deve_retornar_erro_quando_nome_nao_estiver_dentro_dos_limites():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post("/fornecedor-cliente", json={"nome": ""})
    assert response.status_code == 422