from hashlib import sha256
from tqdm import tqdm # Ayuda a visualizar el estado de un ciclo.

def crackear_hash(usuario, hash_dado, contrasenas):
    """Crackea el hash dado mediante fuerza bruta.
    :param usuario: Usuario del hash que se está crackeando. No influye en el crackeo per se, pero se pasa para guardarlo en un archivo.
    :param hash_dado: Hash a crackear. Se considera que tiene el formato $sal$hash.
    :param contrasenas: Lista de contraseñas para hacer un ataque de diccionario.
    """
    sal = hash_dado[1:13]
    hash = hash_dado[14:]
    sal_bytes = bytes.fromhex(sal)

    print('Empezando el crackeo...\n')
    print(f' > Hash crackeando: {hash}\n > Sal: {sal}')

    for c in tqdm(contrasenas):
        c = bytes(c, 'latin-1')

        # Formamos las dos opciones de hash posibles.
        hash1 = sha256(c + sal_bytes).hexdigest()
        hash2 = sha256(sal_bytes + c).hexdigest()

        if (hash1 == hash or hash2 == hash):
            print('¡Contraseña encontrada!')

            with open('contrasenas_jaqueadas.txt', 'a') as f:
                f.write(f'{usuario} {hash_dado} {c.decode("latin-1")}\n')
                f.close()

            break

if __name__ == '__main__':
    usuarios, hashes, contrasenas = [], [], []

    with open('./BD_jaqueada.txt', 'r') as archivo:
        for linea in archivo:
            l = linea.split(' ')
            usuarios.append(l[0].replace('\n', ''))
            hashes.append(l[1].replace('\n', ''))

    print('\nCargando contraseñas en memoria...')
    with open('./realhuman_phill.txt', 'r', encoding='latin-1') as archivo:
        contrasenas = [linea.replace('\n', '') for linea in tqdm(archivo)]
    print('Contraseñas cargadas en memoria.\n')

    for i in range(len(hashes)):
        crackear_hash(usuarios[i], hashes[i], contrasenas)
