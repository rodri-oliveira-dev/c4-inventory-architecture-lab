# C4 Inventory Architecture Lab

[![ADR Guard](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/adr-guard.yml/badge.svg)](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/adr-guard.yml)
[![Documentation Quality](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/docs-quality.yml/badge.svg)](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/docs-quality.yml)

Um laboratório **didático e orientado à documentação** para aprender a comunicar a arquitetura de um sistema de gestão de estoque com os **quatro níveis do Modelo C4**, diagramas **Mermaid** e pequenos exemplos em **C#/.NET**.

> **Objetivo:** demonstrar como a mesma solução pode ser apresentada, do contexto de negócio às classes de código, preservando consistência entre os níveis. **Não** se trata de um produto de estoque pronto para produção.

## O cenário

Uma operação precisa cadastrar produtos, registrar entradas e saídas de mercadorias, consultar saldos e emitir alertas quando um produto atinge seu estoque mínimo.

O fio condutor da documentação é uma **saída de 10 unidades**: um operador ou sistema de vendas solicita a baixa; a aplicação valida as regras, registra a movimentação, atualiza o saldo e, quando necessário, agenda uma notificação.

Consulte o [escopo funcional](docs/escopo-funcional.md) e a [arquitetura de referência](docs/arquitetura-referencia.md).

## Os quatro níveis

| Nível | Pergunta principal | Representação planejada |
| --- | --- | --- |
| **1. System Context** | Quem utiliza o sistema e com quais sistemas ele interage? | [C4Context: ver diagrama](docs/01-contexto.md) |
| **2. Containers** | Quais aplicações e armazenamentos compõem a solução? | [C4Container: ver diagrama](docs/02-containers.md) |
| **3. Components** | Como a API é organizada internamente? | [C4Component: ver diagrama](docs/03-componentes.md) |
| **4. Code** | Como as responsabilidades aparecem nas classes C#? | [classDiagram: ver diagrama](docs/04-codigo.md) |

O Mermaid oferece sintaxes experimentais para os diagramas C4 dos três primeiros níveis. Para o quarto nível, usamos um **diagrama de classes**, não uma sintaxe `C4Code` inexistente. Saiba mais no [guia de modelagem](docs/guia-c4.md).

## LikeC4: segunda representação arquitetural

Além dos diagramas Mermaid existentes, iniciamos a [alternativa LikeC4](likec4/README.md), baseada em **um modelo arquitetural compartilhado**. A fundação define os atores, as integrações e os quatro contêineres; a etapa 2 acrescenta as visões de [**Contexto e Contêineres**](likec4/visoes-contexto-conteineres.md) a partir do mesmo modelo. Os capítulos Mermaid continuam disponíveis em paralelo.

Para explorar o modelo (Node.js 22):

```bash
npm install
npm run likec4:validate
npm run likec4:dev
```

O servidor de prévia LikeC4 usa o modelo em `likec4/`. A visualização `index` representa o **nível 1**, com navegação para `conteineres`, a visão do **nível 2**. As próximas etapas incluem componentes, fluxos dinâmicos e publicação, em PRs independentes. Consulte as [convenções e o roteiro](likec4/README.md). A validação inicial do modelo está incluída no workflow [Documentation Quality](.github/workflows/docs-quality.yml).

## Arquitetura que será documentada

- **Aplicação web:** consultas e operações realizadas por pessoas.
- **API ASP.NET Core (.NET 10):** casos de uso, regras de negócio, integrações e acesso aos dados.
- **Worker .NET:** entrega assíncrona de alertas de estoque mínimo.
- **PostgreSQL:** persistência transacional de produtos, saldos, movimentações e mensagens pendentes de notificação.
- **Integrações externas:** sistema de vendas e provedor de notificações.

Essas escolhas são **hipóteses didáticas**, não recomendações universais. Os motivos e limites estão em [decisões arquiteturais](docs/decisoes-arquiteturais.md).

## Roteiro de construção

1. **Fundação:** README, escopo, arquitetura de referência e convenções.
2. **Nível 1:** [contexto do sistema](docs/01-contexto.md) (disponível).
3. **Nível 2:** [contêineres do sistema](docs/02-containers.md) (disponível).
4. **Nível 3:** [componentes internos da API](docs/03-componentes.md) (disponível).
5. **Nível 4:** [classes e exemplos ilustrativos em C#](docs/04-codigo.md) (disponível).
6. **Fluxos e decisões:** [sequência da movimentação](docs/fluxo-movimentacao.md) e aprofundamento dos ADRs 0003 a 0007 (disponível).
7. **Qualidade e publicação:** [validação automática de Mermaid e links](.github/workflows/docs-quality.yml), revisão e [preparação da v1.0.0](docs/publicacao.md) (disponível).

Os quatro níveis já estão documentados: [Contexto](docs/01-contexto.md), [Contêineres](docs/02-containers.md), [Componentes](docs/03-componentes.md) e [Código](docs/04-codigo.md). O nível 4 utiliza `classDiagram` e pequenos [exemplos C#](examples/registrar-saida.md). O [fluxo de movimentação](docs/fluxo-movimentacao.md) ilustra a confirmação transacional e a entrega eventual. A validação de diagramas e links Markdown está configurada na etapa 7.

## Comece por aqui

1. [Nível 1: Contexto do Sistema de Gestão de Estoque](docs/01-contexto.md)
2. [Nível 2: Contêineres do Sistema de Gestão de Estoque](docs/02-containers.md)
3. [Nível 3: Componentes da API de Estoque](docs/03-componentes.md)
4. [Nível 4: Código do caso de uso RegistrarSaida](docs/04-codigo.md)
5. [Fluxo de movimentação: sequência e falhas](docs/fluxo-movimentacao.md)
6. [Exemplos C# e persistência](examples/README.md)
7. [Índice da documentação](docs/README.md)
8. [Escopo e regras de negócio](docs/escopo-funcional.md)
9. [Arquitetura de referência](docs/arquitetura-referencia.md)
10. [Guia dos níveis C4 e Mermaid](docs/guia-c4.md)
11. [Decisões arquiteturais e ADRs](docs/decisoes-arquiteturais.md)
12. [Preparação da release v1.0.0](docs/publicacao.md)

## Validação de decisões arquiteturais

As decisões são registradas como [ADRs propostos](docs/decisoes-arquiteturais.md). Para instalar a versão fixada do **ADR Guard** e validar localmente (requer SDK .NET 10):

```bash
dotnet tool restore
dotnet tool run adr-guard -- check docs/adr
```

O [GitHub Actions](.github/workflows/adr-guard.yml) executa a **Action oficial ADR Guard v1.10.0** em pull requests e na `main`, independentemente de quais arquivos mudaram.

## Qualidade da documentação

O workflow [Documentation Quality](.github/workflows/docs-quality.yml) roda em todo pull request para `main`, pushes para `main` e manualmente. Ele verifica links e âncoras Markdown locais, extrai os blocos Mermaid dos capítulos e tenta renderizá-los com **Mermaid CLI 11.17.1**, sem manter cópias `.mmd` no Git. Os SVGs gerados ficam disponíveis como artefatos do workflow. A versão do Mermaid CLI é declarada em [`package.json`](package.json) e instalada pelo CI a partir desse manifesto, permitindo atualizações propostas pelo Dependabot.

Verificação local (Python 3.12+):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_docs.py --output-dir .tmp/mermaid
```

O comando Python verifica links e a estrutura dos blocos. Para comprovar **renderização**, execute também o Mermaid CLI `11.17.1` sobre cada `.mmd` extraído, como no workflow. Links externos não são consultados via HTTP no CI para evitar instabilidade de rede e limites de requisição.

## Atualizações de dependências

O [Dependabot](.github/dependabot.yml) verifica semanalmente:

- **GitHub Actions** nos workflows, incluindo ações oficiais e a ação ADR Guard.
- **npm** no `package.json` da raiz, utilizado para instalar `@mermaid-js/mermaid-cli` e `likec4` no workflow de documentação.

As atualizações `minor` e `patch` são agrupadas, enquanto mudanças `major` recebem PRs próprios e precisam passar pelo CI antes de merge. O manifesto local [`.config/dotnet-tools.json`](.config/dotnet-tools.json) contém o ADR Guard da CLI, cuja versão deve ser conferida manualmente: este repositório não contém um projeto .NET para o Dependabot NuGet atualizar. Não há dependências Python de terceiros ou uma imagem Docker neste laboratório.

Para contribuir, consulte [CONTRIBUTING.md](CONTRIBUTING.md). Para publicar, consulte o [checklist de v1.0.0](docs/publicacao.md).

## Licença

Distribuído sob a [licença MIT](LICENSE). © 2026 Rodrigo de Oliveira.
