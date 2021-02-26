import configparser
import os


class ConfigParser:

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read(os.path.join(os.path.dirname(__file__), 'conf/config.ini'))

    def get_company_logo(self, company):
        return self._config['company_logo'].get(company)

    def get_company_icon(self, company):
        return self._config['company_icon'].get(company)
