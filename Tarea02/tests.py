import os
import hashlib
from tqdm import tqdm

print('\nCargando contraseñas en memoria...')
with open('./realhuman_phill.txt', 'r', encoding='latin-1') as archivo:
        # .replace('!', '').replace('(', '').replace(')', '').replace('*', '').replace('[', '').replace(']', '').replace('$', '').replace('#', '').replace('"', '')
    contrasenas = [linea.replace('\n', '') for linea in tqdm(archivo)]
print('Contraseñas cargadas en memoria.\n')
print('guapa000' in contrasenas)
