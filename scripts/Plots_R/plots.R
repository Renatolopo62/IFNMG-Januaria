library(ggplot2)
#library(dplyr)
library(plyr)
library(ggrepel)
library(ggsci)

# matriculas por ano (barra)
matriculas_por_ano <- function(df){
  df <- read.csv('../../dados/dados_padronizados_matriculas_januaria_2009_2018.csv')
  dates <- as.character(paste(df$NU_ANO_CENSO,"-01-01", sep = ""))
  df$NU_ANO_CENSO_DATA = as.Date(dates)
  
  df <- ddply(df,.(NU_ANO_CENSO_DATA), summarise, MATRICULAS = length(NU_ANO_CENSO_DATA))
  
  p <- ggplot(data = df, aes(x = NU_ANO_CENSO_DATA, y = MATRICULAS, label = MATRICULAS))+
    geom_bar(aes(fill = MATRICULAS), stat="identity")+
    #geom_text_repel(vjust = -1, size = 8, segment.color = "transparent")+
    guides(color = guide_legend(title = element_blank()))+
    scale_x_date(date_breaks = "1 year", date_labels = "%Y")+
    scale_y_continuous(expand = c(0.015,0.015)) +
    geom_text(aes(x = NU_ANO_CENSO_DATA, y = MATRICULAS + 35), 
              position = position_dodge(width = 0.8), size=5, stat = "identity")+
    #scale_fill_lancet() +
    guides(fill=guide_legend(title=element_blank()))+
    theme_minimal()+
    labs(x="Ano", y="Número de matrículas") 
  arquivo = paste("graficos/matriculas_por_ano.pdf")
  ggsave(arquivo, width = 18, height = 16)
  p
}


# matriculas por ano e curso (line)
matriculas_por_ano_e_curso <- function(df){
  df <- read.csv('../../dados/dados_padronizados_matriculas_januaria_2009_2018.csv')
  dates <- as.character(paste(df$NU_ANO_CENSO,"-01-01", sep = ""))
  df$NU_ANO_CENSO_DATA = as.Date(dates)
  
  df <- ddply(df,.(NU_ANO_CENSO_DATA, NOME_CURSO), summarise, MATRICULAS = length(NU_ANO_CENSO_DATA))
  
  p <- ggplot(data = df, aes(x = NU_ANO_CENSO_DATA, y = MATRICULAS, group = NOME_CURSO, label = MATRICULAS))+
    geom_line(aes(color = NOME_CURSO), size = 2)+
    geom_point(aes(color = NOME_CURSO), size = 5)+
    guides(color = guide_legend(title = element_blank()))+
    scale_x_date(date_breaks = "1 year", date_labels = "%Y")+
    scale_y_continuous(expand = c(0.07,0.2)) +
    #geom_text(aes(x = NU_ANO_CENSO_DATA + 3), position = position_dodge(width = 0.8), size=5, stat = "identity")+
    theme_minimal()+
    geom_text_repel(vjust=-1, size=4, segment.color = "transparent")+
    labs(x="Ano", y="Número de matrículas") 
  arquivo = paste("graficos/matriculas_por_ano_e_curso.pdf")
  ggsave(arquivo, width = 18, height = 16)
  p
}

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


df <- dados_padronizados_matriculas_januaria_2009_2018

matriculas_por_ano(df)
