from fastapi import FastAPI;
from fastapi.middleware.cors import CORSMiddleware;
from typing import Union;
from PyPDF2 import PdfReader;
from cron_job import cron_dowload_save;
from task import date_current;
from task import productos;
import json;



app = FastAPI();

origins =[
    "http://localhost:4321",
    "http://127.0.0.1:5500"   
]




app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

date =  date_current();

data_products = productos(date);

@app.get("/price")

def price():
    date = date_current();
    return data_products;




@app.get("/historical/prices")

def historicalprices():
    #save_price(date);
    file = open("historical_prices.json","r")
    
    return  json.loads(file.read());




@app.post("/alert_price")

def save_infor_users(info_users : dict):
    array_words = [];
    
    # los dos primero with es para eliminar el ] en el archivo json para poder concaternar el nuevo objeto json
    
    with open("python/info_users.json","r+",encoding="utf-8") as file_info_users:
        for linea in file_info_users:
            array_words.append(linea);
    array_words.pop();
    text = "".join(array_words)
    text.replace("\n", "")
  

    with open("info_users.json","w") as file_info_users:
        file_info_users.write(text)


    with open("info_users.json","a") as file_info_users:
            data = json.dumps(info_users, indent=4)
            file_info_users.write(","+"\n"+data+"\n"+"]")
    





if( not(date[4] == "Sabado" or date[4] == "Domingo")):
    cron_dowload_save.start();
     



