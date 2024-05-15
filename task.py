import requests;
import os;
from datetime import datetime;
from datetime import date;
from email_send import alert_email;
from PyPDF2 import PdfReader;
import json;





def date_current():
    
    now = datetime.now();
    day = str(now.day);
    month = now.month;
    year = str(now.year);

    WEEKDAYS = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo");
    
    arrayMonths = ("enero","febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
    
    monthWord = arrayMonths[month-1];
    month = str(month);

    weekday = WEEKDAYS[now.weekday()];
    
    return [year,month, monthWord, day, weekday];


def extrac():

    data = open(r"Boletin.pdf","rb")
    reader = PdfReader(data);
    page = reader.pages[1];

    archivo = page.extract_text()

    file = open("extrac.txt","r+")
    file.write(archivo);
    file.close();
    print("texto extraido")




def productos(date):

    extrac();

    value = False;

    
    with open("extrac.txt", "r+") as linea:
        for a in linea:
            arrayWords = a.split();
            if(len(arrayWords) >= 2):
                if(value):
                    if("CABEZONA" == arrayWords[1]):

                        if("ROJA"  == arrayWords[2]):
                            cebolla = arrayWords[0]+" "+arrayWords[1]+" "+arrayWords[2]+" "+arrayWords[8];
                            cebolla = cebolla.split("$");
                            cebolla[1] = float(cebolla[1]);


                        
                if("CEBOLLA" == arrayWords[0]):
                    value = True;
                    
                    
                if("FRIJOL" == arrayWords[0]):
                    frijol = arrayWords[0]+" "+arrayWords[1]+" "+arrayWords[7];
                    frijol = frijol.split("$");
                    frijol[1] = float(frijol[1]);
                    
                    
                    
                if("TOMATE" == arrayWords[0]):
                    if("CHONTO" == arrayWords[1]):
                        tomate = arrayWords[0]+" "+arrayWords[1]+" "+arrayWords[7];
                        tomate = tomate.split("$");
                        tomate[1] = float(tomate[1]); 
                        
                        
                if("MAZORCA" == arrayWords[0]):
                    mazorca = arrayWords[0]+" "+arrayWords[6];
                    mazorca = mazorca.split("$");
                    mazorca[1] = float(mazorca[1]);
                    
                    
                if("PIMENTON" == arrayWords[0]):
                    pimento = arrayWords[0]+" "+arrayWords[6];
                    pimento = pimento.split("$");
                    pimento[1] = float(pimento[1]);
                    


    return [{"name" : cebolla[0],"price": cebolla[1],"location": "Bogota","date" : date[3]+"-"+date[1]+"-"+date[0]},
            {"name" : frijol[0],"price": frijol[1],"location": "Bogota","date" : date[3]+"-"+date[1]+"-"+date[0]},
            {"name" : tomate[0],"price": tomate[1],"location": "Bogota","date" : date[3]+"-"+date[1]+"-"+date[0]},
            {"name" : mazorca[0],"price": mazorca[1],"location": "Bogota","date" : date[3]+"-"+date[1]+"-"+date[0]},
            {"name" : pimento[0],"price": pimento[1],"location": "Bogota","date" : date[3]+"-"+date[1]+"-"+date[0]},
            {"year" : date[0],"month" : date[1],"monthWord": date[2],"day" : date[3],"weekday" : date[4]}]














def save_price():
    
    date = date_current();
    products = productos(date);
    array_words = [];
    
    # los dos primero with es para eliminar el ] en el archivo json para poder concaternar el nuevo objeto json
    
    with open("historical_prices.json","r+",encoding="utf-8") as historical_prices:
        for linea in historical_prices:
            array_words.append(linea);
    array_words.pop();
    text = "".join(array_words)
    text.replace("\n", "")
    print(text)     

    with open("historical_prices.json","w") as historical_prices:
        historical_prices.write(text)


    with open("historical_prices.json","a") as historical_prices:
            data = json.dumps(products, indent=4)
            historical_prices.write(","+"\n"+data+"\n"+"]")
     




def alert_price():
    date = date_current();
    products = productos(date)
    
    with open("info_users.json","r+") as file_info_users:
        content = json.loads(file_info_users.read());
        for user in  content:
            index = user['index']
            print(products[index]['price'])
            print(user['value'])
            if((products[index]['price']*1000) >= user['value']):
                alert_email(user["email"],f"{products[index]['name']} HA LLEGADO A UN PRECIO DE {(products[index]['price']*1000)} X KILOS")
                del content[content.index(user)]
                with open("python/info_users.json","w") as file_info_users:
                    file_info_users.write(json.dumps(content, indent=4))
            
            











def dowload_save():
    
    print("se ejecuto el la descarga y guardado")
    my_date_hoy = date_current(); 
    
    year = my_date_hoy[0];
    month = my_date_hoy[1];
    monthWord = my_date_hoy[2];
    day = my_date_hoy[3]; 
    
    print(my_date_hoy)

    url_base = "https://boletin.precioscorabastos.com.co/wp-content/uploads/"
    """url_date = f"{year}/0{month}/Boletin-0{day}{monthWord}{year}.pdf"""
    
    
    if(int (day) > 10):
        url_date = f"{year}/0{month}/Boletin-{day}{monthWord}{year}.pdf"
        if( int (month) > 10):
            url_date = f"{year}/{month}/Boletin-{day}{monthWord}{year}.pdf"
        else:
            url_date = f"{year}/0{month}/Boletin-{day}{monthWord}{year}.pdf"         
    
    else:
        url_date = f"{year}/0{month}/Boletin-0{day}{monthWord}{year}.pdf" 
        if( int (month) > 10):
            url_date = f"{year}/{month}/Boletin-0{day}{monthWord}{year}.pdf"
        else:
            url_date = f"{year}/0{month}/Boletin-{day}{monthWord}{year}.pdf" 


                
    
        


    url = url_base + url_date
    res = requests.get(url);
    print(res)       



    
    if res.status_code == 200:
        with open("Boletin.pdf",'wb') as document:
                document.write(res.content)
                print("boletin guardado")
                with open("historical_prices.json", "r+") as extrac:
                    my_date = date(int (my_date_hoy[0]), int (my_date_hoy[1]),int (my_date_hoy[3]))
                    content = json.loads(extrac.read());
                    index = len(content)-1;
                    two_index = len(content[index])-1;
                    date_historical = [int (content[index][two_index]['year']),int (content[index][two_index]['month']),int (content[index][two_index]['day'])]
                    my_date_historical = date(date_historical[0],date_historical[1],date_historical[2])
                    if(my_date > my_date_historical):
                        save_price();
        alert_price()
    else:
        print("email enviado");
        alert_email("ca30850@gmail.com","REVISAR LA API");            

 


          



    


