import uvicorn
import asyncio
import typer
from fastapi import FastAPI

from .db import init_models
from .routers import attributes


app = FastAPI(version="0.0.1")
cli = typer.Typer()


app.include_router(attributes.router)


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


if __name__ == '__main__':
    cli()