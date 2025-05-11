from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from .api import app as api_app


app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/api")
def redirect_api():
    return RedirectResponse(url="/api/")


app.mount("/api/", api_app)


@app.get("/docs")
def redirect_docs():
    return RedirectResponse(url="/docs/")


app.mount("/docs/", StaticFiles(directory="money_regrets/docs/", html=True, ), name="mkdocs")


app.mount("/", StaticFiles(directory="money_regrets/static", html=True), name="static")
