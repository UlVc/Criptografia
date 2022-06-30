def main():
    texto_cifrado = bytearray()
    llave = bytearray()
    res = bytearray() # Bytes de la imagen a formar.
    contador = 0 # Auxiliar para iterar en los bytes de la llave obtenida.

    # Primeros 8 bytes de un archivo PNG. 
    # Siempre son los mismos para todos los archivos PNG.
    mensaje_claro = bytearray([137, 80, 78, 71, 13, 10, 26, 10])
    
    with open('./ocho.vigenere', 'rb') as archivo:
        texto_cifrado = bytearray(archivo.read())
    
    # Hacemos XOR con los primeros 8 bits del texto cifrado y el claro.
    for i in range(0, 8):
        llave.append(mensaje_claro[i] ^ texto_cifrado[i])

    # Hacemos XOR byte a byte con la llave y los bytes de ocho.vigenere.
    for x in texto_cifrado:
        res.append(x ^ llave[contador])
        contador = (contador + 1) % 8

    with open('./8-vigenere.png', 'wb') as archivo:
        archivo.write(res)

if __name__ == '__main__':
    main()
