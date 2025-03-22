# Laboratório 02 - Um estudo das caracteristicas de qualidade de sistemas java
## Objetivo
Buscando informações da API do github vamos analisar os mil repositóios mais populares e relevantes do github, calculando métricas para responder as seguintes perguntas:
- RQ 01. Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
- RQ 02. Qual a relação entre a maturidade do repositórios e as suas características de qualidade?
- RQ 03. Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
- RQ 04. Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?

Para responder a essas perguntas buscaremos as seguintes métricas:
- Tamanho: linhas de código (LOC) e linhas de comentários
- Atividade: número de releases
- Maturidade: idade (em anos) de cada repositório coletado
- CBO: Coupling between objects
- DIT: Depth Inheritance Tree
- LCOM: Lack of Cohesion of Methods

## Descrição das Sprints
### Sprint 1
Na sprint 1 foi desenvolvido um script em python que usa a API GraphQL do GitHub para obter as informações dos 1000 repositórios mais populares que usam java para o desenvolvimento.<br>
A consulta feita busca:
- Número de estrelas
- Linhas de código e linhas de comentários
- Número de releases
- Idade de cada repositório coletado

Foi usado como parâmetro de qualidade:
- CBO
- DIT
- LCOM

### Sprint 2
