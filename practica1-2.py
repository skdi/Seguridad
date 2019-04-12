# -*- coding: utf-8 -*-
import six
def func1():
	f = open("poema.txt")
	g = open("poema2.txt","w")

	for linea in f:
		for x in linea:
			if(x=="j"):
				x="i"
			if(x=="h"):
				x="i"
			if(x=="ñ"):
				x="n"
			if(x=="k"):
				x="l"
			if(x=="u"):
				x="v"
			if(x=="w"):
				x="v"
			if(x=="y"):
				x="z"
			g.write(x)

	g.close()
	f.close()


def func2():
	f = open("poema.txt")
	g = open("poema2.txt","w")

	for linea in f:
		for x in linea:
			if(x=="á"):
				x="a"
			if(x=="é"):
				x="e"
			if(x=="í"):
				x="i"
			if(x=="ó"):
				x="o"
			if(x=="ú"):
				x="u"
			g.write(x)

	g.close()
	f.close()


def func3():
	f = open("poema.txt")
	g = open("poema2.txt","w")
	for linea in f:
		for x in linea:
			z = ord(x)
			if(z>=97 and z<=122):
				z-=32
			x = str(chr(z))
			g.write(x)


	g.close()
	f.close()



def func4():
	f = open("poema.txt",encoding="utf8")
	g = open("poema20_pre.txt","w")
	for linea in f:
		for x in linea:
			if(x==" " or x=="." or x=="," or x=="“" or x==":"):
				x=""
			g.write(x)

	g.close()
	f.close()

def frecuencias(archivo):
	f = open(archivo+".txt",encoding="utf8")
	c=[]
	alfabeto_size=26
	for i in range(alfabeto_size):
	    c.append([])
	    for j in range(2):
	        c[i].append(None)

	for i in range(alfabeto_size):
		c[i][0]=str(chr(i+65))
		c[i][1]=0

	for linea in f:
		for x in linea:
			z=ord(x)
			if(z!=10):#si z no es salto de linea
				z=z-65
				if(z>=0 and z<=alfabeto_size):
					c[z][1]+=1

	c.sort(key=lambda frecuencia: frecuencia[1],reverse=True)

	for i in range(alfabeto_size):
		print(c[i])
	print("caracteres mas frecuentes: ")
	for i in range(5):
		print(c[i])
	f.close()


def kasiski(archivo):
	f = open(archivo+".txt",encoding="utf8")
	c=[]
	cont=ini=fin=dist=0
	triada=3
	for linea in f:
		for i in range(0,len(linea),triada):
			tri=linea[i:triada+i]
			ini=i+triada

			for j in range(i,len(linea),triada):
				auxtri=linea[j:triada+j]
				if(tri==auxtri):
					dist=(j-ini)
					if(dist==-triada):
						dist=0
					c.append([])
					for k in range(2):
						c[cont].append(None)
					c[cont][0]=tri
					c[cont][1]=dist
					ini=j+triada
					cont=cont+1
					dist=0
	f.close()
	for i in range(len(c)):
		if(c[i][1]!=0):
			print(c[i])



def sustituir_aqui(archivo):
	f = open(archivo+".txt",encoding="utf8")
	g = open("poema20_pre2.txt","w")
	cont=aux=0
	for linea in f:
		for j in linea:
			cont=cont+1
			aux=aux+1
			if(cont==21):
				cont=1
				aux=aux+4
				g.write("AQUI")
				g.write(j)
			else:
				g.write(j)
	aux=aux%4
	if(aux!=0):
		g.write("X"*aux)
	g.close()
	f.close()

"""
def unicode8(archivo):
	f = open(archivo+".txt",encoding="utf8")
	g = open("poema20_pre2.txt","w")
	for linea in f:
		linea=linea.unidecode(linea.decode("utf-8"))
		g.write(linea)


	g.close()
	f.close()

unicode8("poema")
"""

aqui("poema")
