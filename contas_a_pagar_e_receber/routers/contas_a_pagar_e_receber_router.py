from decimal import Decimal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/contas_a_pagar_e_receber")


class ContasPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str


class ContasPagarReceberRequest(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str


@router.get("/", response_model=list[ContasPagarReceberResponse])
def lista_contas():
    return [
        ContasPagarReceberResponse(
            id=1,
            descricao="Salário",
            valor=Decimal(5000.00),
            tipo="Receita",
        ),
        ContasPagarReceberResponse(
            id=2,
            descricao="Salário",
            valor=Decimal(5000.00),
            tipo="Receita",
        ),
    ]


@router.post("/", response_model=ContasPagarReceberResponse, status_code=201)
def criar_conta(conta: ContasPagarReceberRequest):
    return ContasPagarReceberResponse(
        id=3,
        descricao=conta.descricao,
        valor=conta.valor,
        tipo=conta.tipo,
    )
