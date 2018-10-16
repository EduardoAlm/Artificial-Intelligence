import copy
import random
import sys

# ------------------------------------------------------------------
def aux_print (elem):
	if elem == 0:
		return " . "
	if elem == 1:
		return " X "
	if elem == -1:
		return " O "

def mostra_tabuleiro(T):
	for x in range (0,(9)):
		if (x == 3 or x == 6):
			print ("\n")
		print (aux_print (T[x]), end = ""),
	print ("\n")
		
# ------------------------------------------------------------------
# devolve a lista de ações que se podem executar partido de um estado
def acoes(T):
	lista=[]
	for i in range (0,(9)):
		if T[i]==0:
			lista.append(i)
	
	return lista

# ------------------------------------------------------------------
# devolve o estado que resulta de partir de um estado e executar uma ação
def resultado(T,a,jog):
	aux = copy.copy(T)
	if aux[a]==0:
		if jog == 'MAX':
			aux[a]=1
		else:
			aux[a]=-1
	
	return aux

# ------------------------------------------------------------------
# existem 8 possíveis alinhamentos vencedores, para cada jogador
def utilidade(T):
		# testa as linhas
	for i in (0,3,6):
		if (T[i] == T[i+1] == T[i+2]):
			if (T[i] == 1):
				return 1
			elif (T[i] == -1):
				return -1
	#testa colunas
	for i in (0,1,2):
		if (T[i] == T[i+3] == T[i+6]):
			if (T[i] == 1):
				return 1
			elif (T[i] == -1):
				return -1
	#testa diagonais
	if (T[0] == T[4] == T[8]):
		if (T[0] == 1):
			return 1
		elif (T[0] == -1):
			return -1
	if (T[2] == T[4] == T[6]):
		if (T[2] == 1):
			return 1
		elif (T[2] == -1):
			return -1
	# não é nodo folha ou dá empate
	return 0
# ------------------------------------------------------------------
# devolve True se T é terminal, senão devolve False
def estado_terminal(T):
	x = utilidade(T)
	if (x == 0):
		for x in range (0,9):
			if (T[x] == 0):
				return (False)
	
	return (True)


# ------------------------------------------------------------------
# algoritmo da wikipedia
# https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
# ignoramos a profundidade e devolvemos o valor, a ação e o estado resultante
def alfabeta(T,alfa,beta,jog):
	if estado_terminal(T):
		return utilidade(T),-1,-1
	if jog:
		v = -10
		ba=-1
		for a in acoes(T):
			v1,ac,es = alfabeta(resultado(T,a,'MAX'),alfa,beta,False)
			if v1 > v: # guardo a ação que corresponde ao melhor
				v = v1
				ba=a
			alfa = max(alfa,v)
			if beta <= alfa:
				break
		return v,ba,resultado(T,ba,'MAX')
	else:
		# COMPLETAR
		v = 10
		ba= -1
		for a in acoes(T):
			v1,ac,es = alfabeta(resultado(T,a,'MIN'),alfa,beta,True)
			if v1 < v: # guardo a ação que corresponde ao melhor
				v = v1
				ba=a
			alfa = min(alfa,v)
			if beta <= alfa :
				break
		return v,ba,resultado(T,ba,'MIN')

# ------------------------------------------------------------------
def joga_max(T):
	v,a,e = alfabeta(T,-10,10,True)
	print ('MAX joga para '),a
	return e

# ------------------------------------------------------------------
def joga_min(T):
	v,a,e = alfabeta(T,-10,10,False)
	print ('MIN joga para '),a
	return e

# ------------------------------------------------------------------
def jogo(p1,p2):
	# cria tabuleiro vazio
	T = [0,0,0,0,0,0,0,0,0]
	mostra_tabuleiro(T)
	while acoes(T) != [] and not estado_terminal(T):
		T=p1(T)
		mostra_tabuleiro(T)
		if acoes(T) != [] and not estado_terminal(T):
			T=p2(T)
			mostra_tabuleiro(T)
	# fim
	if utilidade(T) == 1:
		print ('Venceu o jogador 1')
	elif utilidade(T) == -1:
		print ('Venceu o jogador 2')
	else:
		print ('Empate')

# ------------------------------------------------------------------
# jogador aleatório
def joga_rand(T):
	x = random.randint(0,8)
	i = True
	while i:
		if (T[x] == 0):
			T=resultado(T,x,'MIN')
			i = False
		else:
			x = random.randint(0,8)

	print ('RAND joga para '),x
	return T

# ------------------------------------------------------------------
#---------Jogador humano
def joga_utilizador(T):
	print ("Introduza a posicao para que quer jogar:")
	posicao = int(input("—> "))
	disponiveis = acoes(T)
	while posicao not in disponiveis:
		posicao = int(input("—> "))
	
	T = resultado(T, posicao, 'MIN')
	print ('USER joga para '), posicao
	return T

# main

# deve ganhar sempre o max:
jogo(joga_max,joga_rand)
# devem empatar sempre:
#jogo(joga_max,joga_min)
# jogador humano vs ZI MACHINE
#jogo(joga_max, joga_utilizador)

