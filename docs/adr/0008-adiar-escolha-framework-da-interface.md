# Adiar a escolha de framework da interface web

## Status

Proposed

## Context

No nível 2, a aplicação web representa a interação de operadores e gestores com a API de estoque. Escolher React, Angular, Vue ou outra tecnologia agora não influencia as regras centrais de movimentação e desviaria o foco didático dos limites entre contêineres.

## Decision

Representar a interface apenas como uma aplicação web SPA, sem selecionar framework ou implementar frontend durante as etapas de documentação arquitetural. A API deverá expor comportamentos conceituais coerentes com os casos de uso, sem depender de componentes específicos de UI.

## Consequences

A documentação permanece concentrada nas responsabilidades e integrações e não cria dependência desnecessária de uma biblioteca de interface. O leitor pode compreender o nível 2 sem conhecer um framework.

A decisão deixa em aberto detalhes de roteamento, autenticação no navegador, gestão de estado e composição visual. Caso uma demonstração executável seja criada, a escolha precisará ser revisitada e documentada.
