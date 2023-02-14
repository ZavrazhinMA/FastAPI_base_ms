import re
import random
import pandas as pd
from time import strftime


class FakeNLPModel:

    def __init__(self):
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

    def logger_info(self, info_txt):
        self.current_process = info_txt
        if self.logger:
            self.logger.info(f'{self.datetime()}: {self.current_process}')

    @staticmethod
    def datetime():
        return strftime('[%Y-%b-%d %H:%M:%S]')

    def get_params(self):
        params_dict = {
            'result_filename': str(self.result_filename),
            'base_size': self.result_filename,
            'last_date': str(self.last_date),
            'history_months': '-' + '<br>-'.join(self.history_list),
            'model_class': self.wv_model_type,
            'status': str(self.status),
            'current_process': str(self.current_process),
        }
        return params_dict

    def get_history(self, filename: str):
        if re.match(r'.+xlsx$', filename):
            self.history_data = True
            self.last_date = f'{random.randint(1, 31)}-{random.randint(1, 13)}-{random.randint(2022, 2023)}'
            self.history_list = ['20-2022']
            self.history_base_size = random.randint(0, 100000)

    def build_model(self, model_type):
        if self.history_data:
            self.wv_model_type = model_type

    def get_sim_phrases(self, text=None, file=None, return_distance=False):
        if text:
            if return_distance:
                ['stroka ' + str(i) + ' :' + str(round(random.random(), 2)) for i in range(1, self.phrase_number + 1)]
            else:
                ['stroka ' + str(i) for i in range(1, self.phrase_number + 1)]
        elif file:
            result_file = pd.DataFrame({'message1': ['text1'], 'message2': ['text2']})
            self.result_filename = str(random.randint(1, 1000)) + '.xlsx'
            result_file.to_excel(self.result_filename)

        else:
            raise Exception('Введены неверные данные или загружен НЕ Excel файл')
