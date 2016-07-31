import re, sys, signal, os, time, datetime
import requests
from smartcard.System import readers
from smartcard.util import toHexString
import opc
######### LOG #########
import logging
#######################

######### LOG CONFIG #########
logger = logging.getLogger('Papalote_RFID')
hdlr = logging.FileHandler('rfid.log')
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
#################################

# se definen los APDUs
#
COMMAND = [0xff, 0xCA, 0x00, 0x00, 0x00]

####### FACECANDY #######
numLEDs = 100
cliente = opc.Client('localhost:7890')
negro = [ (0,0,0) ] * numLEDs
blanco = [ (255,255,255) ] * numLEDs
rojo = [ (255,0,0) ] * numLEDs
####### ID DE LA EXPERIENCIA ########
Z = 1
E = 2
URL = 'http://papalote.cocoplan.mx/v0/'

def encender_led():
    cliente.put_pixels(negro)
    time.sleep(.1)
    cliente.put_pixels(blanco)
    time.sleep(1.5)
    cliente.put_pixels(negro)

def encender_error():
    cliente.put_pixels(negro)
    time.sleep(.1)
    cliente.put_pixels(rojo)
    time.sleep(.5)
    cliente.put_pixels(negro)

if __name__ == '__main__':
    r = readers()
    #print 'lectores disponibles', r
    logger.info('Lectores Disponibles %s: ',r)
    lector = r[0]
    #print 'Usando :', lector
    logger.info('Usando: %s',lector)

    while(1):
        try:
            conexion= lector.createConnection()
            conexion.connect()
            #### enviar datos ####
            data, sw1, sw2 = conexion.transmit(COMMAND)

            #print "Command: %02X %02X" % (sw1, sw2)
            a = sw1
            #print a
            #logger.info('Comando %s',a)
            if a == 144:
                #print 'datos >:', data
                v = data[::-1]
                #print 'invertido',v
                hexa = toHexString(v)
                hexan = hexa.split( )
                #print 'hexa',hexa
                #print 'hexan',hexan
                tam = len(hexan)
                #print 'leng', tam
                cadena = ''

                for x in range(tam):
                    cadena = cadena + str(hexan[x])

                #print 'cadena',cadena
                decimali = int(cadena,16)
                decimal = str(decimali)
                #print 'decimal',decimal
                rfid = decimal
                print rfid
                ######### Get Historial ########
                url_h = 'historial'
                data = { 'rfid':rfid }
                try:
                    r = requests.get(URL + url_h, params = data)
                    if r.status_code == requests.codes.ok:
                        ########### EXISTE el USUARIO ########
                        json = r.json()
                        h = json.get('historial')
                        ##### SI el historial es Vacio, no Ha ingresado
                        if not h:
                            print 'Permited'
                            encender_led()
                            url_v = 'visitante'
                            data_v = {'rfid':rfid,'experiencia':E,'zona':Z}

                            try:
                                rv  = requests.get(URL + url_v, params = data_v)

                            except requests.ConnectionError as e:
                                logger.error('ERROR %s',e)
                                pass
                            except requests.HTTPError as e:
                                logger.error('ERROR %s',e)
                                pass
                            except requests.ConnectTimeout as e:
                                logger.error('ERROR %s',e)
                                pass
                            except requests.ReadTimeout as e:
                                logger.error('ERROR %s',e)
                                pass
                            except requests.Timeout as e:
                                logger.error('ERROR %s',e)
                                pass

                        else:
                            print 'NotPermited'
                            encender_error()

                    else:
                        ########### NO EXISTE el USUARIO ########
                        print 'NotFound'
                        encender_error()

                except requests.ConnectionError as e:
                    logger.error('ERROR %s',e)
                    pass
                except requests.HTTPError as e:
                    logger.error('ERROR %s',e)
                    pass
                except requests.ConnectTimeout as e:
                    logger.error('ERROR %s',e)
                    pass
                except requests.ReadTimeout as e:
                    logger.error('ERROR %s',e)
                    pass
                except requests.Timeout as e:
                    logger.error('ERROR %s',e)
                    pass


        except Exception, e:
            #logger.error('ERROR %s',e)
            continue
