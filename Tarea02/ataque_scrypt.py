from hashlib import scrypt # https://www.tarsnap.com/scrypt.html
from tqdm import tqdm

N = 2**16 # Costo de memoria/CPU. Representa el número de iteraciones a hacer.
R = 8 # Tamaño del bloque.
P = 1 # Factor de paralelismo.
MAXMEM = 2**30 # Máximo de bytes que se puede usar en la RAM.
LONGITUD = 32 # Longitud del hash en bytes

def fuerza_bruta(hash_dado, sal, contrasenas):
    print('Empezando el crackeo...\n')
    print(f' > Hash crackeando: {hash_dado}\n > Sal: {sal}')

    for c in tqdm(contrasenas):
        c = bytes(c, 'latin-1')
        hash = scrypt(c, salt=sal, n=N, r=R, p=P, maxmem=MAXMEM, dklen=LONGITUD).hex()

        if hash == hash_dado:
            return hash

if __name__ == '__main__':
    contra_hash = '5f495364792782144918397bdbb72bc04326a883138a11f3d0b61a3d2576ca00'
    sal = bytes.fromhex('d8201aae236713fefe9a5266dc1f8012')

    print('\nCargando contraseñas en memoria...')
    with open('./realhuman_phill.txt', 'r', encoding='latin-1') as archivo:
        contrasenas = [linea.replace('\n', '') for linea in tqdm(archivo)]
    print('Contraseñas cargadas en memoria.\n')

    a = fuerza_bruta(contra_hash, sal, contrasenas)
    print(f'Contraseña encontrada: {a}')
