import os
import sys
import time

PASSWORD = 'PASS'

def starter():
    if PASSWORD in os.environ:
        password = os.environ[PASSWORD]
    else:
        password = input("Введите пароль: ")

    if password == 'GwLbQhUY':
        pass
    else:
        print("Ты лох, пароль не верный.")
        time.sleep(4)
        sys.exit()
