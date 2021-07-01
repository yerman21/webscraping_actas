#!/usr/bin/env python
# coding: utf-8

# ## ACTAS DE VOTACION

# https://www.resultadossep.eleccionesgenerales2021.pe/SEP2021/Actas/Numero/

# In[1]:


import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# In[2]:


def tiny_file_rename(newname, folder_of_download,time_to_wait):
    time_counter = 0
    filename = max([f for f in os.listdir(folder_of_download)], key=lambda xa :   os.path.getctime(os.path.join(folder_of_download,xa)))
    while '.part' in filename:
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise Exception('Espere demasiado para descargar el archivo')
    os.rename(os.path.join(folder_of_download, filename), os.path.join(folder_of_download, newname))
#Fuente:https://stackoverflow.com/questions/34548041/selenium-give-file-name-when-downloading


# In[3]:


# Ruta de la carpeta de descargas
newpath = os.path.join(os.getcwd(), "archivos_descargados")

profile = webdriver.FirefoxProfile() 
profile.set_preference("browser.download.dir", newpath)
profile.set_preference("browser.download.folderList", 2) 
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain,text/x-csv,text/csv,application/ms-excel,application/vnd.ms-excel,application/csv,application/x-csv,text/csv,text/comma-separated-values,text/x-comma-separated-values,text/tab-separated-values,application/pdf")

caps = DesiredCapabilities.FIREFOX

driver = webdriver.Firefox(firefox_profile=profile,
                            capabilities=caps,
                           #Si no tienes el geckodriver en el path de tu sistema, puedes especificar la ruta
                            executable_path='C:\\Users\\yerman\\Documents\\Selenium\\geckodriver.exe')


# In[5]:


driver.get("https://www.resultadossep.eleccionesgenerales2021.pe/SEP2021/Actas/Numero")


# In[6]:


input_mesa = driver.find_element("css selector", "input.input_mesas")
input_mesa.get_attribute("outerHTML")


# In[7]:


numero_mesa = "034244"


# In[8]:


input_mesa.send_keys(numero_mesa)
time.sleep(2)
input_mesa.send_keys(Keys.ENTER)


# In[9]:


driver.find_element("css selector", "div.botonera_print a:nth-child(2)").click()


# In[10]:


urlActaImg = driver.find_element("css selector", "div.gutters-20 div:nth-child(2) a").get_attribute("href")
urlActaImg


# In[11]:


driver.find_element("css selector", ".borde_gris.text-center").text


# In[12]:


ubicacion_votacion = driver.find_element("css selector", ".borde_gris.text-center").text.split("\n")
ubicacion_votacion


# In[13]:


ubicacion_votacion[2] = numero_mesa
ubicacion_votacion


# In[14]:


ubicacion_votacion = " - ".join(ubicacion_votacion)
ubicacion_votacion


# In[15]:


ubicacion_votacion = ubicacion_votacion.replace("NOMBRE DE LOCAL: ", "").replace(" - ", "_")
ubicacion_votacion


# In[16]:


tiny_file_rename(ubicacion_votacion+".csv", newpath, time_to_wait=60)


# In[17]:


pdf_path = os.path.join(newpath, ubicacion_votacion+".pdf")
pdf_path


# In[18]:


response = requests.get(urlActaImg, stream=True)
with open(pdf_path, 'wb') as f:
    f.write(response.content)


# In[19]:


driver.close()


# In[ ]:





# ### Masimo

# In[20]:


numeros_mesa = ["030390", "030391", "034244" , "034245"]


# In[21]:


driver = webdriver.Firefox(firefox_profile=profile,
                            capabilities=caps,
                            executable_path='C:\\Users\\yerman\\Documents\\Selenium\\geckodriver.exe')


# In[22]:


driver.get("https://www.resultadossep.eleccionesgenerales2021.pe/SEP2021/Actas/Numero")
for n_mesa in numeros_mesa:
    print(f"------------{n_mesa}------------")
    print("Detectando input...")
    input_mesa = driver.find_element("css selector", "input.input_mesas")    
    time.sleep(3)
    input_mesa.clear()
    input_mesa.send_keys(n_mesa)
    time.sleep(1)
    print("Buscando...mesa n°"+n_mesa)
    input_mesa.send_keys(Keys.ENTER)
    time.sleep(5)
    
    table = driver.find_elements("css selector", "div.row.gutters-20 table.table.table-striped.tabla_resultado")[1]
    ubicacion_votacion = driver.find_element("css selector", ".borde_gris.text-center").text.split("\n")
    ubicacion_votacion[2] = n_mesa
    ubicacion_votacion = " - ".join(ubicacion_votacion)
    ubicacion_votacion = ubicacion_votacion.replace("NOMBRE DE LOCAL: ", "").replace(" - ", "_")
    print("Nombre de archivo: "+ubicacion_votacion)
    
    time.sleep(2)
    driver.find_element("css selector", "div.botonera_print a:nth-child(2)").click()
    print("Descargando: "+ubicacion_votacion+".csv")
    tiny_file_rename(ubicacion_votacion+".csv", newpath, time_to_wait=60)
    
    time.sleep(3)
    urlActaPdf = driver.find_element("css selector", "div.gutters-20 div:nth-child(2) a").get_attribute("href")
    print("URL PDF: "+urlActaPdf)
    pdf_path = os.path.join(newpath, ubicacion_votacion+".pdf")
    
    response = requests.get(urlActaPdf, stream=True)    
    with open(pdf_path, 'wb') as f:
        f.write(response.content)
        print("Descargando: "+ubicacion_votacion+".pdf")


# In[23]:


driver.close()

