

from machine import Pin, I2C
import BME280
from microdot import Microdot, send_file
import time, ujson, _thread
import network

# ESP32 - Pin assignment
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
bme = BME280.BME280(i2c=i2c)


def connect_to(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid,password)
        while not sta_if.isconnected():
            print(".", end="")
            time.sleep(.1)
        print()
    print('network config:', sta_if.ifconfig())
    return sta_if.ifconfig()[0]
# paralelo ----
C = 0
def medicion_sensor():
    global C
    while True:
        C = bme.temperature
        print('Temperature: ', C)
        time.sleep(5)
# -------------

def medir_sensor():
    temp = bme.temperature
    print('Temperature: ', temp)
    return temp

def conectar_microdot():
    app = Microdot()

    @app.route('/')
    def index(request):
        print("Enviando index.html")
        return send_file("index.html")

    @app.route("/assets/<dir>/<file>")
    def assets(request, dir, file):
        """
        sirve para que el archivo html pueda usar los archivos dentro de la esp32, los solicita con el src='assets/js/code.js'
    
        Funcion asociada a una ruta que solicita archivos CSS o JS
        request (Request): Objeto que representa la peticion del cliente
        dir (str): Nombre del directorio donde esta el archivo
        file (str): Nombre del archivo solicitado
        returns (File): Retorna un archivo CSS o JS
        """
        print("enviando: ", file)
        return send_file("/assets/" + dir + "/" + file)

    @app.route('/data/update')
    def index(request):
        temp = medir_sensor()
        temp = temp.replace("C","")
        json_data = ujson.dumps({"temp":temp})
        return json_data, 202, {'Content-Type': 'json'}

    app.run(port=80)


if __name__ == "__main__":
    try:
        # Me conecto a internet
        ip = connect_to("Estudiantes", "educar_2018")
        
        # Muestro la direccion de IP
        print("Microdot corriendo en IP/Puerto: ",ip+":80")

        # Inicio la aplicacion
        print("Iniciando microdot")
        conectar_microdot()
    
    except KeyboardInterrupt:
        # Termina el programa con Ctrl + C
        print("Aplicacion terminada")



