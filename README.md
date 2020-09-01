# IFNMG-Januaria
Uma análise do ensino superior do IFNMG campus januária entre os anos de 2009 e 2018 utilizando os dados do INEP.

## Etapas 
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
  Antes de definir quais colunas devemos descartar temos que definir nossos objetivos com essa base de dados.
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

  * Proximo
