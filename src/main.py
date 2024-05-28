from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from src.router.api import router
from src.scraper import scrape_all_pages
from src.auth import get_current_user
import threading

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


tags_metadata = [
    {
        "name": "Autenticação",
        "description": "- Operações com usuários e sua autenticação.",
    },
    {
        "name": "Ajuda",
        "description": "- Rotas de apoio para utilizar a aplicação. Não são "
        "obrigatórias para o funcionamento da API.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "Produção",
        "description": "- Produção de vinhos, sucos e derivados do Rio Grande do Sul.",
        "externalDocs": {
            "description": "Site da Embrapa",
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02",
        },
    },
    {
        "name": "Processamento",
        "description": "- Quantidade de uvas processadas no Rio Grande do Sul.",
        "externalDocs": {
            "description": "Site da Embrapa",
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03",
        },
    },
    {
        "name": "Comercialização",
        "description": "- Comercialização de vinhos e derivados no Rio Grande do Sul.",
        "externalDocs": {
            "description": "Site da Embrapa",
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04",
        },
    },
    {
        "name": "Importação",
        "description": "- Importação de derivados de uva.",
        "externalDocs": {
            "description": "Site da Embrapa",
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05",
        },
    },
    {
        "name": "Exportação",
        "description": "- Exportação de derivados de uva.",
        "externalDocs": {
            "description": "Site da Embrapa",
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06",
        },
    },
]

app = FastAPI(
    debug=True,
    title="Tech Challenge - Dados da Vitivinicultura da Embrapa",
    description=(
        "Esta API fornece dados sobre a vitivinicultura coletados pela Embrapa.\n\n"
        "Através das rotas abaixo, pode-se acessar informações referentes à quantidade de uvas processadas, produção e comercialização de vinhos, suco e derivados provenientes do Estado do Rio Grande do Sul, além dos dados de importações e exportações dos produtos da vitivinicultura.\n\n"
        "Para mais informações, acesse o [README.md do projeto](https://github.com/matheus-chaves/api-consulta-dados-embrapa/blob/develop/README.md).\n\n"
        "### Outras dúvidas? Contate os membros do grupo 39:\n"
        "- [Bruno Pinheiro Mendes](mailto:brupmendes@icloud.com)\n"
        "- [Matheus Fonseca Chaves](mailto:matheusfonsecachaves@gmail.com)\n"
        "- [Michelle Da Luz Rodrigues](mailto:michellerodrigues268@gmail.com)\n"
    ),
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
    "Deve ser utilizado em caso de erros por **falta de arquivos e/ou indisponibilidade do site da Embrapa**.",
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
