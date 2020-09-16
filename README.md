# IFNMG-Januaria
Uma análise do ensino superior do IFNMG campus januária entre os anos de 2009 e 2018 utilizando os dados do INEP.

## Etapas 
### Objetivo
O objetivo desse projeto é retirarar o máximo de informação e conhecimento possível com esses dados, posteriormente 
pretendo fazer algum artigo com os ressultados aqui obitidos para ser usado na disciplina de metodologia cientifica. 
###  Filtragem dos dados
 #### 1. Baixar os censo de Educação superior no site do INEP.
 Os arquivos do censo podem ser encontrados [aqui](http://portal.inep.gov.br/microdados). Todos os arquivos
 vem em .zip então e necessário extrair eles. 
####  2. Filtragem das matriculas que pertencem ao IFNMG - Januária. 
  A função `getCodCurso()` retorna 
  uma lista com os códigos dos cursos do IFNMG - Januária encontrados na tabela `DM_LOCAL_OFERTA`
  ```
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



  ```
  
  
  esses codigos serão usados para filtrar quais matriculas nos interessa dentre as milhares encontradas
  na tabela `DM_ALUNO`, para isso usamos a função `getMatriculas(cod_cursos, ano)`, que recebe como parametro
  a lista com os codigos dos cursos e o ano do censo. As filtragem podem demorar alguns minutos já que estamos 
  trabalhando com uma tabela que tem as matriculas de alunos do Ensino superior do Brasil todo. No final será criado 
  para cada ano um arquivo csv com as matriculas, que serão unidos em um só arquivo na proxima etapa.  
  ```
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
  ```
  
  Obs: Os arquivos `DM_LOCAL_OFERTA` e `DM_ALUNO` devem ser extraidos e passados como parametro o caminho onde ele se encontra
  de acordo com o ano.
  
#### 3. Definir quais colunas serão utilizadas e unir todas as tabelas em uma só.
  Antes de Identificar as colunas devemos definir os nossos objetivos com essa base de dados.
  ##### Objetivos:
  * Criar um ID. Apesar de nas tabelas termos a variável `ID_ALUNO` esse id não é o mesmo para todos os anos
  então e necessário criar o nosso próprio id, para isso vamos precisar das colunas `TP_COR_RACA`, `TP_SEXO`, `NU_ANO_NASCIMENTO`,
  `NU_MES_NASCIMENTO`, `NU_DIA_NASCIMENTO` e `CO_MUNICIPIO_NASCIMENTO`, como essas variáveis não vão mudar independente do ano
  podemos usar elas para criar nosso id.
  * Identificar o número de Evasão de cada ano. Pra isso vamos usar a coluna `NU_ANO_CENSO` e o id que criamos.
  * Identificar as Transferencias entre os cursos do campus e como elas estão distribuidas. Utilizaremos novamente o id para rastear o aluno
  e o `CO_CURSO`. Os cursos do IFNMG - Januária são:

  Nome do curso | Código do curso
  --- | --- 
  ANÁLISE E DESENVOLVIMENTO DE SISTEMAS|96981
  MATEMÁTICA|99503
  ADMINISTRAÇÃO|107474
  AGRONOMIA|107476
  FÍSICA|112692
  CIÊNCIAS BIOLÓGICAS|1102801
  ENGENHARIA AGRÍCOLA E AMBIENTAL|1102802
  ENGENHARIA CIVIL|1376268
  SISTEMAS DE INFORMAÇÃO|1421026

  * Contabilizar o número de matriculas por ano, curso, grau academico, sexo, raça e alunos com deficiencias. Colunas `CO_CURSO`, `TP_GRAU_ACADEMICO`, `IN_DEFICIENCIA`, `TP_COR_RACA` e `TP_SEXO`.
  * Distribuição da idade dos alunos. Coluna `NU_IDADE`.
  * Distribuição do tipo de situação de vínculo do aluno no curso. Coluna `TP_SITUACAO`.
  * Número de alunos ingreço por reserva de vagas. Coluna `IN_RESERVA_VAGAS`.
  * Distribuição de quanto tempo os alunos levam para se formar em cada curso. Coluna `NU_ANO_INGRESSO`.
  
  #### 4. Padronização dos dados e criação do id.
  Nessa etapa foi utilizada a biblioteca pandas que pode ser instalada com o comando `pip install pandas` no seu terminal e importada com `import pandas as pd`.
  No nosso script getters.py temos a função `get_dados_padronizados()` que cria dois arquivos um com os dados padronizados com o id e outro sem, 
  acho desnecessário colocar a função toda aqui então vou por só as partes que julgo necessária para o entendimento. Então vamos lá...
 
   ##### Padronizando os data frame
   Primeiro utilizamos a função `get_df(ano)` passando ano por ano como parametro, essa função retorna o nossos dfs já padronizado e adicionamos todos eles
   em uma lista.
   ```
   def get_df(ano):
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
	dic = get_dic_rename(list(df.columns))
	df.columns = [x for x in dic]

	return df
  ```
  O que a função `get_df()` faz basicamente excluir as colunas que não são interessante para nosso estudo usando a função `.drop` do pandas que recebe de 
  parametro uma lista com as colunas a serem excluidas, adiciona a coluna NU_ANO_CENSO que inicialmente só existe nos anos de 2018 e 2017, adiciona a
  coluna CO_MUNICIPIO_NASCIMENTO no ano de 2009 e renomeia as colunas de forma que todos os anos tenha as colunas com nomes semelhantes.
  
  ```
  # concatena todos os df da list_df em um só.
  df_concat = pd.concat(list_df)
  ```
  Em seguida e usada a função `concat()` para concatenar todos os dfs da nossa lista em um só, para usar a função concat e necessário que os dataframes tenham 
  o mesmo número de colunas e colunas com mesmo nome, por isso que foi feito a renomeação e adicionado novas colunas para alguns anos.
  
  ```
  # padroniza a coluna TP_SEXO
  # >= 2017 1. Feminino 2. Masculino        
  # <= 2016 0. masculino 1. feminino  
  df_concat.loc[df_concat.TP_SEXO == 2, 'TP_SEXO'] = 0

  # add nome dos cursos
  df_concat = get_nome_curso(df_concat)
  ```
  Para dar uma melhorada na nossa base de dados, padronizamos a coluna TP_SEXO que utilizava diferentes valores para identificar o sexo masculino
  dependendo do ano e adicionamos a coluna NOME_CURSO.
  
  Após feito isso salvamos um arquivo com os dados padronizados, e continuamos o processamento, agora para criar o id. Na criação do id foi necessário remover 
  as matriculas de 2009 por não ter o código do municipio de nascimento que e usado para a criação do id, e foi removidas 13 matriculas que tem informações 
  duplicadas.
  
  ```
  df1 = df.applymap(str)
  df1['Id']  = df1[['TP_COR_RACA', 
	            'TP_SEXO', 
	            'NU_ANO_NASCIMENTO',
	            'NU_MES_NASCIMENTO',
	            'NU_DIA_NASCIMENTO',
	            'CO_MUNICIPIO_NASCIMENTO']].agg(''.join, axis=1) 
  ```
  O id e criado através da junção das colunas 'TP_COR_RACA', 'TP_SEXO', 'NU_ANO_NASCIMENTO', 'NU_MES_NASCIMENTO', 'NU_DIA_NASCIMENTO' e 
  'CO_MUNICIPIO_NASCIMENTO', por serem informações unica de cada aluno e possivel identificar esses alunos em cada ano na nossa base de dados
  utilizando esses atributos. Depois e salvo outro arquivo agora com o id.
  
  ##### Porque salvar uma base de dados com Id e outra sem?
  Podiamos muito bem ter somente a base de dados com o Id, porém se fizéssemos isso vamos perder as matriculas de 2009. 
  
