import RPi.GPIO as GPIO
import requests
import math
import random
import threading
import json
from time import sleep
from wiringpi import Serial

import socket
import smtplib
import os
import sys

sender_address = "lmegaleox@gmail.com"
sender_password = "MegamanX123"
sender_server = 'smtp.gmail.com'
sender_port = 587
recipient_address = "leandrocazar07102000@gmail.com"

KEY="ABUAAPYLN2G79YWL"#Poner aqui su Key de escritura
KEYREAD="1635496"#Poner aqui su key de lectura

baud = 9600
ser  = Serial("/dev/serial0",baud)
sleep(0.3)

#Datos que provienen de la empresas

numcamion = 10
Dpeso = 0.50 
cargacamion = 10000
metadiaria = 0


def calcularprecio(numkg):
 precio = numkg * Dpeso 
 return precio

def camiones(numkg):
 cam = numkg/cargacamion
 redondeo = math.ceil(cam)
 cam = redondeo
 return cam
 
def mysleep(delay): 
 start = time() 
 while time()-start < delay:
  pass

def enviarThingSpeak(peso, valor, camiones):
    value_1 = peso
    value_2 = valor
    value_3 = camiones
    lista = [value_1,value_2,value_3] 
    if len(lista) == 3:
     enviar = requests.get("https://api.thingspeak.com/update?api_key="+KEY+"&field1="+str(lista[0])+"&field2="+str(lista[1])
                                   +"&field3="+str(lista[2]))  #cuando se quiere enviar dos o mas datos
    #enviar = requests.get("https://api.thingspeak.com/update?api_key=B3ZRHNV2DUMV48XB&field1="+str(lista[0]))
    if enviar.status_code == requests.codes.ok:
     if enviar.text != '0':
      print("Datos enviados correctamente")
     else:
      print("Tiempo de espera insuficiente (>15seg)")
    else:
      print("Error en el request: ",enviar.status_code)
	  #else:
	  #print("La cadena recibida no contiene 2 elementos, sino:",len(lista),"elementos")

"""def get_device_ip_address():

    try: 
        if os.name == "nt":
            # On Windows
            result = "Running on Windows"
            hostname = socket.gethostname()
            result += "\nHostname:  " + hostname
            host = socket.gethostbyname(hostname)
            result += "\nHost-IP-Address:" + host
            return result

        elif os.name == "posix":
            gw = os.popen("ip -4 route show default").read().split()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((gw[2], 0))
            ipaddr = s.getsockname()[0]
            gateway = gw[2]
            host = socket.gethostname()
            result = "OS:\t\tRaspbian\nIP:\t\t" + ipaddr + "\nGateway:\t" + gateway + "\nHost:\t\t" + host
            return result
        
        else:
            result = os.name + " no funciona en este sistema."
            return result
    except:
        return "No detecta la IP"
"""
def send_email(text):
    try:
        message = "From: " + sender_address + "\nTo: " + recipient_address + "\nSubject: Raspberry\n\n" + text 

        server = smtplib.SMTP(sender_server, sender_port)
        server.ehlo()
        server.starttls()
        server.login(sender_address, sender_password)
        server.sendmail(sender_address, recipient_address, message)
        server.close()
        print("Mensaje enviado por:\n", message)

    except:
        print("Fallo. Lee el punto 1 del tutorial.")
	
def recibir(echo = True):
 data = ""
 while True:
  input = ser.getchar()
  if echo:
   ser.putchar(input)
  if input == "\r":
   return (data)
  data += input
 sleep(0.2)
  
def printsln(menss):
 ser.puts(menss+"\r")
 sleep(0.2)

def prints(menss):
 ser.puts(menss)
 sleep(0.2)

def main () :

# Setup

 #peripheral_setup()

# Infinite loop
 while 1 :
  prints("Recibiendo datos... ")
  mensaje = recibir()
  nuevo = mensaje.replace("T","")
  peso = nuevo.replace("=","")
  print(str(peso.isdigit()))
  if(peso.isdigit()):
    peso_final = int(peso)
    precio = calcularprecio(peso_final)
    camion = camiones(peso_final) 
    prints(" El precio a recibir es de ")
    printsln(str(peso_final))
    prints(" El numero de camiones necesarios es de ")
    printsln(str(camion))
    enviarThingSpeak(peso, precio, camion)
    meta = metadiaria + peso_final
    metalograda = True
    if(meta > 100000 and metalograda):
      message = "Se ha cumplido las metas diarias"
      printsln(message)
      send_email(message)
      metalograda = False

if __name__ == '__main__' :
   main()