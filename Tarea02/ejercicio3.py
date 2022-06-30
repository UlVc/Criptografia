from hashlib import blake2s
from os import urandom

def minar_pumacoin(id, cantidad_mineros):
    """Mina la famosa moneda pumacoin (PMC).
    :param id: Identificador del bloque de transacciones. Debe de estar en binario.
    :param cantidad_mineros: Cantidad de mineros participando en la red.
    """
    print(f'Minando pumacoins con el id {id} y {cantidad_mineros} mineros...\n')

    if (cantidad_mineros <= 100):
        prefijo = '242424'
    elif (cantidad_mineros < 5000):
        prefijo = 'f09fa491'
    else:
        prefijo = 'e29a92e29898'

    while True:
        # Generamos bytes aleatorios y vemos si empiezan con el prefijo necesario una vez aplicando blake2.
        x = urandom(16)
        hash = blake2s(id + x)

        if (hash.hexdigest().startswith(prefijo)):
            print(f' > Cadena encontrada: {hash.hexdigest()}')
            print(f' > Digesto que genera: {hash.digest()}')
            print(f' > Cadena usada: {id}||{x}\n')
            return x

if __name__ == '__main__':
    id1 = bytes.fromhex('d1c5593465eb5bfb9fcad9adf90af61f')
    pt1 = minar_pumacoin(id1, 50)

    id2 = bytes.fromhex('73bf71c8cd6f03c414cd2477a17570c4')
    pt2 = minar_pumacoin(id2, 1000)

    id_op = bytes.fromhex('68188585019b02d746b48b4d06c15dcf')
    pt_op = minar_pumacoin(id_op, 5000)
