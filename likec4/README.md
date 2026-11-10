# LikeC4: modelo de arquitetura e visões C4

Este diretório inicia uma **segunda representação do mesmo sistema** descrito nos quatro níveis [Mermaid](../docs/README.md). Aqui, o LikeC4 modela **elementos e relações uma única vez** e constrói visualizações derivadas, sem criar novos serviços de software ou outra arquitetura.

**Estado atual:** etapa **3 de 5** da trilha LikeC4. [Contexto e Contêineres](visoes-contexto-conteineres.md) e [Componentes da API](visao-componentes.md) são três projeções do mesmo modelo. O nível 4 (Code) permanece em Mermaid, assim como os diagramas de sequência originais, e **não é gerado automaticamente pelo LikeC4**.

## Estrutura

| Arquivo | Responsabilidade |
| --- | --- |
| [`likec4.config.json`](likec4.config.json) | Configuração e identificação do projeto LikeC4. |
| [`specification.c4`](specification.c4) | Vocabulário único: ator, sistema, sistema externo, aplicação, banco e componente. |
| [`model.c4`](model.c4) | Atores, sistema, quatro contêineres, cinco componentes na API e relações compartilhadas em diferentes níveis. |
| [`views.c4`](views.c4) | Três visões: `index` (contexto), `conteineres` (sistema ampliado) e `componentes` (API ampliada). |
| [**Contexto e Contêineres**](visoes-contexto-conteineres.md) | Guia das duas primeiras visões e suas fronteiras. |
| [**Componentes da API**](visao-componentes.md) | Zoom no contêiner API, cinco componentes, dependências e comparação com Mermaid. |

## Tecnologias e requisitos

- **Node.js 22**, compatível com o `package.json` da raiz.
- **LikeC4 1.60.0**, fixado nas `devDependencies` do mesmo `package.json` usado pelo Mermaid CLI.
- [Dependabot npm](../.github/dependabot.yml) já monitora dependências no manifesto existente. Atualizações devem passar por validação e revisão humana.

Na raiz do repositório:

```bash
npm install
npm run likec4:validate
npm run likec4:dev
```

O comando `likec4:dev` inicia uma prévia interativa local (porta padrão 5173). O comando `likec4:validate` verifica o modelo de referência. Para formatar os arquivos `.c4`, use `npm run likec4:format`.

O workflow [Documentation Quality](../.github/workflows/docs-quality.yml) executa a validação do modelo LikeC4 após instalar as dependências npm. A exportação e publicação automatizadas das visões pertencem à etapa 5.

## As três visões disponíveis

- **[`index`: Nível 1 / Contexto](visoes-contexto-conteineres.md#nível-1-contexto-index):** duas pessoas, sistema central e dois sistemas externos; quatro relações de negócio inferidas do modelo.
- **[`conteineres`: Nível 2 / Contêineres](visoes-contexto-conteineres.md#nível-2-contêineres-conteineres):** fronteira do sistema ampliada, com quatro contêineres, participantes externos e sete relações agregadas. Ao selecionar o sistema na visão `index`, a navegação abre `conteineres`.
- **[`componentes`: Nível 3 / Componentes da API](visao-componentes.md):** cinco componentes dentro da API e colaboradores externos. Selecionar a API em `conteineres` abre o novo zoom.

Os detalhes, protocolos e critérios de comparação com Mermaid estão nos guias de [Contexto e Contêineres](visoes-contexto-conteineres.md) e de [Componentes da API](visao-componentes.md).

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
3. **Componentes e Código (concluída nesta branch):** aprofundar a API nos cinco componentes; manter o diagrama UML de classes em Mermaid, sem tentar converter métodos C# em caixas do LikeC4.
4. **Fluxos dinâmicos:** modelar a baixa e o processamento eventual da outbox.
5. **CI/CD e publicação:** exportar, validar e disponibilizar as visões, atualizar índices e comparar ambas as representações.

**Orientação editorial:** ao alterar um componente ou relacionamento em uma das representações, revisar a outra no mesmo PR para não manter duas arquiteturas contraditórias. A eventual geração automática das representações será avaliada no encerramento da trilha.

### Referências

- [Documentação do LikeC4](https://likec4.dev/)
- [Tutorial da DSL](https://likec4.dev/tutorial/)
- [CLI e comando validate](https://likec4.dev/tooling/cli/)
- [Modelo C4 original](https://c4model.com/)
