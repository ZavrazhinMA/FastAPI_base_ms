import re
import random
import pandas as pd
from time import strftime, sleep
from asyncio import sleep as timesleep
import lorem
import os


class FakeNLPModel:

    def __init__(self):
        self.current_answer = ""
        self.history_data = None
        self.data_target = None
        self.last_date = None
        self.history_list = None
        self.history_base_size = 0
        self.logger = None
        self.status = 'FAIL'
        self.current_process = None
        self.phrase_number = 20
        self.result_filename = ''
        self.wv_model_type = 'fasttext'
        self.current_phrase = 'test query'

    def logger_info(self, info_txt):
        self.current_process = info_txt
        if self.logger:
            self.logger.info(f'{self.datetime()}: {self.current_process}')

    @staticmethod
    def datetime():
        return strftime('[%Y-%b-%d %H:%M:%S]')

    def init_base(self):
        self.build_model(self.wv_model_type)
        self.history_data = True

    def get_params(self):

        params_dict = {

            "current_answer": "\n\n".join(self.current_answer),
            'result_filename': str(self.result_filename),
            'base_size': int(self.history_base_size),
            'last_date': str(self.last_date),
            'history_months': '-' + '<br>-'.join(self.history_list) if self.history_list else '-',
            'model_class': self.wv_model_type,
            'status': str(self.status),
            'current_process': str(self.current_process),
            'current_phrase': str(self.current_phrase),
        }
        return params_dict

    def get_history(self, filename):
        if re.match(r'.+xlsx$', filename.filename):
            timesleep(5)
            self.history_data = True
            self.last_date = f'{random.randint(1, 31)}-{random.randint(1, 13)}-{random.randint(2022, 2023)}'
            self.history_list = ['20-2022']
            self.history_base_size = random.randint(0, 100000)

    def build_model(self, model_type):
        if self.history_data:
            sleep(5)
            self.wv_model_type = model_type
            self.status = "OK"

    def get_sim_phrases_df(self, text=None, file=None, return_distance=False):
        if text:
            if return_distance:
                self.current_answer = [lorem.sentence() + ' :' +
                                       str(round(random.random(), 2)) for _ in range(1, self.phrase_number + 1)]
            else:
                self.current_answer = [lorem.sentence() for _ in range(1, self.phrase_number + 1)]

        elif file:
            result_file = pd.DataFrame({'message1': ['text1'], 'message2': ['text2']})
            self.result_filename = str(random.randint(1, 1000)) + '.xlsx'
            result_file.to_excel(os.path.join(".", "data", self.result_filename))
            timesleep(3)

        else:
            raise Exception('Введены неверные данные или загружен НЕ Excel файл')

