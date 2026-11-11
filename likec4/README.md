# LikeC4: modelo de arquitetura e visões C4

Este diretório inicia uma **segunda representação do mesmo sistema** descrito nos quatro níveis [Mermaid](../docs/README.md). Aqui, o LikeC4 modela **elementos e relações uma única vez** e constrói visualizações derivadas, sem criar novos serviços de software ou outra arquitetura.

**Estado atual:** etapa **5 de 5** da trilha LikeC4. As três visões estruturais de [Contexto, Contêineres](visoes-contexto-conteineres.md) e [Componentes da API](visao-componentes.md) convivem com dois [fluxos dinâmicos em sequência](fluxos-dinamicos.md). O [site interativo LikeC4](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/) é preparado pelo workflow de Pages; estará disponível quando o deploy da `main` for confirmado. O nível 4 (Code) e os diagramas de sequência originais permanecem em Mermaid; LikeC4 **não gera automaticamente** os capítulos Mermaid.

## Estrutura

| Arquivo | Responsabilidade |
| --- | --- |
| [`likec4.config.json`](likec4.config.json) | Configuração e identificação do projeto LikeC4. |
| [`specification.c4`](specification.c4) | Vocabulário único: ator, sistema, sistema externo, aplicação, banco e componente. |
| [`model.c4`](model.c4) | Atores, sistema, quatro contêineres, cinco componentes na API e relações compartilhadas em diferentes níveis. |
| [`views.c4`](views.c4) | Três visões estáticas: `index` (contexto), `conteineres` (sistema ampliado) e `componentes` (API ampliada). |
| [`dynamics.c4`](dynamics.c4) | Duas visões dinâmicas: `registrarSaida` e `entregarAlerta`, com participantes do modelo existente. |
| [**Contexto e Contêineres**](visoes-contexto-conteineres.md) | Guia das duas primeiras visões e suas fronteiras. |
| [**Componentes da API**](visao-componentes.md) | Zoom no contêiner API, cinco componentes, dependências e comparação com Mermaid. |
| [**Fluxos dinâmicos**](fluxos-dinamicos.md) | Confirmação síncrona da baixa e envio eventual do alerta, com comparativo Mermaid/LikeC4. |
| [**Comparação e publicação**](../docs/likec4-vs-mermaid.md) | Compara as duas abordagens e documenta GitHub Pages, build e CI. |

## Tecnologias e requisitos

- **Node.js 22**, compatível com o `package.json` da raiz.
- **LikeC4 1.60.0**, fixado nas `devDependencies` do mesmo `package.json` usado pelo Mermaid CLI.
- [Dependabot npm](../.github/dependabot.yml) já monitora dependências no manifesto existente. Atualizações devem passar por validação e revisão humana.

Na raiz do repositório:

```bash
npm install
npm run likec4:validate
npm run likec4:dev
npm run likec4:build:pages
```

O comando `likec4:dev` inicia uma prévia interativa local (porta padrão 5173). O comando `likec4:validate` verifica o modelo de referência. Para formatar os arquivos `.c4`, use `npm run likec4:format`.

A [versão leve para iPhone](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/mobile/) não executa o motor visual do LikeC4: mostra os seis diagramas Mermaid pré-renderizados como SVG, com link de retorno à experiência completa. Um redirecionamento executado antes dos bundles do LikeC4 seleciona esse modo em telas iOS compactas; `?full=1` desativa o redirecionamento. Consulte [compatibilidade mobile](../docs/compatibilidade-mobile.md) e suas limitações.

O workflow [Documentation Quality](../.github/workflows/docs-quality.yml) valida o modelo LikeC4 após instalar as dependências npm. O novo [LikeC4 Site](../.github/workflows/likec4-pages.yml) compila o site em PRs e, após merge na `main`, publica a versão estática no GitHub Pages. A [comparação Mermaid vs. LikeC4](../docs/likec4-vs-mermaid.md) explica publicação, limites e configuração de Pages.

## As três visões disponíveis

- **[`index`: Nível 1 / Contexto](visoes-contexto-conteineres.md#nível-1-contexto-index):** duas pessoas, sistema central e dois sistemas externos; quatro relações de negócio inferidas do modelo.
- **[`conteineres`: Nível 2 / Contêineres](visoes-contexto-conteineres.md#nível-2-contêineres-conteineres):** fronteira do sistema ampliada, com quatro contêineres, participantes externos e sete relações agregadas. Ao selecionar o sistema na visão `index`, a navegação abre `conteineres`.
- **[`componentes`: Nível 3 / Componentes da API](visao-componentes.md):** cinco componentes dentro da API e colaboradores externos. Selecionar a API em `conteineres` abre o novo zoom.

Os detalhes, protocolos e critérios de comparação com Mermaid estão nos guias de [Contexto e Contêineres](visoes-contexto-conteineres.md) e de [Componentes da API](visao-componentes.md).

## Fluxos dinâmicos disponíveis

- **[`registrarSaida`: saída síncrona](fluxos-dinamicos.md#1-registrarsaida-baixa-e-confirmação-síncrona):** Sistema de Vendas, endpoints, caso de uso, persistência, regras e PostgreSQL, com commit antes da resposta.
- **[`entregarAlerta`: entrega eventual](fluxos-dinamicos.md#2-entregaralerta-outbox-e-entrega-eventual):** Worker, PostgreSQL e provedor; alternativas para confirmação e falha/timeout, sem prometer entrega exatamente uma vez.

Ambos os fluxos usam `variant sequence` e reutilizam participantes de `model.c4`. A [documentação da etapa 4](fluxos-dinamicos.md) detalha as invariantes de concorrência, idempotência e outbox.

## Modelo compartilhado e invariantes

**Fronteira:** `estoque` é o **Sistema de Gestão de Estoque**, com os contêineres `estoque.web`, `estoque.api`, `estoque.worker` e `estoque.banco`. Somente `estoque.api` contém cinco componentes. Pessoas e sistemas externos permanecem fora da fronteira de `estoque`.

| Identificador LikeC4 | Correspondente Mermaid |
| --- | --- |
| `operador`, `gestor` | Atores humanos do [contexto](../docs/01-contexto.md) |
| `estoque` | Sistema central dos níveis 1 e 2 |
| `vendas`, `notificacoes` | Sistema de Vendas e Provedor de Notificações |
| `estoque.web` | Aplicação Web (SPA) |
| `estoque.api` | API de Estoque (ASP.NET Core / .NET 10) |
| `estoque.worker` | Worker de Notificações (.NET) |
| `estoque.banco` | Banco de Dados (PostgreSQL) |
| `estoque.api.http`, `estoque.api.movimentacoes`, `estoque.api.gestao`, `estoque.api.regras`, `estoque.api.persistencia` | Cinco [componentes da API](visao-componentes.md), no C4 nível 3 |

As relações preservam a iniciativa das chamadas: operadores e gestores usam a Web; Vendas chama a API; a API acessa o PostgreSQL; o Worker lê a outbox e solicita alertas ao provedor. **Não** existe relação direta API → Worker. O padrão outbox não pressupõe um broker nesta arquitetura.

O cenário de referência continua sendo a saída de **10 unidades** de `SKU-001`, com saldo **15 → 5**, estoque mínimo **5**, idempotência para vendas, outbox na mesma transação e entrega eventual de alerta. Esses detalhes são documentados em [escopo](../docs/escopo-funcional.md), [nível 2](../docs/02-containers.md) e [sequência](../docs/fluxo-movimentacao.md).

## Próximas etapas da trilha LikeC4

1. **Fundação (concluída):** configuração, vocabulário e modelo compartilhado.
2. **Contexto e Contêineres (concluída):** visões de níveis 1 e 2 com as mesmas fronteiras do Mermaid.
3. **Componentes e Código (concluída):** aprofundar a API nos cinco componentes; manter o diagrama UML de classes em Mermaid.
4. **Fluxos dinâmicos (concluída nesta branch):** modelar baixa síncrona e processamento eventual da outbox como visões de sequência LikeC4.
5. **CI/CD e publicação (concluída nesta branch):** validar, compilar e publicar o site interativo no GitHub Pages, atualizar índices e comparar ambas as representações. O deploy depende do merge na `main` e da fonte Pages = GitHub Actions.

**Orientação editorial:** ao alterar um componente ou relacionamento em uma das representações, revisar a outra no mesmo PR para não manter duas arquiteturas contraditórias. A eventual geração automática das representações será avaliada no encerramento da trilha.

### Referências

- [Documentação do LikeC4](https://likec4.dev/)
- [Tutorial da DSL](https://likec4.dev/tutorial/)
- [CLI e comando validate](https://likec4.dev/tooling/cli/)
- [Modelo C4 original](https://c4model.com/)
