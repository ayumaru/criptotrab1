import numpy as np
import cv2
import os

"""
ord > e a funcao que vai pegar o codigo unicode da letra representada por i
format > e a funcao responsavel por pegar o decimal que representa a letra e transforma pra binario 8bits
"""

def convert_bin(texto):

    if type(texto) == str:
        temp = ''
        for i in texto:
            temp += format(ord(i), "08b")
        return temp     
 
    elif type(texto) == bytes or type(texto) == np.ndarray: #tenho impressao que o nparray eh o que vem da memoria        
        return [ format(i, "08b") for i in texto ] 

    elif type(texto) == int or type(texto) == np.uint8:
        return format(message, "08b")  
    
    else:
        print("Mensagem nao suportada")
        raise


"""
A tecnica vai ser LSB aproveitando os 3 canais do rgb
Na teoria podemos esconder textos de ate N bytes dentro de uma imagem com dimensao  m*n
usando sistema de canal rgb, então temos 3 canais com cada pixel contendo 8 bits cada canal = 24 bits no total -> 3 bytes
Entao algebricamente podemos representar mais ou menos como:
( altura x largura ) * piso(3/8)
posicao do canal dentro do pixel [r = 0, g = 1 , b = 2]
"""
def inserir_texto_img(img, txt):
    
    nb =((img.shape[0] * img.shape[1])* 3)//8
    print("Tamanho da imagem inserida: ", img.shape[0] ,"x" ,img.shape[1], "\n")
    print("Maximo de caracteres possiveis no texto: ", nb, "\n") 
    print("Seu texto possui: ", len(txt), " caracteres.\n")

    txt += "@!@!@" # @ > delimitador do texto
    if len(txt) > nb:
        print("Quantidade maxima de caracteres excedida, o programa sera finalizado")
        raise
    
    bin_txt = convert_bin(txt)
    #controle da insercao dos dados na imagem
    index = 0
    tam_bin = len(bin_txt) 
    for posicao in img:
        for pixel in posicao: 
            
            r,g,b = convert_bin(pixel)

            if index < tam_bin:
                pixel[0] = int( r[:-1] + bin_txt[index], 2 ) 
                index += 1
            if index < tam_bin:
                pixel[1] = int(g[:-1] + bin_txt[index], 2)            
                index += 1
            if index < tam_bin:
                pixel[2] = int(b[:-1] + bin_txt[index], 2)
                index += 1
            if index >= tam_bin: break

    return img

def retirar_texto(img):

    bin_txt = ""
    for posicao in img:
        for pixel in posicao:
            r,g,b = convert_bin(pixel)
            bin_txt += r[-1] + g[-1] + b[-1] 
    
    
    palavra_byte = [ bin_txt[i:i+8] for i in range(0, len(bin_txt), 8) ]
    palavra_txt = ""

    for b in palavra_byte:
        palavra_txt += chr(int(b,2)) #transforma pra decimal 

        if palavra_txt[-5:] == "@!@!@": #delimitador definido na hora de esconder o texto
            break
    
    return palavra_txt[:-5]

def carregar_img():
    nome_img = input()
    return cv2.imread(nome_img), nome_img

def ler_texto():
    print("Insira o caminho ate o arquivo texto que deseja esconder: ")
    nome_txt = input()
    f = open(nome_txt, "r", encoding='utf8')
    
    texto = ''
    for c in f:
        texto += c

    final = ""
    temp = texto.split()
    final = ' '.join([str(x) for x in temp]) 
    
    f.close()
    return final

def main():
    print("Esteganografia de texto em imagem. O que deseja fazer? \n")
    print("1 -> Esconder texto em imagem. \n")
    print("2 -> Recuperar texto de uma imagem. \n")
    op = input()
    op = int(op)
    if op == 1:
        print("Insira o caminho ate a imagem com o seu formato: \n")
        imagem, nome_img = carregar_img()

        if imagem is None: 
            print("Imagem invalida ou nao encontrada. Finalizando o programa\n")
            return 

        print("Insira o nome para a imagem que vai possuir um texto escondido com formato .png: \n")
        temp = True
        while temp:
            
            nome_img_res = input()
            if nome_img_res[-4:] != ".png":
                print("Formato invalido, insira novamente ou aborte o programa. \n")
            else:
                temp = False

        
        texto = ler_texto()
        if len(texto) == 0:
            print("Nenhum caracter inserido. Finalizando o programa. \n")

        nova_imagem = inserir_texto_img(imagem, texto)
        cv2.imwrite(nome_img_res, nova_imagem)
        #"{:.5f}".format / (1024*1024)
        fi = os.stat(nome_img_res)
        print("Tamanho da nova imagem:", ( fi.st_size ), "Bytes")
        fi = os.stat(nome_img)
        print("Tamanho da original: ", ( fi.st_size ), " Bytes")
       

    elif op == 2:
        print("Insira o caminho ate a imagem com o seu formato: \n") ## tranformar isso em uma funcao de leitura de imagem
        imagem, nome_img = carregar_img()
       
        if imagem is None:
            print("Imagem invalida ou nao encontrada. Finalizando o programa\n")
            return
        
        print("O texto recuperado foi: \n")
        print(retirar_texto(imagem)) 
           
    else:
        print("opcao nao suportada \n")

if __name__ == "__main__":
    main()