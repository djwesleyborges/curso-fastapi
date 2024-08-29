from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from contas_a_pagar_e_receber.models import ContaPagarReceber
from shared.dependencies import get_db
from shared.exceptions import NotFound

router = APIRouter(prefix="/contas_a_pagar_e_receber")


class ContasPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: str

    class Config:
        # orm_mode = True
        from_attributes = True


class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = "PAGAR"
    RECEBER = "RECEBER"


class ContasPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=5, max_length=30)
    valor: float = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum
    fornecedor_id: int | None = None


@router.get("/", response_model=list[ContasPagarReceberResponse])
def lista_contas(db: Session = Depends(get_db)) -> list[ContasPagarReceberResponse]:
    contas = db.query(ContaPagarReceber).all()
    return contas


@router.get("/{id_conta_a_pagar_e_receber}", response_model=ContasPagarReceberResponse)
def obter_conta_por_id(id_conta_a_pagar_e_receber: int,
                       db: Session = Depends(get_db)) -> ContasPagarReceberResponse:
    return busca_conta_por_id(id_conta_a_pagar_e_receber, db)


@router.post("/", response_model=ContasPagarReceberResponse, status_code=201)
def criar_conta(conta: ContasPagarReceberRequest,
                db: Session = Depends(get_db)) -> ContasPagarReceberResponse:
    contas_a_pagar_e_receber = ContaPagarReceber(**conta.dict())

    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)

    return contas_a_pagar_e_receber


@router.put("/{id_conta_a_pagar_e_receber}", response_model=ContasPagarReceberResponse,
            status_code=200)
def atualizar_conta(id_conta_a_pagar_e_receber: int, conta: ContasPagarReceberRequest,
                    db: Session = Depends(get_db)) -> ContasPagarReceberResponse:
    contas_a_pagar_e_receber = busca_conta_por_id(id_conta_a_pagar_e_receber, db)
    contas_a_pagar_e_receber.descricao = conta.descricao
    contas_a_pagar_e_receber.valor = conta.valor
    contas_a_pagar_e_receber.tipo = conta.tipo
    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)
    return contas_a_pagar_e_receber


@router.delete("/{id_conta_a_pagar_e_receber}", status_code=204)
def remover_conta(id_conta_a_pagar_e_receber: int,
                  db: Session = Depends(get_db)) -> None:
    conta = busca_conta_por_id(id_conta_a_pagar_e_receber, db)
    db.delete(conta)
    db.commit()
    return None


def busca_conta_por_id(id_conta_a_pagar_e_receber: int,
                       db: Session) -> ContaPagarReceber:
    conta_a_pagar_e_receber = db.query(ContaPagarReceber).get(
        id_conta_a_pagar_e_receber)
    if conta_a_pagar_e_receber is None:
        raise NotFound("Conta a Pagar e Receber")
    return conta_a_pagar_e_receber
