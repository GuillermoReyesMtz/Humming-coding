# -*- coding: utf-8 -*-
import sys
import codecs
import os
import csv
import operator

class Nodo:

    def __init__(self,dato,symbol):
        self.freq=dato
        self.symbol=symbol
        self.left=None
        self.right=None
        self.encode=None
        self.visit=False

def insertar(raiz,nodo):
    if raiz is None:
        raiz=nodo
    else:
        if raiz.freq < nodo.freq:
            if raiz.right is None:
                raiz.right=nodo
            else:
                insertar(raiz.right,nodo)
        else:
            if raiz.left is None:
                raiz.left=nodo
            else:
                insertar(raiz.left,nodo)

def mini(Q):
    minimo=Nodo(999999,'None')
    eliminar=0
    for i in range(0,len(Q)):
        if Q[i].freq < minimo.freq:
            minimo= Q[i]
            eliminar=i
    Q.pop(eliminar)
    return minimo

    
def huffman(directorio):
    n=len(directorio)
    Q=[]
    for i in directorio:
        Q.append(Nodo(directorio.get(i),i))
    for i in range(0,n-1):
        x=mini(Q)
        y=mini(Q)
        z=Nodo(x.freq+y.freq,x.symbol+y.symbol)
        z.left=x
        z.right=y
        z.left.encode=0
        z.right.encode=1
        Q.append(z)
    return mini(Q)
        
def codificacionH(raiz,i,codificacion=""):
    if len(raiz.symbol)>1:                                          #y cadena vacía codificacion que será la codificacion
        #print("el símbolo en nodo izq es ",repr(raiz.left.symbol), "y en el derecho", repr(raiz.right.symbol))
        if i in raiz.left.symbol:#checamos si nuestro simbolo está en el nodo izquierdo
            codificacion+=str(raiz.left.encode) #meto el símbolo adecuado a la codificación
            return codificacionH(raiz.left,i,codificacion) #si sí está vamos a ese nodo y repetimos
            
        else:
            codificacion+=str(raiz.right.encode) #meto el símbolo adecuado a la codificación
            return codificacionH(raiz.right,i,codificacion) #si no estuvo en el izq. está en el derecho y repetimos
    #print("codificación final: ", codificacion)
    return codificacion

def GenerarArchivoCodificado(ruta_Archivo_Original,ruta_Archivo_Codificado,H):
    #---Codificaion a huffman
    archivo=codecs.open(ruta_Archivo_Original,encoding='utf-8')
    linea1 = archivo.read().replace("\n", " ")
    directorio = {}
    for i in linea1:
        if i in directorio:
            directorio[i]+=1
        else:
            directorio[i]=1
    raiz=huffman(directorio)
                        
    caracteres=[]
    for i in directorio:
        caracteres.append(i)
    
    dirFinal={}
    for i in caracteres:
        #print("símbolo:",repr(i))
        dirFinal[i]=codificacionH(raiz,i)

    code_Huffman=""
    linea2="algoritmo, algoritmo"
    
    for i in linea1:
        code=dirFinal[i]
        code_Huffman=code_Huffman+code
    
    aux="" 
    if len(dividir4bits(code_Huffman)*4)!=len(code_Huffman): 
        aux= code_Huffman[len(dividir4bits(code_Huffman))*4::]     
    
    huffman_4bits=dividir4bits(code_Huffman)
    
    StrA = "".join(huffman_4bits)  
    StrA=StrA+aux

    dirHam={} #directorio para las palabra-codigo (hamming)
    dirHamInv={}
    dirHamInv2={}
    codeword=creating_code(H,huffman_4bits,dirHam,dirHamInv2) #Mio
    DirHamInv_keys=list(dirHam.values())
    DirHamInv_values=list(dirHam.keys())    
    dirHamInv = dict(zip(DirHamInv_keys,DirHamInv_values))   
    
    code_Hamming=""
 
    for i in huffman_4bits:
        code=dirHam[i]
        code_Hamming=code_Hamming+code       
    
    file = open(ruta_Archivo_Codificado, "w")
    #for i in dirFinal:
        #file.write(i+","+str(dirFinal.get(i))+"\n")    
    file.write(code_Hamming)
    file.close()
    archivo.close
    
    #return dirHamInv,code_Hamming,raiz,code_Huffman,directorio,aux
    return dirHamInv,raiz,aux
    #return dirInv

def creating_code_word(H, bit_string): #Mio
    codeword = ''
    r = len(H)
    for row in H:
        counter = 0
        for i in range(r, len(row)):
            if bit_string[i - r] == '1':
                counter += int(row[i])
            else:
                continue
        codeword += str((counter % 2))
    codeword += bit_string
    
    return codeword

def dividir4bits(valor_binario):
    power_set=[]
    valor=""
    for i in range(0,len(valor_binario)):
        valor=valor+valor_binario[i]
        if len(valor) == 4:
            power_set.append(valor)
            valor=""
    return power_set

#def dividir8bits(valor_binario):
    #power_set=[]
    #valor=""
    #for i in range(0,len(valor_binario)):
        #valor=valor+valor_binario[i]
        #if len(valor) == 8:
            #power_set.append(valor)
            #valor=""
    #if len(valor)>=4:
        #valor_aux=""
        #for i in range(0,4):
            #valor_aux+=valor[i]
        #power_set.append(valor_aux)
    #return power_set

def creating_code(H,power_set,dirHam,dirHamInv): 
    r = len(H)
    code = []
    imparopar=1
    for word in range(0,len(power_set),1): #Antes 2
        #(codeword,dirHam,dirHamInv)=creating_code_word(H, word,dirHam,dirHamInv)
        codeword=creating_code_word(H, power_set[word])
        #value=fill_DirHam(codeword)
        value=codeword
        (valido,vector_res)=verificador(value,H)
        if max(vector_res)==1:
            print(vector_res)  
        codeword=value
        aux_word=power_set[word]     
        
        dirHam[aux_word]=codeword
        dirHamInv[codeword]=aux_word        
           
        code.append(codeword)
    return code

def verificador(code,H):
    suma_aux=0
    suma=""
    resul=""
    res_mult=[]
    for row in H:
        for i in range(0,len(code)):
            val1=int(code[i])
            val2=int(row[i])
            suma_aux=val1*val2
            if suma_aux%2 == 0:
                resul='0'
            else:
                resul='1'
            suma+=resul
        res_mult.append(suma)
        suma=""
        
    aux=0
    vector_resultante=[]
    for i in res_mult:
        #print(i)
        for j in i:
            aux=aux+int(j)
        if aux%2 ==0:
            vector_resultante.append(0)
        else:
            vector_resultante.append(1)
        aux=0
    valido=1
    if max(vector_resultante)==1:
        valido=0
    
    return valido,vector_resultante

def corregir_bit(bit_malo,codeword):
    codewordcorregido=""
    for i in range(0,len(codeword)):
        if i == bit_malo:
            if codeword[i]==0:
                codeword[i]=1
                break
            else:
                codeword[i]=0
                break
    
    codeword_=""
    for i in codeword:
        codeword_=codeword_+str(i)
    return codeword_

def columnaerror (Vector,H): #lista de listas despues de aplicar la multiplicacion de H1\n",
    ilist=[]
    for j in range (0, len(Vector)):
        for i in range (0, len(H[0])):
            columna= []
            columna = [fila[i] for fila in H]
            if Vector[j]==columna:
                #ilist+= [i]
                return i
                #break
            elif Vector[j]== [0]*len(Vector[j]):
                ilist+= ["no hay error"]
                break
    return ilist

def recuperar_Archivo(ruta1,H):
    archivo1=codecs.open(ruta1,encoding='utf-8')
    cont_archivo_Codi = archivo1.read().replace("\n", " ")
    binario_recuperado=cont_archivo_Codi
    archivo_corregido=corregir_Archivo(binario_recuperado,H)
    
    return archivo_corregido
    
def corregir_Archivo(binario_recuperado,H):
    code_word=[]
    code=""
    for i in binario_recuperado:
        code+=i
        if len(code)==8:
            code_word.append(code)
            code=""    

    resultado=""
    for i in code_word:
        (valido,vector_res)=verificador(i,H)
        if valido==0:
            bit_incorrecto=columnaerror([vector_res],H)
            code_word_aux=[int(x) for x in i] #Convertir la cadena a una lista de enteros
            code_coregido=corregir_bit(bit_incorrecto,code_word_aux)
            resultado+=code_coregido
            #print("Bit malo:"+str(bit_incorrecto))  #Las siguiente 3 lineas de codigo te muestran los errores que se estan corrigiendo
            #print("code word malo: "+i)
            #print("code word bien: "+code_coregido)            
        else:
            resultado+=i    
            
    return resultado
    

def dividir8bits(valor_binario):
    tam_8=[]
    valor=""
    for i in range(0,len(valor_binario)):
        valor=valor+valor_binario[i]
        if len(valor) == 8:
            tam_8.append(valor)
            valor=""
       
    return tam_8

def huffman_Inv(raiz,codeH): #pide la codificación de una palabra y la raiz principal del arbol con el que codificó la palabra
    c=""
    i=1 #contador para la posición en la cadena. La posición cero se pone fuera del ciclo
    raiz_aux=raiz    #guardamos la raiz en una variable auxiliar
    if raiz_aux.left.encode==int(codeH[0]): #si yendo hacia la izquierda está nuestro primer simbolo de la codificación...
        raiz_aux=raiz_aux.left #nos movemos hacia ese nodo izquierdo

        while(i < len(codeH)): #continuamos el proceso hasta que acabamoscon la cadena
            #print("i en el while explicitamente acotado:",i,"longitud codeH", len(codeH))
            (c_aux,raiz_aux,i)=v2(raiz_aux,codeH,i) #recorremos toda el arbol hasta un nodo hoja de acuerdo a la codificacion codeH. c_aux simbolo de la hoja, raiz_aux es el nodo hoja e i es la posición que sigue en nuestra codificación codeH 
            raiz_aux=raiz #¿Para qué pedimos raiz_aux en la función anterior si la vamos a reiniciar de todas formas?
            c+=c_aux #sumamos los simbolos de las hojas a las que llegamos para formar la cadena
        if len(codeH)==1:
            (c_aux,raiz_aux,i)=v2(raiz_aux,codeH,i)
            raiz_aux=raiz
            c+=c_aux        
    else:
        raiz_aux=raiz_aux.right
        while(i < len(codeH)):
            #print("i en el while explicitamente acotado:",i,"longitud codeH", len(codeH))
            (c_aux,raiz_aux,i)=v2(raiz_aux,codeH,i)
            raiz_aux=raiz
            c+=c_aux    
        if len(codeH)==1:
            (c_aux,raiz_aux,i)=v2(raiz_aux,codeH,i)
            raiz_aux=raiz
            c+=c_aux       
    return c

def v(raiz,codeH,i): #le metodomos un nodo y la codificación de huffman de un simbolo. Nos permite pasar al siguiente nodo tomando en cuenta la codificacio
                                                                                   
    if raiz.left.encode == int(codeH[i]):
        raiz=raiz.left
        i=i+1 #este es el contador para saber en qué posición de la cadena estoy
    else:
        #print(raiz.right.freq)
        raiz=raiz.right
        i=i+1
    #print(raiz.freq)
    return raiz,i
    
def v2(raiz_aux,codeH,i): #en conjunto con v1, hace el recorrido del arbol hasta su respectiva hoja
    c=""
    while len(raiz_aux.symbol) > 1: #siempre y cuando no estemos en un nodo hoja
        #print("raiz_aux:", raiz_aux.symbol)
        (raiz_aux,i)=v(raiz_aux,codeH,i)
    c+=raiz_aux.symbol #el simbolo de la hora a la que llegamos. ¿Es necesario declarle una variable?
    #print("c:", c)
    return c,raiz_aux,i #regresa el símbolo de la hoja en donde acabamos, el nodo hoja y en qué elemento de la codificación
                                                                                           #nos quedamos
    
def decodificar(archivo_corregido,restoHam,dirHamInv,raiz,ruta_Archivo_Decodificado):    
    tam_8=dividir8bits(archivo_corregido)
    huffman_recuperado=""
    
    for i in tam_8:
        code=dirHamInv[i]
        huffman_recuperado=huffman_recuperado+code
    
    huffman_recuperado=huffman_recuperado+restoHam
    codigo_huff_inv=huffman_Inv(raiz,huffman_recuperado)
    
    file = open(ruta_Archivo_Decodificado, "w")
    file.write(codigo_huff_inv)
    file.close()

#--------------------------------------

H =  [[1, 0, 0, 0, 1, 1, 1, 0], #tamanio 8
      [0, 1, 0, 0, 0, 1, 1, 1], 
      [0, 0, 1, 0, 1, 1, 1, 0], 
      [0, 0, 0, 1, 0, 0, 1, 1]]


ruta=r'C:\Users\memo_\OneDrive - Universidad Autonoma de Yucatan\MCC\Matemáticas Discretas\Humming-coding/Alejo-Carpentier-Los-pasos-perdidos.txt'

ruta_Archivo_Original=ruta                                    
ruta_Archivo_Codificado='C:/Users/memo_/OneDrive - Universidad Autonoma de Yucatan/MCC/Matemáticas Discretas/Humming-coding/codificacion.txt'
ruta_Archivo_a_corregir = 'C:/Users/memo_/OneDrive - Universidad Autonoma de Yucatan/MCC/Matemáticas Discretas/Humming-coding/codificacion_error.txt'
ruta_Archivo_Decodificado='C:/Users/memo_/OneDrive - Universidad Autonoma de Yucatan/MCC/Matemáticas Discretas/Humming-coding/decodificacion.txt'



(dirHamInv,raiz,restoHam)=GenerarArchivoCodificado(ruta_Archivo_Original,ruta_Archivo_Codificado,H) #generar el archivo codificado

archivo_corregido=recuperar_Archivo(ruta_Archivo_a_corregir,H)  #abrir txt con codigos hammig y corregir errores

decodificar(archivo_corregido,restoHam,dirHamInv,raiz,ruta_Archivo_Decodificado) #Decodficar el archivo ya corregido

                      
