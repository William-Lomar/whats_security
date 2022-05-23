from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert 
from selenium.webdriver.support.ui import Select
import time
import requests
import sys
from threading import Timer,Thread,Event
import os

#Função de intervalo
class SetInterval():
   def __init__(self,time,function):
      self.time=time
      self.function = function
      self.thread = Timer(self.time,self.handle_function)

   def handle_function(self):
      self.function()
      self.thread = Timer(self.time,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

# configurar usuário
setor = "setor"

#Função de validação de usuário
def usuario():
    if setor == "setor":
        return "endereço da imagem do wats"
    elif setor == "x":
        return "img do x"
    elif setor == "y":
        return "img da y"

#Verificar se tem internet 
def check_internet():
    ''' checar conexão de internet '''
    url = 'https://www.google.com'
    timeout = 5
    try:
        requests.get(url, timeout=timeout)
        return True
    except Exception as e:
        print(e)
        return False  
    
if check_internet():
    print('Internet OK!')
else:
    print('Sem conexão à internet!')
    sys.exit()

#Pre-configuração de profile
options = Options()
options.add_argument("user-data-dir=Endereço do arquivo de config desejado")

#Instancia o driver como Chrome
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),chrome_options=options)

#Config wait
wait = WebDriverWait(driver,30000)
wait_erro = WebDriverWait(driver,2)

#Vai até o whats web
driver.get("https://web.whatsapp.com/")

invalido = 0

#Verificação de abas abertas 
def verifica_abas():
    global invalido
    try:
        verifica_browser = driver.get_window_size()
        
        #Colocar segunda validação de imagem 
        try:
            verifica_imagem = wait_erro.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#side > header > div.YtmXM > div > img')))
            tag_imagem = verifica_imagem.get_attribute("src")
            
            if invalido == 3:
                print("Usuario não autorizado persistiu logado!")
                driver.execute_script("alert('Usuário não autorizado permaneceu logado, fechando app!')")
                time.sleep(2)
                #Confirmar pop-up 
                try:
                    wait_erro.until(EC.alert_is_present())
                    Alert(driver).accept()
                except:
                    print("")
                driver.quit()
                sys.exit()
            
            if tag_imagem == usuario():
                print("Usuário ok")
            else:
                print("Usuário não autorizado")
                invalido += 1
        except Exception as e:
            print("Usuário não logado")
        
        quantidade = len(driver.window_handles) 
        if quantidade != 1:
            print("Abas não autorizada aberta")
            driver.quit()
            sys.exit()
        else:
            print('ok')
        
    except:
        print("Navegador fechado")
        sys.exit()

verificar = SetInterval(10,verifica_abas)
verificar.start()

#main
def main():
    imagem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#side > header > div.YtmXM > div > img')))
    tag_imagem = imagem.get_attribute("src")

    if tag_imagem == usuario():
        print("Validação ok")
        #Aguardar QRcode e iniciar novamente looping
        qr_code = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#app > div > div > div.landing-window > div.landing-main > div > div._25pwu > div > canvas')))
        main()
    else:
        print("Celular não permitido logado!!")
        driver.execute_script("alert('Usuário sem autorização para utilizar este número!')")  
        time.sleep(2)
        
        #Confirmar pop-up 
        try:
            wait_erro.until(EC.alert_is_present())
            Alert(driver).accept()
        except:
            print("")
        
        sucess = True
        
        while sucess:
            #Botão mais opções 
            ampliar = wait_erro.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#side > header > div._3yZPA > div > span > div:nth-child(3) > div > span')))
            ampliar.click()
            
            #Botão Sair
            #por algum motivo está clicando em configurações as vezes, parece q está aparecendo 5 opções em vez de 4 as vezes
            sair = wait_erro.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#side > header > div._3yZPA > div > span > div._2cNrC._1CTfw > span > div > ul > li:nth-child(4) > div._2oldI.dJxPU")))
            sair.click()
            
            #se config aparecer
            try:
                #Botão desconectar
                desconectar = wait_erro.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#app > div > span:nth-child(2) > div > div > div > div > div > div > div._2i3w0 > div > div._20C5O._2Zdgs > div > div')))
                desconectar.click()
                
                sucess = False
            except:
                voltar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#app > div > div > div._3ArsE > div.ldL67._2i3T7 > span > div > span > div > header > div > div._2-1k7 > button')))
                voltar.click()
        #Chamar inicio da função
        main()

try:
    main()
except:
    print("Algum erro ocorreu durante a execução")
    try:
        driver.quit()
    except:
        print()
    sys.exit()


