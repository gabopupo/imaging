#
#	GABRIEL ROMUALDO SILVEIRA PUPO 9896250
#	SCC0251 - 2018/1
#	TRABALHO 1 - GERADOR DE IMAGENS
#

import numpy as np
import imageio as iio
import random as rnd

def randomwalk(scene, d):
	x, y = 0, 0
	for i in range(1 + (d*d)//2):
		scene[x,y] = 1.0
		dx = rnd.randint(-1, 1)						# gera um inteiro aleatorio entre [-1, 1]
		dy = rnd.randint(-1, 1)
		x, y = (x + dx) % d, (y + dy) % d				# colore um pixel baseando-se nas variacoes horiz. e vert.

def scene_gen(c, func, q):
	scene = np.zeros(shape=(c,c))					 	# cria uma matriz vazia para a cena
	if func == 5:
		randomwalk(scene, c)
	else:
		for x in range(c):
			for y in range(c):
				if func == 1:
					scene[x,y] = x+y
				elif func == 2:
					scene[x,y] = np.abs(np.sin(x/q)+np.sin(y/q))
				elif func == 3:
					scene[x,y] = (x/q)-np.sqrt(y/q)
				elif func == 4:
					scene[x,y] = rnd.uniform(0, 1)
	scene *= 65535 / (scene.max() * 1.0) 					# normaliza matriz da imagem cena [0, 65535]
	return np.absolute(scene)						# retorna-a com seus valores absolutos para impedir pixels negativos

def digitalize(n, scene, c, b):
	digital = np.zeros(shape=(n,n))						# cria uma matriz vazia para a img digital
	d = c//n								# dimensoes das submatrizes usadas na operacao max
	for i in range(n):
		for j in range(n):
			digital[i,j] = scene[i*d:(i*d)+d,j*d:(j*d)+d].max()	# obtem o maximo local de uma porcao da cena e insere na img digital
	digital *= 255 / (digital.max() * 1.0)					# normaliza matriz da imagem digital [0, 255] para caber em 8 bits
	digital = np.bitwise_and(digital.astype(np.uint8), 256-(2**(8-b)))	# fixa os B bits mais significativos em cada pixel da img digital
	return np.right_shift(digital, 8-b)					# shifta os bits de cada pixel para direita para caber no limite definido por B

def rmse(g, r):
	return np.sqrt(((g-r)**2).mean())					# calcula a raiz do erro medio quadratico

def main():
	sc_dim = int(input("Dimensões da imagem cena: "))							# dimensoes da imagem da cena
	func = int(input("Função:\n1. (x+y)\n2. |sen(x/Q)+sin(y/Q)|\n3. [(x/Q)-sqrt(y/Q)]\n4. rand(0,1,S)\n5. randomwalk(S)\nR: ")) # funcao a ser usada
	q = float(input("Q = ")) 							# parametro Q constante
	dg_dim = int(input("Dimensões da imagem digital: "))							# dimensoes da imagem digital
	bpp = int(input("Bits p/ pixel: "))							# bits por pixel para a quantizacao
	seed = int(input("Semente para randomização: "))							# semente para funcoes random

	rnd.seed(seed)								# define a semente
	scene = scene_gen(sc_dim, func, q)					# gera a cena
	digital = digitalize(dg_dim, scene, sc_dim, bpp)			# gera a imagem digital
	iio.imwrite("out.png", digital)

if __name__ == "__main__":
	main()
