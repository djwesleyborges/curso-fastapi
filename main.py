from fastapi import FastAPI

# from shared.database import Base, engine
from contas_a_pagar_e_receber.routers import contas_a_pagar_e_receber_router
from shared.exceptions import NotFound
from shared.exceptions_handler import not_found_exception_handler

# from contas_a_pagar_e_receber.models import (
#     ContaPagarReceber,
# )
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contas_a_pagar_e_receber_router.router)
app.add_exception_handler(NotFound, not_found_exception_handler)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
