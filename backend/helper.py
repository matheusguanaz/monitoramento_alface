from datetime import date
from datetime import datetime

def criarJSON(chaves,valores):
    res = {}
    valores = list(valores) 
    for key in chaves: 
        for value in valores:
            if(type(value)==date):
                print(datetime.now())
                res[key] = value.strftime("%d/%m/%y")
                valores.remove(value)
            elif (type(value)==datetime):
                res[key] = value.strftime("%H:%M:%S")
                valores.remove(value)
            else: 
                res[key] = value 
                valores.remove(value) 
            break
    return res

def mapperUV(valor):  
    if(valor <= 0.05):
        return 0
    elif(valor > 0.05 and valor < 0.227):
        return 1
    elif(valor >= 0.227 and valor < 0.318):
        return 2
    elif(valor >= 0.318 and valor < 0.408):
        return 3
    elif(valor >= 0.408 and valor < 0.503):
        return 4
    elif(valor >= 0.503 and valor < 0.606):
        return 5
    elif(valor >= 0.606 and valor < 0.696):
        return 6
    elif(valor >= 0.696 and valor < 0.795):
        return 7
    elif(valor >= 0.795 and valor < 0.881):
        return 8
    elif(valor >= 0.881 and valor < 0.976):
        return 9
    elif(valor >= 0.976 and valor < 1.079):
        return 10
    elif(valor >= 1.170):
        return 11
    else:
        return -1
