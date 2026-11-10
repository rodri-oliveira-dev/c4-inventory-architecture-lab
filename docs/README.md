# Documentação

Este índice orienta a leitura do laboratório. Os diagramas dos quatro níveis serão criados em PRs posteriores; esta etapa estabelece o vocabulário, as responsabilidades e as regras que eles deverão respeitar.

## Fundação (etapa 1)

| Documento | Finalidade |
| --- | --- |
| [Escopo funcional](escopo-funcional.md) | Atores, funcionalidades, regras e limites do domínio |
| [Arquitetura de referência](arquitetura-referencia.md) | Contêineres previstos, fluxo principal e responsabilidades |
| [Guia C4 e Mermaid](guia-c4.md) | Critérios de modelagem, consistência e renderização |
| [Decisões arquiteturais](decisoes-arquiteturais.md) | Catálogo de ADRs propostos, trade-offs, instalação e validação com ADR Guard |
| [Registros ADR](adr/0001-adotar-monolito-modular.md) | ADRs individuais 0001 a 0009 validados automaticamente |

## Próximos documentos

- **Etapa 2:** `docs/01-contexto.md` — visão de contexto (nível 1).
- **Etapa 3:** `docs/02-containers.md` — aplicações e bancos (nível 2).
- **Etapa 4:** `docs/03-componentes.md` — interior da API (nível 3).
- **Etapa 5:** `docs/04-codigo.md` — classes e relações (nível 4).
- **Etapa 6:** `docs/fluxo-movimentacao.md` e aprofundamento/revisão dos ADRs já registrados.
- **Etapa 7:** automação de diagramas Mermaid e documentação de publicação. A automação de ADRs foi antecipada para a etapa 1.

Os caminhos acima são **planejados**, portanto ainda não são links navegáveis.

Veja também [orientações de contribuição](../CONTRIBUTING.md), [diagramas](../diagrams/README.md) e [exemplos C#](../examples/README.md).
