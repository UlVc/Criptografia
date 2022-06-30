def main():
    mensaje_cifrado = bytearray()
                
    with open('./uno.vigenere', 'rb') as archivo:
        mensaje_cifrado = bytearray(archivo.read())
                    
    # Usamos todas las 2^8 posibles llaves y guardamos lo obtenido.
    for k in range(0, 255):
        with open(f'./vigenere-uno/mensaje_cifrado{k}.png', 'wb') as archivo:
            archivo.write(bytearray([a ^ k for a in mensaje_cifrado]))
            
if __name__ == '__main__':
    main()
