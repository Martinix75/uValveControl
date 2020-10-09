'''
Created on 15 set 2020

@author: andrea
'''
import time
import ujson
from pyb import delay

version = "0.3.1"

class Holding_Pulse():
    def __init__(self, pulse ,time):
        self.TimeX = time #tempo minimo di pressione pulsante
        self.Pulse = pulse #nome del pulsante da esaminare
        self.Flag_Press = 0 #variabile che per prendere il tempo della press. pulsante
        self.Flag_Relase = 0 #variabile per vedere se il pulsante 猫 stato rilasciato
    def Holding_Time(self):
        if self.Pulse.value() == 0: #valuta se il pulsante indicato 猫 premuto
            if self.Flag_Press == 0:# se la variabile =0 prendi il tempo di sistema
                self.TimeSystem = time.ticks_ms() #prende il tempo di sistema in quel istante
                #print('punto 1')
                self.Flag_Press = 1 #setta la variabile a 1 per non rientrare in questa condi.
            if time.ticks_ms() - self.TimeSystem > self.TimeX and self.Flag_Relase == 0:
                #la line sopra valuta se il tempo ora 猫 > del tempo preso e se la variabile =0
                #print('punt 2')
                self.Flag_Press = 0 #setta la varibile a 0 per poter rientrare a prendre il tempo
                self.Flag_Relase = 1 #setta a 1 per non rientrare se il puls resta premuto molto
                return 1 #torna 1 se il pulsante 猫 premuto per x tempo)
        else:
            self.Flag_Press = 0 #se il pulsante non vien premuto setta a 0 per entrae dopop nel tempo
            self.Flag_Relase = 0 #setta a zero per ntrare nella condizione di accensione/spegnimento     
            return 0 #torna zero(nessun pulsante premuto per x tempo)
        
def Blink(Tempo1, Tempo2, nLed):# funzione per il tempo di lampeggio
    nLed.high()
    delay(Tempo1)# Tempo1 = tempo acceso
    nLed.low()
    delay(Tempo2)# tempo2 = tempo spento

def Read_Config(**Values): #uso un wkargs, anche se molto lento!
    try:
        with open('controller.config', 'r') as _Filex:
            _valx = ujson.load(_Filex)# legge il file json (è un dizionario!)
        return _valx # ritorna il dizionario
    except(OSError):
        Write_Config(**Values)# se il file non ce chiema la funzione per crearlo, passando i parametri
        return Read_Config()
    
def Write_Config(**Values):
    with open('controller.config', 'w') as _Filex:
        ujson.dump(Values, _Filex)
    #return (Values)# ritorna il dizionario(forse non occore!)
    
def Test_Led(Va,Lr, Ll, La): #funzione test per i led (li accende tutti)
    Va.high()
    Lr.high()
    Ll.high()
    La.high()
    delay(1000)
    Va.low()
    Lr.low()
    Ll.low()
    La.low()
    delay(400)


