from sqlalchemy import Integer, String, Column

from shared import Base


class FornecedorCliente(Base):
    __tablename__ = "fornecedor_cliente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255))
