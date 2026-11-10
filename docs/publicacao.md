# Preparação da release v1.0.0

A `v1.0.0` é a **primeira publicação documental planejada** do C4 Inventory Architecture Lab. Esta página é um checklist para o responsável pelo repositório. **Criar este documento não cria uma tag, nem publica uma release.**

## Escopo incluído

- Os quatro níveis C4 para um único sistema de gestão de estoque (Contexto, Contêineres, Componentes e Código).
- O fluxo de saída de 10 unidades, com bloqueio de saldo, idempotência e outbox.
- Os exemplos ilustrativos C#/.NET 10 e PostgreSQL.
- Os nove ADRs mantidos como **Proposed** e o ADR Guard em CI.
- O workflow de documentação com renderização de Mermaid e verificação de links Markdown.

## Critérios antes de publicar

1. Integrar o PR da etapa 7 na `main` **somente após revisão**.
2. Confirmar as verificações **ADR Guard** e **Documentation Quality / Mermaid and Markdown links** com resultado verde no commit final da `main`.
3. Abrir o artefato **`mermaid-diagram-previews`** da última execução de Documentation Quality. Verificar legibilidade e conteúdo dos **6 SVGs** gerados; a sintaxe renderizada não substitui revisão editorial.
4. Conferir no GitHub os quatro diagramas dos [níveis 1 a 4](README.md) e os [dois diagramas de sequência](fluxo-movimentacao.md).
5. Revisar o [escopo funcional](escopo-funcional.md) e a correspondência com as responsabilidades, relações e interfaces entre níveis.
6. Revisar os [ADRs](decisoes-arquiteturais.md) e manter `Proposed` até que uma decisão humana os aprove individualmente; a release não implica aprovação dos ADRs.
7. Conferir o [CHANGELOG](../CHANGELOG.md), links externos relevantes e o caráter **não executável** dos exemplos.
8. Na página de **Releases** do GitHub, criar manualmente um novo draft com tag **`v1.0.0`**, alvo `main`, usando as notas abaixo. Publicar somente após a conferência final.

## Texto sugerido para a release

**Título:** `v1.0.0 — Modelo C4 aplicado a um Sistema de Gestão de Estoque`

**Descrição:**

> Primeira versão documental do C4 Inventory Architecture Lab. O laboratório apresenta os quatro níveis do Modelo C4 em Mermaid, um cenário único de saída de estoque, exemplos ilustrativos em C#/.NET e decisões arquiteturais rastreáveis. Inclui diagramas de sequência para a baixa transacional e o processamento assíncrono de notificações, além de validação de ADRs e documentação via GitHub Actions.
>
> O projeto é educativo: não inclui aplicação executável nem oferece garantias de prontidão para produção.

## Comandos de referência

Para validar links locais, âncoras e extrair as definições Mermaid:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_docs.py --output-dir .tmp/mermaid
```

A **renderização de todos os diagramas** é feita pelo workflow `Documentation Quality`. O `ADR Guard` é executado separadamente. Nenhum desses checks substitui o julgamento sobre modelagem, idempotência ou implantação.

## Após a publicação

- Conferir a página da release e a tag.
- Se desejar, divulgar o repositório e vinculá-lo ao artigo sobre C4.
- Abrir issues futuras para exemplos adicionais, melhorias de renderização e possíveis projetos executáveis, sem misturá-los ao escopo documental inicial.
