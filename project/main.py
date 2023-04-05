from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
import os
from logging.handlers import RotatingFileHandler
from time import strftime
from pydantic import BaseModel

from model import FakeNLPModel
import os

handler = RotatingFileHandler(filename='app.log', maxBytes=10000, backupCount=0, encoding="UTF-8")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

app = FastAPI()
app.mount("/front", StaticFiles(directory="front"), name="static")
templates = Jinja2Templates(directory="front")
nlp_model = FakeNLPModel()
nlp_model.logger = logger


@app.on_event("startup")
def build_models():
    try:
        logger.info(f"{datetime()}: ----------------NEW START----------------")
        nlp_model.init_base()
        logger.info(f"{datetime()}: Модель поиска похожих фраз инициализирована")
    except Exception as init_er:
        logger.error(f"{datetime()}: Ошибка при инициализации модели поиска похожих фраз -> {init_er}")


def datetime():
    return strftime('[%Y-%b-%d %H:%M:%S]')


class GetItem(BaseModel):
    result_filename: str
    base_size: int
    last_date: str
    history_months: str
    model_class: str
    status: str
    current_process: str
    current_phrase: str
    current_answer: str


@app.get("/", response_class=HTMLResponse)
async def main_get(request: Request):
    params = GetItem(**nlp_model.get_params())
    return templates.TemplateResponse("index.html", {"request": request, "params": params.dict()})


@app.post("/history_files")
async def read_history_files(request: Request, h_file: UploadFile | None = File(...), model_type: str = Form()):
    if h_file.filename != "":
        try:
            nlp_model.get_history(h_file)
        except Exception as update_er:
            logger.error(f"{datetime()}: Ошибка обновления файла истории сообщений - {update_er}")
        if (nlp_model.status == "FAIL" or nlp_model.wv_model_type != model_type) \
                and nlp_model.history_data is not None:
            try:
                nlp_model.wv_model_type = model_type
                nlp_model.build_model(model_type)
            except Exception as model_er:
                logger.error(f"{datetime()}: Ошибка при создании WV или KNN моделей -> {model_er}")
    params = GetItem(**nlp_model.get_params())
    return templates.TemplateResponse("index.html", {"request": request, "params": params.dict()})


@app.post("/excel_predict")
async def get_excel_predict(request: Request, target_file: UploadFile | None = File(...)):
    if target_file.filename != "" and nlp_model.status == "OK":
        try:
            nlp_model.get_sim_phrases_df(file=target_file)
        except Exception as update_er:
            logger.error(f"{datetime()}: Ошибка при подготовке итогового датасета похохжих фраз -> {update_er}")
    params = GetItem(**nlp_model.get_params())
    return templates.TemplateResponse("index.html", {"request": request, "params": params.dict()
                                                     })


@app.get("/excel_file")
async def get_excel_file(request: Request):
    if nlp_model.result_filename != "":
        result_df_path = os.path.join('.', 'data', nlp_model.result_filename)
        if os.path.exists(result_df_path):
            return FileResponse(result_df_path, filename=nlp_model.result_filename,
                                media_type="application/vnd.ms-excel")
    else:
        nlp_model.current_process = "Остутсвует файл для скачивания"
        params = GetItem(**nlp_model.get_params())
        return templates.TemplateResponse("index.html", {"request": request, "params": params.dict()})


@app.post("/sim_phrases")
async def get_phrase_predict(request: Request,
                             phrase: str = Form(), return_dist: bool = Form(False), num_phrases: int = Form()):
    if num_phrases:
        nlp_model.phrase_number = num_phrases
    if phrase and nlp_model.status == "OK":
        try:
            nlp_model.get_sim_phrases_df(text=phrase, return_distance=return_dist)
        except Exception as update_er:
            logger.error(f"{datetime()}: Сбой поиска похожих фраз -> {update_er}")
    params = GetItem(**nlp_model.get_params())
    return templates.TemplateResponse("index.html", {"request": request, "params": params.dict()})


@app.get("/logs")
async def get_logs():
    return FileResponse(os.path.join(".", "app.log"), media_type="text")

#
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="127.0.0.1", port=8080)
