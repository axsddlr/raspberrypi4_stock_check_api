import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from api.scrape import RPIST

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Unofficial Lost Ark API",
    description="An Unofficial REST API for [Lost Ark](https://www.playlostark.com/en-us/news), Made by [Andre "
                "Saddler]( "
                "https://github.com/axsddlr)",
    version="1.0.3",
    docs_url="/",
    redoc_url=None,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# init limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# init classes
rpis = RPIST()


@app.get("/digikey/", tags=["News"])
@limiter.limit("250/minute")
def digikey_store(request: Request):
    return rpis.digikey()


@app.get("/pishop/", tags=["News"])
@limiter.limit("250/minute")
def pishop_store(request: Request):
    return rpis.pishop()


@app.get("/chicagodist/", tags=["News"])
@limiter.limit("250/minute")
def chicagodist_store(request: Request):
    return rpis.chicagodist()


@app.get("/okdo/", tags=["News"])
@limiter.limit("250/minute")
def okdo_store(request: Request):
    return rpis.okdo()


@app.get("/vilros/", tags=["News"])
@limiter.limit("250/minute")
def vilros_store(request: Request):
    return rpis.vilros()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
