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
# Call external functions
from posicion import *
import os


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


# Function to clean game area
def limpiar():
    for fl in range(6, 20):
        for cl in range(2, 120):
            print_at(fl, cl, ' ')


# Function to create a graphic map
def mapa():
    mapa = []
    os.chdir(os.getcwd() + '/mapas')
    try:
        # Open file whith only read mode
        archivo = open('mapa_01.txt', mode='r', encoding='utf-8')

        continua = True
        while continua:
            linea = archivo.readline()
            fila = []
            if linea != '':
                for carac in linea:
                    fila.append(carac)
                mapa.append(fila)
            else:
                break

        # Close file
        archivo.close()
    except:
        print('Error al leer el archivo')

    return mapa


def valida(mapa, posX, posY):
    if mapa[posY][posX] == ' ':
        return True
    else:
        return False
