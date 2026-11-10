# Changelog

Este repositório é um laboratório de arquitetura **orientado à documentação**. As mudanças relevantes são registradas aqui.

## Unreleased

### LikeC4: trilha complementar

- Modelo arquitetural compartilhado com três visões estruturais e duas dinâmicas.
- Geração de site interativo estático por LikeC4, com base path correto para GitHub Pages e navegação por hash.
- Workflow que valida e compila o site em PRs e publica após alterações na `main`.
- Guia comparativo de Mermaid e LikeC4, sem substituir o nível 4 em UML de classes.

A versão **v1.0.0** está preparada para publicação **após** a integração do PR da etapa 7 e a aprovação das verificações automatizadas. **Nenhuma tag ou release é criada automaticamente**.

### Funcionalidades de documentação planejadas para v1.0.0

- Quatro níveis do modelo C4 no mesmo cenário de estoque, utilizando Mermaid:
  - Nível 1: System Context;
  - Nível 2: Containers;
  - Nível 3: Components, com foco na API de Estoque;
  - Nível 4: Code, com diagrama de classes.
- Dois diagramas de sequência da movimentação síncrona e do envio eventual de alertas.
- Exemplos C# ilustrativos para `RegistrarSaida`, regras de saldo e persistência transacional.
- Nove ADRs com status `Proposed`, com validação pelo ADR Guard.
- Validação de links locais e renderização Mermaid automatizadas no GitHub Actions.
- Documentação de contribuição e checklist de publicação.

### Limites

Não há aplicação de estoque executável, API publicada, worker implantado ou infraestrutura operacional. Os diagramas são didáticos e os exemplos C# não são tratados como implementação de produção.
