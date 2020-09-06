import getters as get
import verificacoes as verifica
import pandas as pd

#cod_cursos = get.getCodCurso()

#get.getMatriculas(cod_cursos, '2009')
#get.getNomeCurso(cod_cursos)
#get.getDadosPadronizados()

#print(get.LIST_COLUMNS)
#529

df = pd.read_csv('../dados/dados_padronizados_matriculas_januaria_2009_2018_com_id.csv')
#verifica.contIdRepetido(df)
verifica.matriculas_repetidas(df)