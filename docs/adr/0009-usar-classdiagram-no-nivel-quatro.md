# Usar Mermaid classDiagram para o nível 4 do C4

## Status

Proposed

## Context

O repositório pretende manter todos os níveis em Markdown e Mermaid, com renderização fácil no GitHub. O Mermaid oferece sintaxe experimental de C4 para contexto, contêineres e componentes, mas não um tipo C4Code específico. Consideramos ferramenta de desenho externa ou um diagrama de classes Mermaid para detalhar o código.

## Decision

Representar o nível 4 com Mermaid classDiagram, limitado às classes, interfaces e relações diretamente ligadas ao caso de uso de saída de estoque. Não afirmar que classDiagram é uma extensão C4 nativa; ele é uma representação complementar da perspectiva de código.

## Consequences

A documentação continua baseada em texto, versionável e revisável nos pull requests. Leitores poderão relacionar componentes da API às estruturas C# sem depender de imagens produzidas manualmente.

Diagramas de classes não expressam sozinhos comportamento em execução, transações nem concorrência. Esses aspectos exigirão explicações e um diagrama de sequência complementar. A renderização deve ser verificada conforme a versão do Mermaid disponível no GitHub.
