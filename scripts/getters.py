def getCodCurso():
	# retorna o codigo dos cursos superiores do IFNMG campus Januária.
	file = open('../dados de entrada/DM_LOCAL_OFERTA.CSV','r',encoding='ISO-8859-1')
	codigo_curso = []
	cod_januaria = '3135209'
	for row in file:
		column = row.split('|')
		if 'Campus Januária' in column[2] and column[5] == cod_januaria:
			codigo_curso.append(column[9])
	file.close()
	return codigo_curso
'''
id | descrição
2 	 NO_LOCAL_OFERTA == Campus Januária
5    CO_MUNICIPIO
9    CO_CURSO
co municipal de januária = 3135209

'''

def getMatriculas(cod_cursos, ano):
	# cria um arquivo csv com as matriculas de todos os cursos superiores do IFNMG campus Januária.
	file = open('../dados de entrada/DM_ALUNO.CSV','r',encoding='ISO-8859-1')
	out = open(f'../dados/matriculas_januaria{ano}.csv','w')
	cont = 0
	add = 0
	for row in file:
		column = row.split('|')
		# o codigo de cada curso e unico e se mantem o mesmo em todos os
		# anos então podemos selecionar as matriculas pela variavel CO_CURSO.
		if column[6] in cod_cursos or cont == 0: # cont == 0  para escreve o cabeçalho.
			out.write(row)
			add += 1
		print(f'{cont} processados *** {add} adicionados')
		cont += 1
	file.close()
	out.close()
'''
Obs: a posição dos indices e nomes das vareaveis nos arquivos podem variar 
de acordo com o ano.
id  |  descrição
4      CO_CURSO

O id pode variar entre 4 ou 6.
'''


def getNomeCurso(cod_cursos):
	file = open('../dados de entrada/DM_CURSO.CSV','r',encoding='ISO-8859-1')
	for row in file:
		column = row.split('|')
		if column[8] in cod_cursos:
			print(f"{column[9]}|{column[8]}")
	file.close()




'''
NU_ANO_CENSO, CO_CURSO, TP_GRAU_ACADEMICO, TP_COR_RACA, TP_SEXO, NU_ANO_NASCIMENTO,
NU_MES_NASCIMENTO, NU_DIA_NASCIMENTO, NU_IDADE, CO_MUNICIPIO_NASCIMENTO, IN_DEFICIENCIA,
TP_SITUACAO, IN_RESERVA_VAGAS, NU_ANO_INGRESSO

'''