from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
from pydantic import BaseModel
from model import FakeNLPModel
import os

app = FastAPI()

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "front/")
app.mount("/front", StaticFiles(directory="front"), name="static")
templates = Jinja2Templates(directory="front")

nlp_model = FakeNLPModel()


def datetime():
    return strftime('[%Y-%b-%d %H:%M:%S]')


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "test": 1})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
