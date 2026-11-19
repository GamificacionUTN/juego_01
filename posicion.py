"""================================================================================================
Institute...: Universidad Técnica Nacional
Campus......: Pacífico
Career......: Tecnologías de Información
Period......: 3-2026
Document....: posicion.py
Goals.......: Screen position manager, using the Windows kernel
Professor...: Jorge Ruiz (york)
Student.....:
================================================================================================"""
from ctypes import Structure, windll, c_short


# Standard output device, this is the active console screen buffer
STD_OUTPUT_HANDLE = -11


# pass is a null operation, when it is executed, nothing happens.
# It is useful as a placeholder when a statement is required syntactically,
# but no code needs to be executed, for example:
#   def f(arg): pass    # a function that does nothing (yet)
#   class C: pass       # a class with no methods (yet)
class COORD (Structure):
    pass


# define position on screen same form that cartesian blueprint
COORD._fields_ = [("X", c_short), ("Y", c_short)]


# function to position cursor on screen and print text,
# used in the main code
def print_at(r, c, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
    print(s)


# function to position cursor on screen
