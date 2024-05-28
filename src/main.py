import threading
from contextlib import asynccontextmanager

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException

from src.auth import get_current_user
from src.config.docs import api_description
from src.config.docs import tags_metadata
from src.router.api import router
from src.scraper import scrape_all_pages

lock = threading.Lock()


def scrape_all_pages_with_lock():
    global lock
    if lock.acquire(blocking=False):
        try:
            scrape_all_pages()
        finally:
            lock.release()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes the project by creating API data via web scraping.\n
    A thread was used to not delay the API initialization.
    """
    threading.Thread(target=scrape_all_pages_with_lock).start()
    yield


app = FastAPI(
    debug=True,
    title="Tech Challenge - Dados da Vitivinicultura da Embrapa",
    description=api_description,
    version="1.0.0",
    license_info={
        "name": "Licença MIT",
        "identifier": "MIT",
    },
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)


@app.get(
    "/scrape-data",
    tags=["Ajuda"],
    summary="Busca os dados da API via web scraping",
    description="Busca e salva os dados sem bloquear outros endpoints da API.\n\n"
    "Deve ser utilizado em caso de erros por **falta de arquivos e/ou"
    " indisponibilidade do site da Embrapa**.",
    responses={"503": {"description": "Scraping is already in progress."}},
    dependencies=[Depends(get_current_user)],
)
async def scrape_data():
    """
    Create the API data via web scraping and save it at 'data' folder.\n
    With threads, automatically blocks multiple calls to this endpoint,
    throwing an HTTP error.
    """

    if lock.locked():
        raise HTTPException(status_code=503, detail="Scraping is already in progress.")
    else:
        threading.Thread(target=scrape_all_pages_with_lock).start()
        return {"message": "Scraping has been started."}


app.include_router(router)
