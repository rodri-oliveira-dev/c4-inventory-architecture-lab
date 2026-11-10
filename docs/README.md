# Documentação

Este índice orienta a leitura do laboratório. Os **quatro níveis do C4** estão disponíveis em Mermaid: os níveis 1 a 3 com sintaxe C4, o nível 4 com diagrama de classes e uma visão de sequência complementar na etapa 6.

## Fundação (etapa 1)

| Documento | Finalidade |
| --- | --- |
| [Escopo funcional](escopo-funcional.md) | Atores, funcionalidades, regras e limites do domínio |
| [Arquitetura de referência](arquitetura-referencia.md) | Contêineres previstos, fluxo principal e responsabilidades |
| [Guia C4 e Mermaid](guia-c4.md) | Critérios de modelagem, consistência e renderização |
| [Decisões arquiteturais](decisoes-arquiteturais.md) | Catálogo de ADRs propostos, trade-offs, instalação e validação com ADR Guard |
| [Registros ADR](adr/0001-adotar-monolito-modular.md) | ADRs individuais 0001 a 0009 validados automaticamente |

## C4: diagramas por nível

- **Etapa 2 (disponível):** [Nível 1: Contexto do sistema](01-contexto.md) — atores, integrações e fronteira do sistema.
- **Etapa 3 (disponível):** [Nível 2: Contêineres](02-containers.md) — aplicações executáveis, armazenamento, tecnologias e comunicação.
- **Etapa 4 (disponível):** [Nível 3: Componentes da API](03-componentes.md) — responsabilidades internas e dependências transacionais.
- **Etapa 5 (disponível):** [Nível 4: Código](04-codigo.md) — classes, interfaces e o caso de uso `RegistrarSaida`.

**Etapa 6 (disponível):** [Fluxo de movimentação: confirmação, outbox e falhas](fluxo-movimentacao.md) — interação síncrona e entrega eventual.

**Exemplos de apoio:** [C# do caso de uso](../examples/registrar-saida.md) · [consistência transacional, idempotência e outbox](../examples/persistencia-transacional.md).

## Próximos documentos
- **Etapa 7:** automação de diagramas Mermaid e documentação de publicação. A automação de ADRs foi antecipada para a etapa 1.

Os caminhos acima são **planejados**, portanto ainda não são links navegáveis.

Veja também [orientações de contribuição](../CONTRIBUTING.md), [diagramas](../diagrams/README.md) e [exemplos C#](../examples/README.md).
