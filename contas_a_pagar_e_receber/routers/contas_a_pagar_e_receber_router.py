from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from contas_a_pagar_e_receber.models import ContaPagarReceber
from shared.dependencies import get_db

router = APIRouter(prefix="/contas_a_pagar_e_receber")


class ContasPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str

    class Config:
        orm_mode = True


class ContasPagarReceberRequest(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str


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
