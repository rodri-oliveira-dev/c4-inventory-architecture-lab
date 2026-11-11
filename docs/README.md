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

## Representação alternativa: LikeC4

- [Modelo compartilhado LikeC4](../likec4/README.md) — tipos, atores, integrações, contêineres e comandos locais.
- [LikeC4: Contexto e Contêineres (etapa 2)](../likec4/visoes-contexto-conteineres.md) — duas projeções do mesmo modelo e comparação com Mermaid.
- [LikeC4: Componentes da API (etapa 3)](../likec4/visao-componentes.md) — terceiro zoom, cinco componentes internos, relações e integração com o nível 4 Mermaid.
- [LikeC4: Fluxos dinâmicos (etapa 4)](../likec4/fluxos-dinamicos.md) — confirmação da baixa e entrega eventual do alerta como duas visões de sequência.
- [Mermaid vs. LikeC4: trade-offs e publicação](likec4-vs-mermaid.md) — matriz de critérios técnicos, observações do laboratório, escolha por cenário e deploy via GitHub Pages.
- [Compatibilidade mobile](compatibilidade-mobile.md) — alternativa de baixo consumo para iPhone, limitações e validações recomendadas.

## Qualidade e publicação (etapa 7)

- [Automação: Documentation Quality](../.github/workflows/docs-quality.yml) — verifica links e âncoras locais e renderiza os seis blocos Mermaid com versão fixa da CLI.
- [Validador Markdown e Mermaid](../scripts/validate_docs.py) — mantém os capítulos Markdown como fonte única dos diagramas.
- [Checklist para a release v1.0.0](publicacao.md) — revisão, verificações e publicação manual após merge.
- [Changelog](../CHANGELOG.md) — histórico das entregas.

Os ADRs continuam validados pelo [ADR Guard](../.github/workflows/adr-guard.yml) como workflow independente.

Veja também [orientações de contribuição](../CONTRIBUTING.md), [diagramas](../diagrams/README.md) e [exemplos C#](../examples/README.md).
