# Como contribuir

Obrigado pelo interesse neste laboratório de documentação arquitetural.

## Princípios

- Priorize clareza didática, rigor técnico e consistência entre os quatro níveis C4.
- Documente em **português do Brasil**; preserve nomes de conceitos conhecidos (`System Context`, `Container`, `Component` e `Code`) quando melhorarem a precisão.
- Mantenha os diagramas Mermaid legíveis e restritos à fronteira do nível.
- Não introduza novas tecnologias ou componentes apenas para deixar a arquitetura mais complexa.
- Se alterar uma regra de negócio, revise os documentos e diagramas afetados.

## Fluxo sugerido

1. Abra uma issue para propor ajustes de escopo ou arquitetura.
2. Crie uma branch a partir da `main` e faça mudanças pequenas e revisáveis.
3. Descreva no PR a motivação, os documentos afetados e as verificações realizadas.
4. Confira links relativos e a renderização dos blocos Mermaid no GitHub; o workflow de documentação verifica automaticamente links e renderização.
5. Ao alterar uma decisão arquitetural, crie ou atualize um ADR em `docs/adr/` e mantenha [o catálogo](docs/decisoes-arquiteturais.md) coerente.
6. Execute `dotnet tool restore` e `dotnet tool run adr-guard -- check docs/adr` antes de enviar o PR (requer SDK .NET 10).
7. Execute também `python3 -m unittest discover -s tests -v` e `python3 scripts/validate_docs.py --output-dir .tmp/mermaid` (Python 3.12+).
8. Não altere o status `Proposed` para `Accepted` sem aprovação humana e não inclua credenciais, dados reais ou código proprietário.

O GitHub Actions valida ADRs com ADR Guard e documentação com [Documentation Quality](.github/workflows/docs-quality.yml). O segundo job confere os links locais e renderiza Mermaid usando a CLI; a inspeção visual no GitHub continua importante.

## Estilo

- Use arquivos Markdown, títulos hierárquicos e exemplos sucintos.
- Mantenha o cenário da **saída de 10 unidades** ao atravessar os níveis.
- Ao representar decisões relevantes, registre alternativas e trade-offs.
- Código C# é ilustrativo: deixe claras as simplificações.

Confira o [índice da documentação](docs/README.md) e o [guia C4](docs/guia-c4.md).
