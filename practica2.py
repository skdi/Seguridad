# -*- coding: utf-8 -*-
import six
import numpy as np


"""
*****Practica 2******
"""

def vignere_cifrado(archivo,clave):
	f = open(archivo,encoding="utf8")
	g = open("cifrado.txt","w")
	j=0
	c=""
	abc="ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
	alfabeto_size=len(abc)
	for linea in f:
		for i in linea:
			m=abc.find(i)
			k=abc.find(clave[j])
			ci=(m+k)%alfabeto_size
			g.write(abc[ci])
			if(j<len(clave)-1):
				j+=1
			else:
				j=0


	g.close()
	f.close()


def vignere_descifrado(archivo,clave):
	f = open(archivo,encoding="utf8")
	g = open("descifrado.txt","w")
	j=0
	c=""
	abc="ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
	alfabeto_size=len(abc)
	for linea in f:
		for i in linea:
			c=abc.find(i)
			k=abc.find(clave[j])
			mi=(c+(alfabeto_size-k))%alfabeto_size
			g.write(abc[mi])
			
			if(j<len(clave)-1):
				j+=1
			else:
				j=0


	g.close()
	f.close()



vignere_descifrado("cifrado.txt","SABIDURIA")