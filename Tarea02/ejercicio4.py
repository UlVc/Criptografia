import os
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import ECB

def aes128_ecb_enc(llave, mensaje):
    """Encripta el mensaje dado con AES con modo ECB.
    :param llave: Llave a usar para encriptar.
    :param mensaje: Mensaje a encriptar.
    """
    aes_k = Cipher(AES(llave), ECB())
    enc = aes_k.encryptor()
    return enc.update(mensaje) + enc.finalize()

def aes128_ecb_dec(llave, mensaje):
    """Desencripta el mensaje dado con AES con modo ECB.
    :param llave: Llave a usar para desencriptar.
    :param mensaje: Mensaje a desencriptar.
    """
    aes_k = Cipher(AES(llave), ECB())
    dec = aes_k.decryptor()
    return dec.update(mensaje) + dec.finalize()

def padding(mensaje):
    """Aplica el padding necesario al mensaje dado.
    Consiste en agregar la secuencia de bytes BB...B de longitud igual a B, 
    donde B es un entero entre 1 y 16.
    :param mensaje: Mensaje a aplicar el padding.
    """
    falta = (16-len(mensaje)) % 16 # Longitud de la secuencia restante.
    a_anadir = falta.to_bytes(1, 'big')*falta

    return mensaje + a_anadir

def unpadding(mensaje):
    """Remueve, si es que existe, el padding del mensaje.
    :param mensaje: Mensaje a remover el padding.
    """
    longitud_padding = mensaje[-1]

    if longitud_padding > 15:
        return mensaje
  
    return mensaje[:-longitud_padding]

def xor_bloque(b1, b2):
    """Aplica XOR bit a bit de los dos bloques dados.
    :param b1, b2: Bloques de bits. Ambos bloques deben de tener longitud igual a 16.
    """
    return bytes(b1[i % 16] ^ b2[i % 16] for i in range(16))

def aes128_cbc_enc(llave, mensaje, iv):
    """Encripta el mensaje dado con AES con modo CBC.
    :param llave: Llave a usar para encriptar.
    :param mensaje: Mensaje a encriptar.
    :param iv: Vector de inicialización
    """
    padded = padding(mensaje)
    bloque_anterior = iv
    cifrado = []

    for i in range(0, len(padded), 16):
        bloque = padded[i:i+16]
        bloque_encriptado = aes128_ecb_enc(llave, xor_bloque(bloque, bloque_anterior))
        cifrado += bloque_encriptado
        bloque_anterior = bloque_encriptado

    return bytes(cifrado)

def aes128_cbc_dec(llave, cifrado, iv):
    """Desencripta el mensaje dado con AES con modo CBC.
    :param llave: Llave a usar para desencriptar.
    :param mensaje: Mensaje a desencriptar.
    :param iv: Vector de inicialización
    """
    bloque_anterior = iv
    mensaje = []
  
    for i in range(0, len(cifrado), 16):
        bloque = cifrado[i:i+16]
        # Vemos si el mensaje cifrado que recibimos tiene padding correcto. Esto lo hacemos al intentar hacer
        # xor con los bloques, pues si no tuviera un padding correcto, no se podría hacer xor con el bloque_encriptado.
        # bloque_anterior siempre será de longitud 16 por construcción, por lo que la única opción es que los bloques
        # del mensaje cifrado estén mal, es decir, su padding incorrecto.
        try:
            mensaje += xor_bloque(aes128_ecb_dec(llave, bloque), bloque_anterior)
        except:
            raise Exception('Padding incorrecto')
        bloque_anterior = bloque
    
    return unpadding(bytes(mensaje))
    
def aes128_ctr_enc(llave, mensaje, nonce):
    """Encripta el mensaje dado con AES con modo CTR.
    :param llave: Llave a usar para encriptar.
    :param mensaje: Mensaje a encriptar.
    :param nonce: Vector de longitud 16 aleatorio que solo se puede usar una vez. 
                  En este caso, es equivalente al vector de inicialización (IV).
    """
    padded = padding(mensaje)
    cifrado = []
    contador = 0

    for i in range(0, len(padded), 16):
        contador_unico_bloque = xor_bloque(nonce, contador.to_bytes(16, 'big'))
        bloque = padded[i:i+16]
        bloque_encriptado = aes128_ecb_enc(llave, contador_unico_bloque)
        cifrado += xor_bloque(bloque_encriptado, bloque)
        contador += 1

    return bytes(cifrado)
    
def aes128_ctr_dec(llave, cifrado, nonce):
    """Desencripta el mensaje dado con AES con modo CTR.
    :param llave: Llave a usar para desencriptar.
    :param mensaje: Mensaje a desencriptar.
    :param nonce: Vector de longitud 16 aleatorio que solo se puede usar una vez. 
                  En este caso, es equivalente al vector de inicialización (IV).
    """
    mensaje = []
    contador = 0

    for i in range(0, len(cifrado), 16):
        contador_unico_bloque = xor_bloque(nonce, contador.to_bytes(16, 'big'))
        bloque_encriptado = aes128_ecb_enc(llave, contador_unico_bloque)
        bloque = cifrado[i:i+16]
        # Vemos si el mensaje cifrado que recibimos tiene padding correcto. Esto lo hacemos al intentar hacer
        # xor con los bloques, pues si no tuviera un padding correcto, no se podría hacer xor con el bloque_encriptado.
        # bloque_encriptado siempre será de longitud 16 por construcción, por lo que la única opción es que los bloques
        # del mensaje cifrado estén mal, es decir, su padding incorrecto.
        try:
            mensaje += xor_bloque(bloque_encriptado, bloque)
        except:
            raise Exception('Padding incorrecto')
        contador += 1

    return unpadding(bytes(mensaje))

if __name__ == '__main__': 
    llave = b'Mi llave secreta'
    mensaje = b'Mensaje de texto mas grande que un bloque y de longitud que si es multiplo de 16'
    mensaje2 = b'UwU'
    iv = os.urandom(16)

    cbc_cifrado_1 = aes128_cbc_enc(llave, mensaje, iv)
    ctr_cifrado_1 = aes128_ctr_enc(llave, mensaje, iv)

    cbc_cifrado_2 = aes128_cbc_enc(llave, mensaje2, iv)
    ctr_cifrado_2 = aes128_ctr_enc(llave, mensaje2, iv)

    print('>>>> Mensaje 1:\n')
    print(f'Cifrado con CBC: {cbc_cifrado_1}')
    print(f'Cifrado con CTR: {ctr_cifrado_1}')
    print(f'Descifrado con CBC: {aes128_cbc_dec(llave, cbc_cifrado_1, iv)}')
    print(f'Descifrado con CTR: {aes128_ctr_dec(llave, ctr_cifrado_1, iv)}\n')

    print('>>>> Mensaje 2:\n')
    print(f'Cifrado con CBC: {cbc_cifrado_2}')
    print(f'Cifrado con CTR: {ctr_cifrado_2}')
    print(f'Descifrado con CBC: {aes128_cbc_dec(llave, cbc_cifrado_2, iv)}')
    print(f'Descifrado con CTR: {aes128_ctr_dec(llave, ctr_cifrado_2, iv)}')
