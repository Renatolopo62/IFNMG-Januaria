import pandas as pd
import verificacoes as verifica

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
*Váriaveis que serão selecionadas

NU_ANO_CENSO, CO_CURSO, TP_GRAU_ACADEMICO, TP_COR_RACA, TP_SEXO, NU_ANO_NASCIMENTO,
NU_MES_NASCIMENTO, NU_DIA_NASCIMENTO, NU_IDADE, CO_MUNICIPIO_NASCIMENTO, IN_DEFICIENCIA,
TP_SITUACAO, IN_RESERVA_VAGAS, NU_ANO_INGRESSO

'''
LIST_COLUMNS = [
	'NU_ANO_CENSO', 
	'CO_CURSO', 
	'TP_GRAU_ACADEMICO', 'CO_GRAU_ACADEMICO',
	'TP_COR_RACA', 'CO_COR_RACA_ALUNO',
	'TP_SEXO', 'IN_SEXO_ALUNO',
	'NU_ANO_NASCIMENTO', 'NU_ANO_ALUNO_NASC',
	'NU_MES_NASCIMENTO', 'NU_MES_ALUNO_NASC',
	'NU_DIA_NASCIMENTO', 'NU_DIA_ALUNO_NASC',
	'NU_IDADE', 'NU_IDADE_ALUNO',
	'CO_MUNICIPIO_NASCIMENTO', 
	'IN_DEFICIENCIA', 'TP_DEFICIENCIA', 'IN_ALUNO_DEF_TGD_SUPER', 'IN_ALUNO_DEFICIENCIA',
	'TP_SITUACAO', 'CO_ALUNO_SITUACAO',
	'IN_RESERVA_VAGAS', 
	'NU_ANO_INGRESSO', 'ANO_INGRESSO'

]
# 2009 não tem CO_MUNICIPIO_NASCIMENTO
DIC_NAME_COMUNS = {
	'NU_ANO_CENSO': ['NU_ANO_CENSO'], 
	'CO_CURSO': ['CO_CURSO'], 
	'TP_GRAU_ACADEMICO': ['TP_GRAU_ACADEMICO', 'CO_GRAU_ACADEMICO'],
	'TP_COR_RACA': ['TP_COR_RACA', 'CO_COR_RACA_ALUNO'],
	'TP_SEXO': ['TP_SEXO', 'IN_SEXO_ALUNO'],
	'NU_ANO_NASCIMENTO': ['NU_ANO_NASCIMENTO', 'NU_ANO_ALUNO_NASC'],
	'NU_MES_NASCIMENTO': ['NU_MES_NASCIMENTO', 'NU_MES_ALUNO_NASC'],
	'NU_DIA_NASCIMENTO': ['NU_DIA_NASCIMENTO', 'NU_DIA_ALUNO_NASC'],
	'NU_IDADE': ['NU_IDADE', 'NU_IDADE_ALUNO'],
	'CO_MUNICIPIO_NASCIMENTO': ['CO_MUNICIPIO_NASCIMENTO'], 
	'IN_DEFICIENCIA': ['IN_DEFICIENCIA', 'TP_DEFICIENCIA', 'IN_ALUNO_DEF_TGD_SUPER', 'IN_ALUNO_DEFICIENCIA'],
	'TP_SITUACAO': ['TP_SITUACAO', 'CO_ALUNO_SITUACAO'],
	'IN_RESERVA_VAGAS': ['IN_RESERVA_VAGAS'], 
	'NU_ANO_INGRESSO': ['NU_ANO_INGRESSO', 'ANO_INGRESSO']
}

def getDicRename(columns):
	# retorna um dicionário com os novos nomes das colunas (ex: {novo nome: antigo nome})
	dic_rename = {}
	for col in columns:
		for i in DIC_NAME_COMUNS:
			if col in DIC_NAME_COMUNS[i]:
				dic_rename[i] = col
				break

	return dic_rename


def getDf(ano):
	df = pd.read_csv(f'../dados/matriculas_januaria{ano}.csv','r', delimiter='|')   

	# seleciona somente as colunas que estão em LIST_COLUMNS
	columns = list(df.columns)
	columns_drop = [x for x in columns if x not in LIST_COLUMNS]
	df = df.drop(columns = columns_drop)

	# adiciona novas colunas caso ela não exista, para que os df ficarem com o
	# mesmo número de colunas.
	if ano != 2017 and ano != 2018:
		df['NU_ANO_CENSO'] = ano
	if ano == 2009:
		df['CO_MUNICIPIO_NASCIMENTO'] = 'null'

	# renomeia as colunas, elas devem ter os mesmos nomes em todos os data frames
	# para poder usar a função concat.
	dic = getDicRename(list(df.columns))
	df.columns = [x for x in dic]

	return df



def getId(df):
	# remover 2009 por não ter CO_MUNICIPIO_NASCIMENTO
	df = df[df['NU_ANO_CENSO'] != 2009]

	df1 = df.applymap(str)
	df1['Id']  = df1[['TP_COR_RACA', 
	                 'TP_SEXO', 
	                 'NU_ANO_NASCIMENTO',
	                 'NU_MES_NASCIMENTO',
	                 'NU_DIA_NASCIMENTO',
	                 'CO_MUNICIPIO_NASCIMENTO']].agg(''.join, axis=1) 

	# remove os id que se repetem              
	repetidos = verifica.repetidos(df1)
	for i in repetidos:
		df1 = df1[df1['Id'] != i]
	df1.to_csv('../dados/dados_padronizados_matriculas_januaria_2010_2018_com_id.csv', index=False)
	
	return df1

# cria a coluna NOME_CURSO
def get_nome_curso(df):
	nome_curso = {
		'96981': 'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
		'99503': 'MATEMÁTICA',
		'107474': 'ADMINISTRAÇÃO',
		'107476': 'AGRONOMIA',
		'112692': 'FÍSICA',
		'1102801': 'CIÊNCIAS BIOLÓGICAS',
		'1102802': 'ENGENHARIA AGRÍCOLA E AMBIENTAL',
		'1376268': 'ENGENHARIA CIVIL',
		'1421026': 'SISTEMAS DE INFORMAÇÃO'
	}

	df['NOME_CURSO'] = '--'
	for index, row in df.iterrows():
		df.loc[index, 'NOME_CURSO'] = nome_curso[str(row['CO_CURSO'])]

	return df




def getDadosPadronizados():
	list_df = []
	for ano in range(2009,2019):
		df = getDf(ano)
		list_df.append(df)

	# concatena todos os df da list_df em um só.
	df_concat = pd.concat(list_df)

	# padroniza a coluna TP_SEXO
	# >= 2017 1. Feminino 2. Masculino        
	# <= 2016 0. masculino 1. feminino  
	df_concat.loc[df_concat.TP_SEXO == 2, 'TP_SEXO'] = 0

	# add nome dos cursos
	df_concat = get_nome_curso(df_concat)

	# salva o df sem id
	df_concat.to_csv('../dados/dados_padronizados_matriculas_januaria_2009_2018.csv', index=False)

	# cria um id para cada matricula
	df_concat = getId(df_concat)
	print(df_concat)

