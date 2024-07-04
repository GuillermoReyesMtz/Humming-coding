# -*- coding: utf-8 -*-
import sys
import codecs
import os
import csv
import operator

#creacion del arbol de Huffman
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

    #creacion del nodo raiz principal
def huffman(directorio):
    n=len(directorio)
    Q=[]
    for i in directorio:
        #Se añaden los nuevos nodos que se forman con la etiqueta de simbolo y frecuencia
        Q.append(Nodo(directorio.get(i),i))
    for i in range(0,n-1):        
        #Se toma al nodo mas pequeño
        x=mini(Q)
        #Tambien se selecciona al segudo nodo mas pequeño
        y=mini(Q)
        z=Nodo(x.freq+y.freq,x.symbol+y.symbol)
        z.left=x
        z.right=y
        z.left.encode=0
        z.right.encode=1
        Q.append(z)
    return mini(Q)

#la funcion codificacionH() recibe por parametro el nodo inicial, el simbolo i del diccionario de caracteres y la codificacion.        
def codificacionH(raiz,i,codificacion=""):     
    if len(raiz.symbol)>1:                                          
       #verificamos si el simbolo se encuentra en el nodo izquierdo
        if i in raiz.left.symbol:
            #Introducimos el simbolo correcto a la codificacion
            codificacion+=str(raiz.left.encode) 
            #si el simbolo se encuentra en el nodo izquierdo recorremos hasta llegar y repetimos el proceso
            return codificacionH(raiz.left,i,codificacion) 
            
        else:
            #Introducimos el simbolo correcto a la codificacion
            codificacion+=str(raiz.right.encode) 
            #En caso de no encontrarlo en el nodo izquierdo podemos concluir que se encuentra en el nodo derecho, luego repetimos el proceso
            return codificacionH(raiz.right,i,codificacion) 
    return codificacion

 #---Codificaion a huffman
def GenerarArchivoCodificado(ruta_Archivo_Original,ruta_Archivo_Codificado,H):   
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
    
    #Se crea el directorio para las palabras-codigo de Hamming
    dirHam={} 
    dirHamInv={}
    dirHamInv2={}
    codeword=creating_code(H,huffman_4bits,dirHam,dirHamInv2) 
    DirHamInv_keys=list(dirHam.values())
    DirHamInv_values=list(dirHam.keys())    
    dirHamInv = dict(zip(DirHamInv_keys,DirHamInv_values))   
    
    code_Hamming=""
 
    for i in huffman_4bits:
        code=dirHam[i]
        code_Hamming=code_Hamming+code       
    
    file = open(ruta_Archivo_Codificado, "w")       
    file.write(code_Hamming)
    file.close()
    archivo.close
    
    return dirHamInv,raiz,aux
    
#-----Creacion del codigo Hamming    
# Funcion que crea las palabras codigo
def creating_code_word(H, bit_string):
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


#Funcion que determina los bits de paridad
def dividir4bits(valor_binario):
    power_set=[]
    valor=""
    for i in range(0,len(valor_binario)):
        valor=valor+valor_binario[i]
        if len(valor) == 4:
            power_set.append(valor)
            valor=""
    return power_set

#funcion que crea un diccionario para el codigo de Hamming
def creating_code(H,power_set,dirHam,dirHamInv): 
    r = len(H)
    code = []
    imparopar=1
    for word in range(0,len(power_set),1):         
        codeword=creating_code_word(H, power_set[word])        
        value=codeword
        (valido,vector_res)=verificador(value,H)
        if max(vector_res)==1:
            print(vector_res)  
        codeword=value
        aux_word=power_set[word]     
        
        dirHam[aux_word]=codeword
        dirHamInv[codeword]=aux_word        
           
        code.append(codeword)
    #Este es el conjunto de 8bits
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

#Lista de listas generada despues de multiplicar H1
def columnaerror (Vector,H): 
    ilist=[]
    for j in range (0, len(Vector)):
        for i in range (0, len(H[0])):
            columna= []
            columna = [fila[i] for fila in H]
            if Vector[j]==columna:                
                return i                
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

            #Se convierte la cadena en una lista de enteros
            code_word_aux=[int(x) for x in i] 
            code_coregido=corregir_bit(bit_incorrecto,code_word_aux)
            resultado+=code_coregido                        
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

#Se pasa por parametro la codificacion de una palabra y la raiz principal del arbol con la que se codifico
def huffman_Inv(raiz,codeH): 
    c=""
    #Contador que indica la posicion en la cadena; La posicion cero no es parte del ciclo
    i=1 
    #La raiz se almacena en una variable temporal
    raiz_aux=raiz 
    #Si nuestro primer simbolo de la codificacion se encuentra del lado izquierdo, recorremos el arbol hacia el nodo izquierdo
    if raiz_aux.left.encode==int(codeH[0]): 
        raiz_aux=raiz_aux.left 
        
        #El proceso continua hasta llegar al final de la cadena
        while(i < len(codeH)): 
            #Se recorre todo el arbol hasta un nodo hoja que coincide con la codificacion codeH, los parametros c_aux, raiz_aux e i corresponden a: el simbolo de la hoja, el nodo de la hoja y la posicion siguiente respectivamente            
            (c_aux,raiz_aux,i)=v2(raiz_aux,codeH,i)  
            raiz_aux=raiz
            #Se suman los simbolos de las hojas visitadas para formar la cadena
            c+=c_aux 
        if len(codeH)==1:
            (c_aux,raiz_aux,i)=v2(raiz_aux,codeH,i)
            raiz_aux=raiz
            c+=c_aux        
    else:
        raiz_aux=raiz_aux.right
        while(i < len(codeH)):            
            (c_aux,raiz_aux,i)=v2(raiz_aux,codeH,i)
            raiz_aux=raiz
            c+=c_aux    
        if len(codeH)==1:
            (c_aux,raiz_aux,i)=v2(raiz_aux,codeH,i)
            raiz_aux=raiz
            c+=c_aux       
    return c

#En esta funcion se recibe por parametro un nodo y la codificacion de Huffman de un simbolo, esto nos permite dirigirnos al siguiente nodo basandonos en la codificacion
def v(raiz,codeH,i): 
                                                                                   
    if raiz.left.encode == int(codeH[i]):
        raiz=raiz.left
        #i es un contador que nos indica en que posision nos encontramos
        i=i+1 
    else:        
        raiz=raiz.right
        i=i+1    
    return raiz,i

#Esta funcion trabaja en conjunto con la funcion v, de modo que se recorre el arbol hasta su respectiva hoja    
def v2(raiz_aux,codeH,i): 
    c=""
    #El ciclo seguira repitiendose mientras no estemos en un nodo hoja
    while len(raiz_aux.symbol) > 1:         
        (raiz_aux,i)=v(raiz_aux,codeH,i)
    #Aqui se obtiene el simbolo de la hoja a la que se llego
    c+=raiz_aux.symbol
    #Retornamos el simbolo de la hoja final, el nodo al que corresponde, y en que elemento de la codificacion nos encontramos
    return c,raiz_aux,i 
    
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
#Matriz de 4x8
H =  [[1, 0, 0, 0, 1, 1, 1, 0], 
      [0, 1, 0, 0, 0, 1, 1, 1], 
      [0, 0, 1, 0, 1, 1, 1, 0], 
      [0, 0, 0, 1, 0, 0, 1, 1]]

#Ruta del archivo original
ruta='C:/Users/user/Desktop/textos/archivo.txt'

ruta_Archivo_Original=ruta         
#Ruta en donde se escribira el archivo de codificacion                           
ruta_Archivo_Codificado='C:/Users/user/Desktop/codificacion.txt'                             
ruta_Archivo_a_corregir=ruta_Archivo_Codificado       
#Ruta donde se escribira el archivo decodificado                                       
ruta_Archivo_Decodificado='C:/Users/user/Desktop/decodificacion.txt'   


#Aqui se llama a la funcion que creara el archivo codificado
(dirHamInv,raiz,restoHam)=GenerarArchivoCodificado(ruta_Archivo_Original,ruta_Archivo_Codificado,H) 

#Aqui se llama a la funcion para la correccion de errores
archivo_corregido=recuperar_Archivo(ruta_Archivo_a_corregir,H)

#Aqui se llama a la funcion para crear el archivo corregido
decodificar(archivo_corregido,restoHam,dirHamInv,raiz,ruta_Archivo_Decodificado) 

                      
