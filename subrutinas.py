"""================================================================================================
Institute...: Universidad Técnica Nacional
Campus......: Pacífico
Career......: Tecnologías de Información
Period......: 3-2026
Document....: subrutinas.py
Goals.......: Define the methods to be used in the dungeon game.
Professor...: Jorge Ruiz (york)
Student.....:
================================================================================================"""
import os

from posicion import print_at


# Draw a frame on the console screen
def marco(col1, fil1, col2, fil2):
    for fl in range(fil1, fil2 + 1):
        for cl in range(col1, col2 + 1):
            if (fl == fil1) or (fl == fil2):
                # Print horizontal line (top - bottom)
                print_at(fl, cl, '═')
            elif ((cl == col1) or (cl == col2)) and ((fl > fil1) or (fl < fil2)):
                # Print vertical line (left - right)
                print_at(fl, cl, '║')

            # Print the higher corners
            if (fl == fil1) and (cl == col1):
                print_at(fl, cl, '╔')
            elif (fl == fil1) and (cl == col2):
                print_at(fl, cl, '╗')

            # Print the lower corners
            if (fl == fil2) and (cl == col1):
                print_at(fl, cl, '╚')
            elif (fl == fil2) and (cl == col2):
                print_at(fl, cl, '╝')


# Function to create a graphic map
def mapa():
    mapa = []
    try:
        ruta_mapa = os.path.join(os.path.dirname(__file__), 'mapas', 'mapa_01.txt')
        with open(ruta_mapa, mode='r', encoding='utf-8') as archivo:
            mapa = [list(linea.rstrip('\r\n')) for linea in archivo]
    except OSError as error:
        print('Error al leer el archivo:', error)

    return mapa


def valida(mapa, posX, posY):
    if posY < 0 or posY >= len(mapa):
        return False
    if posX < 0 or posX >= len(mapa[posY]):
        return False
    return mapa[posY][posX] in (' ', '$', 'K', '^', '*')

def enviarArduino(comando, puerto=None):
    try:
        if puerto is not None and puerto.is_open:
            puerto.write(comando.encode('ascii'))
            puerto.flush()
    except (OSError, AttributeError):
        return False
    return True