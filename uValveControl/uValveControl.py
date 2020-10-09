'''
Created on 10 set 2020

@author: andrea
'''
from pyb import Pin, delay, USB_VCP,millis
from machine import WDT
import uasyncio
import martinLib

class Dati(): #valori di default
    Cambio = 0 #variabile flag pe qundo si cambia il tempo press pulsante
    Ton = 30
    Toff = 800
    T_Press = 2000

Versione_ = '0.2'

Seriale = USB_VCP()
P_Apri = Pin('Y1',Pin.IN)#, Pin.PULL_UP)
P_Chiudi = Pin('Y2',Pin.IN)#, Pin.PULL_UP)
Valvola = Pin('Y3', Pin.OUT_PP)
Rem_Loc = Pin('Y4', Pin.IN)
Led_Rem = Pin('Y5',Pin.OUT_PP)
Led_Loc = Pin('Y6',Pin.OUT_PP)
Led_Alr = Pin('Y7',Pin.OUT_PP)
Crea_Pulsante = 0 #var per creare i pulsanti una sola volta

Wdt = WDT(timeout=50000) #attiva il watch dog


def Scrivi_Configurazione(): #scrivi il file json con i valori dei parametri
    martinLib.Write_Config(ton=Dati.Ton, toff=Dati.Toff, tpress=Dati.T_Press)
    
def Leggi_Configurazione(**Parametri):# #leggi al file json i parametri salvati
    valori = martinLib.Read_Config(**Parametri) #parametri passati con kwargs
    Dati.Ton = valori['ton']
    Dati.Toff = valori['toff']
    Dati.T_Press = valori['tpress']

async def main(mod):
    x = uasyncio.create_task(Comunicazione(mod))# lancia la funzione in asincrono
    await uasyncio.sleep_ms(5)# attendi un pò...
    x.cancel() #uccidi il processo asincrono

async def Comunicazione(mod):# funzione lanciata in modo asincrono (anti blocco)
    #if Seriale.any() == True:
    Comando = Seriale.read() #leggi il buffer della seriale
    Comando = Comando.decode() #decodifica bin-->utf
    Comando = Comando.split(' ') #divit dove ce '='
    #delay(300)
    #print('Ricevuto--> ',Comando)
    if Comando[0] == 'v_stat':#lista dei comandi implementati
        Seriale.send(Valvola.value())
    elif Comando[0] == 'mod_stat':
        Seriale.send(Rem_Loc.value())
    elif Comando[0] == 'version':
        Seriale.send('Ver {0}'.format(Versione_))
    elif Comando[0] == 'test':
        martinLib.Test_Led(Valvola,Led_Rem,Led_Loc,Led_Alr)
    elif Comando[0] == 'tpress':
        Dati.T_Press = int(Comando[1])
        Dati.Cambio = 1
        Scrivi_Configurazione()
    elif Comando[0] == 'ton':
        Dati.Ton = int(Comando[1])
        Scrivi_Configurazione()
        #print('ton= ',Dati.Ton)
    elif Comando[0] == 'toff':
        Dati.Toff = int(Comando[1])
        Scrivi_Configurazione()
        #print('toff= ',Dati.Toff)
    elif Comando[0] == 'param':
        Val_conf = martinLib.Read_Config()
        print('START, '+str(Val_conf)+' ,END')
    if mod == 0:
        if Comando[0] == 'open':
            Valvola.high()
        elif Comando[0] == 'close':
            Valvola.low()
            
def Modulo_Pulsante_Doppio():
    if Apri.Holding_Time() == 1:
        Valvola.high()
    if Chiudi.Holding_Time() == 1:
        Valvola.low()
'''
def Modulo_Pulsante_Singolo():
    if Apri.Holding_Time() == 1:
      if Valvola.value() == 0:
          Valvola.high()
      elif Valvola.value() == 1:
            Valvola.low()
'''
martinLib.Test_Led(Valvola,Led_Rem,Led_Loc,Led_Alr)
Leggi_Configurazione(ton=Dati.Ton, toff=Dati.Toff, tpress=Dati.T_Press)

while True:
    Wdt.feed() #resetta conteggio watc dog
    if Seriale.isconnected() == True:
        martinLib.Blink(Dati.Ton, Dati.Toff, Led_Alr)
        Seriale = USB_VCP()
    elif Seriale.isconnected() == False:
        Led_Alr.low()
        Seriale.close()
    if Rem_Loc.value() == 0:#attiva mod remota
        Led_Rem.high()
        Led_Loc.low()

    elif Rem_Loc.value() == 1: #attiva mod manuale
        Led_Rem.low()
        Led_Loc.high()
        if Dati.Cambio == 1 or Crea_Pulsante == 0:
            Apri = martinLib.Holding_Pulse(P_Apri, Dati.T_Press)
            Chiudi = martinLib.Holding_Pulse(P_Chiudi, Dati.T_Press)
            Dati.Cambio = 0
            Crea_Pulsante = 1
        Modulo_Pulsante_Doppio()
        #Modulo_Pulsante_Singolo()

    if Seriale.any() == 1:
        uasyncio.run(main(Rem_Loc()))
        Seriale.close()
        
            
            
