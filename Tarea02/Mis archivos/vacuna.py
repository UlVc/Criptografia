from sys import argv
import os

def vacuna(archivo, llave):
    """Aplica la vacuna al archivo dado.
    :param archivo: Archivo a aplicar la vacuna.
    :param llave: Llave para desencriptar.
    """
    with open(archivo.replace('.enc', ''), 'wb') as z: # Le quitamos la terminación .enc al archivo.
        # Como se encripto usando XOR, volvemos a usar XOR para regresar al estado original.
        z.write(
             (lambda archivo: bytes([archivo[i] ^ llave[i%16] for i in range(len(archivo))]))
                 (open(archivo, 'rb').read())
        )

    os.remove(archivo)

if __name__ == '__main__':
    y = '\x2e' + '\x78' + '\x79\x7a' # Archivo .xyz

    with open(y, 'rb') as f:
        suma = f.readline() # c + d + k

    # Removemos los bytes c y k para obtener a d.
    d = suma[17:33]

    # Hacemos OR bit a bit que se hizo en el virus para obtener el valor original de d.
    # Una vez hecho esto, d será igual a la llave generada k.
    d = int.from_bytes(d, 'big')
    d |= 1
    d = d.to_bytes(16, 'big')

    # Obtenemos todos los archivos que están en donde está este script.
    _, _, archivos = next(os.walk('./'))
    archivos.remove(argv[0]) # Removemos de la lista de archivos este script.

    # Aplicamos la vacuna.                                                                          
    list(map(lambda x: vacuna(x, d), archivos))
