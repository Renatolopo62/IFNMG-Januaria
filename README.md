# IFNMG-Januaria
Uma análise do ensino superior do IFNMG campus januária entre os anos de 2009 e 2018 utilizando os dados do INEP.

## Etapas 
###  Filtragem dos dados
 #### 1. Baixar os censo de Educação superior no site do INEP.
 Os arquivos do censo podem ser encontrados [aqui](http://portal.inep.gov.br/microdados).
####  2. filtragem das matriculas que pertencem ao IFNMG - Januária. 
  A função `getCodCurso()` retorna 
  uma lista com os códigos dos cursos do IFNMG - Januária encontrados na tabela `DM_LOCAL_OFERTA`,
  esses codigos serão usados para filtrar quais matriculas nos interessa dentre as milhares encontradas
  na tabela `DM_ALUNO`, para isso usamos a função `getMatriculas(cod_cursos, ano)`, que recebe como parametro
  a lista com os codigos dos cursos e o ano do censo. As filtragem podem demorar alguns minutos já que estamos 
  trabalhando com uma tabela que tem as matriculas de alunos do Ensino superior do Brasil todo. No final será criado 
  para cada ano um arquivo csv com as matriculas, que serão unidos em um só arquivo na proxima etapa.  
  
  Obs: Os arquivos `DM_LOCAL_OFERTA` e `DM_ALUNO` devem ser extraidos e passados como parametro o caminho onde ele se encontra
  de acordo com o ano.
