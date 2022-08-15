"""
    Pegar os repositórios do github
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep, time

import env
import sql

log = True

options = webdriver.ChromeOptions()
options.add_argument("--disable-popup-blocking")
options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
wait_120 = WebDriverWait(driver, 120)
wait_60 = WebDriverWait(driver, 60)
wait_30 = WebDriverWait(driver, 30)
wait_20 = WebDriverWait(driver, 20)
wait_10 = WebDriverWait(driver, 10)
inicio = time()

if __name__ == '__main__':
    def main():
        driver.get(env.URL_LOGIN_GIT)
        wait_120.until(EC.visibility_of_element_located((By.ID, 'login_field')))
        
        driver.find_element_by_id('login_field').send_keys(env.USER_GIT)
        driver.find_element_by_id('password').send_keys(env.PASS_GIT)
        driver.find_element_by_css_selector('[type="submit"]').click()

        wait_30.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[href="https://github.com/"]')))
        
        page = 1

        loop = True
        while(loop):
            print('Olhando página ' + str(page))
            driver.get(env.URL_GIT(page))
            wait_30.until(EC.presence_of_element_located((By.ID, 'your-repos-filter')))

            try:
                driver.find_element_by_css_selector(env.EL_END)
                loop = False
            except:
                repos = driver.find_elements_by_css_selector(env.EL_REPOS)

                for index, repo in enumerate(repos):
                    nome_repo = repo.text
                    url_repo = repo.get_attribute('href')

                    dados = sql.get_repo_db(nome_repo)
                    if(len(dados) == 0):
                        sql.insert_repo_db(nome_repo, url_repo)
                    else:
                        print('Repositório já existe')

                page = page + 1
    main()
driver.close()
exit()
