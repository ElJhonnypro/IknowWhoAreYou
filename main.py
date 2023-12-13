# Importar módulos necesarios
import os
import sys
import subprocess
import time
from colorama import Fore, init, Style

# Limpiar la pantalla en varias plataformas
os.system('clear')

# Verificar si el script se está ejecutando como root
try:
    result = subprocess.run(['whoami'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    username = result.stdout.strip() if result.stdout else ''
except subprocess.CalledProcessError:
    print(f'{Fore.RED}Error al ejecutar el comando whoami')
    sys.exit(1)

if username != 'root':
    print(f'{Fore.RED}ERROR: ¡Este script debe ejecutarse como root!')
    sys.exit(1)

# Definir una clase para las opciones del menú
class option:
    def __init__(self, numberoption, helptext):
        self.number = numberoption
        self.help = helptext
    
    def itsselected(self, question):
        if question == self.number:
            return True
        else:
            return False

# Crear instancias de la clase option
option1 = option(1, 'Modo normal: ver IP, sistema operativo, versión de Windows, etc.')

# Inicializar colorama para la salida coloreada
init(autoreset=True)

# Función para verificar si un puerto está abierto en una dirección IP dada
def checkport(port: str, ipadress: str):
    try:
        subprocess.run(['nc', '-zvw', '2', ipadress, port], text=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f'{Fore.GREEN}Puerto {port} abierto en {ipadress}.')
        return True
    except subprocess.CalledProcessError as e:
        if 'Connection timed out' in e.stderr or 'Connection refused' in e.stderr:
            print(f'{Fore.RED}{Style.BRIGHT}Puerto {port} no abierto en {ipadress}.')
            print(f'{Fore.RESET}')
            return False

# Función para verificar la versión de Windows en una dirección IP utilizando crackmapexec
#Desarrollo
def checkwindowsversion(ipadress):
    commandexecute = subprocess.run(['crackmapexec','smb',ipadress])
    print(commandexecute.stdout)

# Función para manejar el menú para la opción 1
def option1menu():
    puertosencontrados = []  # Lista para almacenar puertos encontrados
    os.system('clear')
    print(f'{Fore.BLUE}Modo normal activado...')
    ipadress = input(f'{Fore.RED}{Style.BRIGHT}MODO NORMAL: Ingrese la IP de destino>{Fore.YELLOW} ')
    
    try:
        ttloutput = subprocess.run(['ping', '-c', '1', ipadress], text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True).stdout.split('ttl=')[1].split()[0]
        
        # Determinar si el objetivo es Linux/Mac o Windows según el valor de TTL
        if int(ttloutput) == 64 or int(ttloutput) == 128:
            print(f'TTL: {Fore.BLUE}{ttloutput} Linux o Mac (puede compartir el TTL {ttloutput} en internet)')
        else:
            print(f'TTL: {Fore.BLUE}{ttloutput} Windows o Windows Server (puede compartir el TTL {ttloutput} en internet)')

    except subprocess.CalledProcessError as e:
        print('La página web o dispositivo no existe o hay un error al ejecutarlo')
        print('Ingrese un dato correcto')
        sys.exit(1)

    # Verificar si los puertos comunes (80, 443) están abiertos y agregarlos a la lista
    if checkport('80', ipadress):
        print(f'{Fore.YELLOW}Ingrese al servidor HTTP en: http://{ipadress}/')
        puertosencontrados.append(80)

    if checkport('443', ipadress):
        print(f'{Fore.YELLOW}Ingrese al servidor HTTPS en: https://{ipadress}/')
        puertosencontrados.append(443)

    print('Detectando puertos...')
    
    try:
        rangopuertos = int(input('Rango de puertos> '))
    except:
        print('Ingrese otro rango de puerto válido')
        initmenu()

    # Iterar a través del rango de puertos, verificando y agregando puertos abiertos a la lista
    for i in range(rangopuertos+1):
        # No verificar los puertos 80 o 443
        if i == 80 or i == 443:
            checkport(str(i), ipadress)
        else:
            if checkport(str(i), ipadress):
                puertosencontrados.append(i)
                print(f'{Fore.BLUE}¡Puerto encontrado!')

    # Imprimir los puertos encontrados
    for puerto in puertosencontrados:
        print(f'Puerto encontrado: {puerto}')

# Función para inicializar el menú principal
def initmenu():
    print(
        f"""
        {Fore.RED}{Style.BRIGHT}========================== ¡Hola! Bienvenido a IkWhoAreYou =======================

        {Fore.BLUE}[1]:{Fore.YELLOW} Modo normal (ver IP, Linux/Mac o Windows, versión de Windows, etc)

        {Fore.RED}
        ================================================================================
        """
    )
    try:
        #Conseguimos la opcion elejida
        option = int(input(f'{Fore.BLUE}Seleccione una opción:>{Fore.YELLOW}'))
    except ValueError:
        print('Error: Por favor, ingrese un número o valor válido')
        sys.exit(1)
    except KeyboardInterrupt:
        print('Gracias por utilizar esta herramienta')
        os.system('clear')
        sys.exit(0)
    if option1.itsselected(option):
        option1menu()

# Ejecución principal: inicializar el menú principal y manejar interrupciones de teclado
if __name__ == '__main__':
    try:
        initmenu()
    except KeyboardInterrupt:
        os.system('clear||cls')
        print(f'{Fore.YELLOW}Adiós. Gracias por usar esta herramienta.')
        sys.exit(0)