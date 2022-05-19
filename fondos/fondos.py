from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests as req
import pandas as pd

import time
import datetime  # manejo temporal


from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

PATH = r'C:\Users\ragod\Desktop\reposicion\Proyectos_TB\Proyectos_TB\Funciones\chromedriver.exe'  #'driver/chromedriver'
usuario=UserAgent().random


from selenium import webdriver  # driver selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By   # para elegir por elemento
from selenium.webdriver.support.ui import WebDriverWait # para el time sleep
from selenium.webdriver.support import expected_conditions as EC # condiciones esperadas
from selenium.webdriver import ActionChains as AC # acciones en cadena
url='https://www.morningstar.es/es/'
driver=webdriver.Chrome(PATH) 
driver.get(url)

time.sleep(3)
mis_fondos =pd.read_excel(r'C:\Users\ragod\Desktop\reposicion\Proyectos_TB\Proyectos_TB\fondos\fondos.xlsx', sheet_name ='Fondos',header = 0)
mis_fondos_l =list (mis_fondos.n_nom_fondo)


#Busqueda en MorningStar
saltar_coockies=driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')
saltar_coockies.click()
time.sleep(3)

aceptar_cookies=driver.find_element(By.XPATH,'//*[@id="btn_individual"]') # objeto en la web de busqueda
aceptar_cookies.click() # Boton busqueda


mi_lista_valorada =[]

#buscar fondos

for n in mis_fondos_l:
    buscar=driver.find_element(By.XPATH,'//*[@id="quoteSearch"]').clear()
    producto = n
    buscar=driver.find_element(By.XPATH,'//*[@id="quoteSearch"]')# objeto en la web de busqueda
    buscar.send_keys(producto)  # incrusta la string
    time.sleep(3)
    buscar=driver.find_element(By.XPATH,'//*[@id="GoSearch"]')
    buscar.click()
    buscar=driver.find_element(By.XPATH,'//*[@id="ctl00_MainContent_fundTable"]/tbody/tr[2]/td[1]/a')
    buscar.click()

    precio= (driver.find_element(By.XPATH, '//*[@id="overviewQuickstatsDiv"]/table/tbody/tr[2]/td[3]').text).split()
    fecha =driver.find_element(By.XPATH, '//*[@id="overviewQuickstatsDiv"]/table/tbody/tr[2]/td[1]').text
    fecha=fecha[3:]
    # Crear lista valorada 
    mi_lista_valorada.append([precio[0],precio[1],fecha])

df = pd.DataFrame(mi_lista_valorada, columns = ['moneda','valor','fecha'])
df_final = pd.concat([mis_fondos,df],axis=1)
df_final['valor'] =df_final['valor'].replace(",",".", regex = True).astype(float)
df_final['importe']=df_final.valor*df_final.num_participaciones

url='https://www.xe.com/es/currencyconverter/convert/?Amount=1&From=USD&To=EUR'
driver=webdriver.Chrome(PATH) 
driver.get(url)

cambio =(driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/section/div[2]/div/main/form/div[2]/div[1]/p[2]').text)

t_cambio= cambio.split()[0].replace(',','.')

df_final['t_cambio']=df_final.apply(lambda x: 1 if x.moneda =='EUR' else t_cambio,axis=1).astype(float) 
df_final['importe_euro']=df_final.importe*df_final.t_cambio
fecha = str(datetime.datetime.now())
fecha2 =fecha.split()[0].replace('-','')
archivo_con_fecha = f"{fecha2}_fondos.csv"
# Crea CSV
df_final.to_csv(archivo_con_fecha, index = False)

df_final2=df_final[['n_nom_fondo', 'importe_euro']]
df_final2.append({'n_nom_fondo':'total','importe_euro': 9704.80}, ignore_index = True)
                             