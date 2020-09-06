import pandas as pd

# imprime uma lista com os id que se repetem, se tiver algum.
# porém não compara o codigo do curso
def contIdRepetido(df):
	
	x = df.groupby(['NU_ANO_CENSO'])['Id'].value_counts()

	rep = [[i[0], i[1]] for i, v in x.items() if v > 1]
	for i in rep:
		print(f'{i[0]}: {i[1]}')
	print(f'Ids repetidos: {len(rep)}')


# verifica se tem matriculas repetidas
def matriculas_repetidas(df):
	df1 = df.applymap(str)
	columns = list(df.columns)
	df1['Join'] = df1[columns].agg(''.join, axis=1)

	matriculas = []
	repetidas = []
	for i in df1['Join']:
		if i in matriculas:
			repetidas.append(i)
		else:
			matriculas.append(i)
	print(f'matriculas repetidas: {repetidas}\n {len(repetidas)}')

# verifica os ids que se repetem verificando tambem os codigos do curso
# e retorna uma lista com os que se repetem 
def repetidos(df):
	repetidos = []
	vistos = set()
	for index, row in df.iterrows():
	    chave = row["Id"], row["NU_ANO_CENSO"], row["CO_CURSO"]
	    if chave not in vistos:
	        vistos.add(chave)
	    else:
	        repetidos.append(row["Id"])
	print(f'id repetidos: {repetidos}')
	print(len(repetidos))
	return repetidos

