from decimal import Decimal
from enum import Enum

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from contas_a_pagar_e_receber.models import ContaPagarReceber
from shared.dependencies import get_db

router = APIRouter(prefix="/contas_a_pagar_e_receber")


class ContasPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: str

    class Config:
        orm_mode = True


class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = "PAGAR"
    RECEBER = "RECEBER"


class ContasPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=5, max_length=30)
    valor: float = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum


@router.get("/", response_model=list[ContasPagarReceberResponse])
def lista_contas(db: Session = Depends(get_db)) -> list[ContasPagarReceberResponse]:
    contas = db.query(ContaPagarReceber).all()
    return contas


@router.post("/", response_model=ContasPagarReceberResponse, status_code=201)
def criar_conta(conta: ContasPagarReceberRequest,
                db: Session = Depends(get_db)) -> ContasPagarReceberResponse:
    contas_a_pagar_e_receber = ContaPagarReceber(**conta.dict())

    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)

    return contas_a_pagar_e_receber
