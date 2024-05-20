"""
Helper functions for the Personal Assistant.
"""
import os
import platform
from colorama import init, Fore, Back
from pyfiglet import Figlet

init(autoreset=True)

def clear_screen():
    """
    Clear the terminal screen.
    """

    os_name = platform.system().lower()
    if 'windows' in os_name:
        os.system('cls')
    else:
        os.system('clear')

def hello_screen():
    """
    Print the welcome screen.
    """

    # Створення тексту за допомогою Figlet
    figlet = Figlet(font='slant')
    welcome_text = figlet.renderText('BRO Assistant')

    # Вивід заставки з кольоровим текстом
    print(Fore.YELLOW + Back.BLUE + welcome_text)
    print(Fore.YELLOW + Back.BLUE + "Ласкаво просимо до вашого персонального помічника!")
    print(Fore.YELLOW + Back.BLUE + "Введіть команду (або 'exit' для виходу):")
