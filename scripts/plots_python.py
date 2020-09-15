import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# matriculas por ano (barra)
def plot_matriculas_por_ano(df):
	df1 = df['NU_ANO_CENSO'].value_counts()
	y = [i for i in  df1]
	x = [str(ano) for ano, v in df1.items()]
	y.reverse()
	x.reverse()

	plt.bar(x, y)
	plt.title("Matriculas por ano")
	plt.show()

# matriculas por ano e curso (line)
def plot_matriculas_por_ano_e_curso(df):
	df1 = df.groupby(['NU_ANO_CENSO'])['NOME_CURSO'].value_counts()
	ls = [[i[0], i[1], v] for i, v in df1.items()]
	df = pd.DataFrame(np.array(ls).reshape(len(ls),3), columns = ['NU_ANO_CENSO', 'NOME_CURSO', 'NUMERO_DE_MATRICULA'])
	#print(df)
	
	cursos = ['ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
		'MATEMÁTICA',
		'ADMINISTRAÇÃO',
		'AGRONOMIA',
		'FÍSICA',
		'CIÊNCIAS BIOLÓGICAS',
		'ENGENHARIA AGRÍCOLA E AMBIENTAL',
		'ENGENHARIA CIVIL',
		'SISTEMAS DE INFORMAÇÃO']


	for curso in cursos:
		x = [row['NU_ANO_CENSO'] for index, row in df.iterrows() if row['NOME_CURSO'] == curso]
		y = [row['NUMERO_DE_MATRICULA'] for index, row in df.iterrows() if row['NOME_CURSO'] == curso]
		plt.plot(x, y, label = curso, marker='o', markerfacecolor='blue',  markersize=1, linewidth=4)



	plt.xlabel('Ano do censo')
	# Set the y axis label of the current axis.
	plt.ylabel('Número de matrículas')
	# Set a title of the current axes.
	plt.title('Marículas por ano e curso')
	plt.legend()
	plt.show()


# matriculas por grau academico (pizza)

# matriculas por ano e sexo (barra)

# matricula por raça e ano (line)

# matricula alunos com deficiencia (line)

# distribuição da idade (histograma)

# situação de vinculo do aluno no curso (barra)

# número de alunos ingreço com reservas de vagas por ano (line)

# tempo de formação por curso (barra)

# numero de evasão por ano e curso (line)

# transferencia entre cursos (?)


df = pd.read_csv('../dados/dados_padronizados_matriculas_januaria_2010_2018_com_id.csv')
#plot_matriculas_por_ano(df)
plot_matriculas_por_ano_e_curso(df)

'''
Index(['CO_CURSO', 'TP_GRAU_ACADEMICO', 'TP_SITUACAO', 'IN_DEFICIENCIA',
       'IN_RESERVA_VAGAS', 'TP_SEXO', 'TP_COR_RACA', 'NU_ANO_NASCIMENTO',
       'NU_DIA_NASCIMENTO', 'NU_MES_NASCIMENTO', 'NU_IDADE', 'NU_ANO_INGRESSO',
       'NU_ANO_CENSO', 'CO_MUNICIPIO_NASCIMENTO', 'NOME_CURSO', 'Id'],
      dtype='object')



'''