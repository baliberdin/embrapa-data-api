import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from embrapadataapi.configuration.environment import JobConfig
from embrapadataapi.data.transform import *
from embrapadataapi.tasks.jobs import AbstractJob
import traceback

logger = get_logger(__name__)


class EmbrapaCrawlJob(AbstractJob):
    """Classe responsável pelo Crawling/Scraping dos dados do Site da Embrapa.
    Esta classe extende a classe Abstrata de Jobs
    """

    def __init__(self, config: JobConfig):
        super().__init__(config)

        # Configura diversos parâmetros do navegador para fazer o acesso ao site da Embrapa
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # Define o diretório de downloadas para o Selenium salvar os arquivos
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": self.config.params['downloaded_data_path']}
        options.add_experimental_option("prefs", prefs)
        logger.info(f"Pasta de downloads definida para: {self.config.params['downloaded_data_path']}")

        # Inicia o WebDriver do Chrome (Navegador)
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(driver_version="126.0.6478.182").install()), options=options)
        self.vars = {}

    def close(self):
        """Método usado para encerrar o Chrome
        """
        self.driver.quit()

    def _wait_for_window(self, timeout=2):
        """
        Método usado para aguardar a janela do Chrome durante as iterações
        """
        # Aguarda por um tempo, baseado no parâmetro timeout
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def do_crawl(self):
        """
        Método que executa o processo de crawling propriamente dito.
        O passo a passo é baseado em Selenium IDE
        """
        try:
            self.driver.get(self.config.params['url'])
            self.driver.set_window_size(1740, 1147)

            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(2)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win1"] = self._wait_for_window(2000)
            self.vars["root"] = self.driver.current_window_handle
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(3)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win6726"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.NAME, "opcao").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(3)").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_sopt:nth-child(3)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win6493"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(3)").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_sopt:nth-child(5)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win8797"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.NAME, "opcao").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(3)").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_sopt:nth-child(7)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win9331"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(4)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win1629"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.NAME, "opcao").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(5)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win1876"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(5)").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_sopt:nth-child(3)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win4480"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.NAME, "opcao").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(5)").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_sopt:nth-child(5)").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_sopt:nth-child(5)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win9692"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(5)").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_sopt:nth-child(7)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win2632"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.NAME, "opcao").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(5)").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_sopt:nth-child(9)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win5035"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(6)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win8446"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.NAME, "opcao").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(6)").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_sopt:nth-child(3)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win5295"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(6)").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_sopt:nth-child(5)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) .spn_small").click()
            self.vars["win7973"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
            self.driver.find_element(By.NAME, "opcao").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_opt:nth-child(6)").click()
            self.driver.find_element(By.CSS_SELECTOR, ".btn_sopt:nth-child(7)").click()
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.LINK_TEXT, "DOWNLOAD").click()
            self.vars["win8659"] = self._wait_for_window(2000)
            self.driver.switch_to.window(self.vars["root"])
        except Exception as e:
            traceback.print_exc()
            logger.warn(f"Erro ao executar o scraping do site da embrapa. {e}")
        finally:
            self.close()

    def run(self):
        # Executa a navegação no site da Embrapa e faz o Download dos arquivos
        self.do_crawl()

        # Executa os ETLs dos dados CSV que foram baixados do site da embrapa
        # Cada passo abaixo é referente a um tipo de dado/modelo
        execute_production_model_etl(self.config.params['downloaded_data_path'])
        execute_process_model_etl(self.config.params['downloaded_data_path'])
        execute_commercial_model_etl(self.config.params['downloaded_data_path'])
        execute_import_model_etl(self.config.params['downloaded_data_path'])
        execute_export_model_etl(self.config.params['downloaded_data_path'])
