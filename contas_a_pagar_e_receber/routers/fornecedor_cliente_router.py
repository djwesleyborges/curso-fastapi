from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from contas_a_pagar_e_receber.models import FornecedorCliente
from shared.dependencies import get_db
from shared.exceptions import NotFound

router = APIRouter(prefix="/fornecedor-cliente")


class FornecedorClienteResponse(BaseModel):
    id: int
    nome: str

    class Config:
        #orm_mode = True
        from_attributes = True

class FornecedorClienteRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=30)


@router.get("", response_model=List[FornecedorClienteResponse])
def listar_fornecedor_cliente(db: Session = Depends(get_db)) -> List[
    FornecedorClienteResponse]:
    return db.query(FornecedorCliente).all()


@router.get("/{id_fornecedor}", response_model=FornecedorClienteResponse)
def obter_fornecedor(id_fornecedor: int, db: Session = Depends(get_db)) -> \
        List[FornecedorClienteResponse]:
    return buscar_fornecedor_por_id(id_fornecedor, db)


@router.post("", response_model=FornecedorClienteResponse, status_code=201)
def criar_fornecedor(fornecedor: FornecedorClienteRequest,
                     db: Session = Depends(
                         get_db)) -> FornecedorClienteResponse:
    novo_fornecedor = FornecedorCliente(**fornecedor.dict())
    db.add(novo_fornecedor)
    db.commit()
    db.refresh(novo_fornecedor)
    return novo_fornecedor


@router.put("/{id_fornecedor}", response_model=FornecedorClienteResponse,
            status_code=200)
def atualizar_fornecedor(id_fornecedor: int,
                         fornecedor: FornecedorClienteRequest,
                         db: Session = Depends(
                             get_db)) -> FornecedorClienteResponse:
    fornecedor_a_ser_alterado = buscar_fornecedor_por_id(id_fornecedor, db)
    fornecedor_a_ser_alterado.nome = fornecedor.nome
    db.add(fornecedor_a_ser_alterado)
    db.commit()
    db.refresh(fornecedor_a_ser_alterado)
    return fornecedor_a_ser_alterado


@router.delete("/{id_fornecedor}", status_code=204)
def deletar_fornecedor(id_fornecedor: int, db: Session = Depends(get_db)):
    fornecedor_a_ser_deletado = buscar_fornecedor_por_id(id_fornecedor, db)
    db.delete(fornecedor_a_ser_deletado)
    db.commit()


def buscar_fornecedor_por_id(id_fornecedor: int,
                             db: Session) -> FornecedorCliente:
    fornecedor = db.query(FornecedorCliente).get(id_fornecedor)
    if fornecedor is None:
        raise NotFound("Fornecedor")
    return fornecedor
