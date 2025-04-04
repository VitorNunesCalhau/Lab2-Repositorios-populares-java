# Relatório final

## Introdução
Este trabalho explora a qualidade interna de projetos open-source escritos em Java e hospedados no GitHub, com foco nos repositórios mais populares. A análise considera aspectos como o grau de popularidade, tempo de existência, frequência de atualizações e dimensão dos projetos, buscando identificar como esses fatores se relacionam com métricas de qualidade de código obtidas por meio da ferramenta CK.

## Hipótese
### RQ 01
#### Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
Repositórios com melhores indicadores de qualidade não estarão entre os mais populares nem entre os menos populares.Imaginamos que a qualidade será um fator na popularidade dos repositórios, mas, nos mais populares, devido à sua maior visibilidade, haverá mais colaboradores, o que poderá influenciar a qualidade do código.

### RQ 02
#### Qual a relação entre a maturidade do repositórios e as suas características de qualidade?
Repositórios mais antigos tenderão a apresentar um nível de qualidade maior, já que a manutenção e a escalabilidade do código não são viáveis de forma constante em um código de baixa qualidade.

### RQ 03
#### Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
"Repositórios com muita atividade tenderão a apresentar uma qualidade de código inferior, já que o grande número de colaboradores, com diferentes níveis de conhecimento e vícios de código, contribuiu para o projeto, abrindo brechas para erros e inconsistências."
### RQ 04
#### Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?
Repositórios maiores tenderão a apresentar um nível de qualidade maior, já que a manutenção e a escalabilidade do código não são viáveis de forma constante em um código de baixa qualidade.

## Metodologia
Para responder às questões de pesquisa, foi realizada a coleta de dados dos 1.000 repositórios Java mais estrelados no GitHub, utilizando para isso as APIs GraphQL da plataforma. Após a coleta, aplicamos a ferramenta CK para realizar a análise estática do código e extrair métricas relacionadas à qualidade interna dos projetos.

### As métricas de processo consideradas foram:

- Popularidade: quantidade de estrelas no GitHub
- Tamanho: número de linhas de código (LOC) e linhas de comentários
- Atividade: total de releases publicadas
- Maturidade: idade do repositório em anos

### Já as métricas de qualidade interna, calculadas com base na ferramenta CK, incluem:

- CBO (Coupling Between Objects)
- DIT (Depth of Inheritance Tree)
- LCOM (Lack of Cohesion of Methods)

Todos os dados obtidos foram organizados em um arquivo CSV para posterior análise.
## Resultados

### RQ 01 - Popularidade e Qualidade
A análise indica que os repositórios mais populares apresentam baixa LCOM, o que sugere maior coesão entre os métodos das classes. Além disso, a média de LOC também foi relativamente baixa, indicando projetos menores ou com código mais enxuto. Esses resultados sugerem que repositórios populares tendem a manter uma boa organização interna, possivelmente devido à maior visibilidade e atenção da comunidade.

### RQ 02 - Maturidade e Qualidade
A análise mostra que repositórios mais antigos apresentam maior variação nos valores de LCOM, o que pode refletir diferenças no estilo de programação ao longo do tempo ou mudanças na estrutura do projeto. Isso indica que, embora a maturidade não garanta coesão alta, ela traz diversidade no histórico de desenvolvimento, impactando a consistência do código.

### RQ 03 - Atividade e Qualidade
A análise revelou uma correlação positiva entre o número de releases e a qualidade do código. Repositórios com mais releases tendem a apresentar melhores métricas, como um DIT (profundidade da hierarquia de herança) em níveis adequados, indicando um uso equilibrado da herança. Isso sugere que repositórios mais ativos passaram por mais ciclos de melhoria, favorecendo uma estrutura de código mais bem organizada.

### RQ 04 - Tamanho e Qualidade
A análise mostrou uma correlação positiva entre o tamanho do repositório e a qualidade do código. Repositórios maiores tendem a apresentar melhores métricas, possivelmente porque sua maior complexidade exige maior organização e qualidade interna para manter o código sustentável e gerenciável ao longo do tempo.

![36805858-00a4-42e0-ad20-ac0d31f67e34](https://github.com/user-attachments/assets/4b529eec-fe8a-4a2d-9de0-183ce95841f3)

## Conclusão

A análise dos 1.000 repositórios Java mais populares do GitHub revelou padrões interessantes entre popularidade, maturidade, atividade, tamanho e qualidade interna do código. Repositórios populares apresentaram boa coesão (LCOM baixo), sugerindo que a visibilidade pode estar associada a um cuidado maior com a estrutura do código. Repositórios mais antigos demonstraram maior variação na coesão, indicando que o tempo de vida influencia a consistência, mas não garante qualidade constante. Projetos com maior número de releases mostraram melhor desempenho em métricas como DIT, refletindo melhorias graduais ao longo das iterações. Por fim, repositórios maiores também apresentaram melhor qualidade, o que reforça a ideia de que maior complexidade demanda uma estrutura mais bem organizada.

Esses resultados indicam que fatores como atividade e tamanho têm forte relação com a qualidade do código, enquanto popularidade e maturidade influenciam de forma mais variável. A combinação dessas métricas pode ajudar a identificar projetos bem estruturados e com maior potencial de manutenção e evolução.
