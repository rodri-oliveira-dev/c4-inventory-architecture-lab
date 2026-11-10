# LikeC4: fundação do modelo de arquitetura

Este diretório inicia uma **segunda representação do mesmo sistema** descrito nos quatro níveis [Mermaid](../docs/README.md). Aqui, o LikeC4 modela **elementos e relações uma única vez** e constrói visualizações derivadas, sem criar novos serviços de software ou outra arquitetura.

**Estado atual:** etapa **1 de 5** da trilha LikeC4. Existe uma visão inicial `index` para experimentar o modelo; os diagramas definitivos e a comparação visual serão desenvolvidos nas etapas seguintes. Os seis blocos Mermaid dos capítulos originais continuam sendo as representações publicadas, e **não são gerados automaticamente a partir do LikeC4** nesta fase.

## Estrutura

| Arquivo | Responsabilidade |
| --- | --- |
| [`likec4.config.json`](likec4.config.json) | Configuração e identificação do projeto LikeC4. |
| [`specification.c4`](specification.c4) | Vocabulário único: ator, sistema, sistema externo, aplicação, banco e componente. |
| [`model.c4`](model.c4) | Atores, fronteira do sistema, quatro contêineres e sete relações de referência. |
| [`views.c4`](views.c4) | Visão `index` inicial; a etapa 2 adicionará níveis 1 e 2 explícitos. |

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

O workflow [Documentation Quality](../.github/workflows/docs-quality.yml) executa a validação inicial do LikeC4 após instalar as dependências npm. O tratamento completo de geração, publicação de artefatos e integração contínua para **todas as visões** pertence à etapa 5.

## Modelo compartilhado e invariantes

**Fronteira:** `estoque` é o **Sistema de Gestão de Estoque**, com os contêineres `estoque.web`, `estoque.api`, `estoque.worker` e `estoque.banco`. Pessoas e sistemas externos não pertencem a essa fronteira.

| Identificador LikeC4 | Correspondente Mermaid |
| --- | --- |
| `operador`, `gestor` | Atores humanos do [contexto](../docs/01-contexto.md) |
| `estoque` | Sistema central dos níveis 1 e 2 |
| `vendas`, `notificacoes` | Sistema de Vendas e Provedor de Notificações |
| `estoque.web` | Aplicação Web (SPA) |
| `estoque.api` | API de Estoque (ASP.NET Core / .NET 10) |
| `estoque.worker` | Worker de Notificações (.NET) |
| `estoque.banco` | Banco de Dados (PostgreSQL) |

As relações preservam a iniciativa das chamadas: operadores e gestores usam a Web; Vendas chama a API; a API acessa o PostgreSQL; o Worker lê a outbox e solicita alertas ao provedor. **Não** existe relação direta API → Worker. O padrão outbox não pressupõe um broker nesta arquitetura.

O cenário de referência continua sendo a saída de **10 unidades** de `SKU-001`, com saldo **15 → 5**, estoque mínimo **5**, idempotência para vendas, outbox na mesma transação e entrega eventual de alerta. Esses detalhes são documentados em [escopo](../docs/escopo-funcional.md), [nível 2](../docs/02-containers.md) e [sequência](../docs/fluxo-movimentacao.md).

## Próximas etapas da trilha LikeC4

1. **Fundação (esta etapa):** configuração, vocabulário, modelo compartilhado e visão inicial.
2. **Contexto e Contêineres:** vistas explícitas de níveis 1 e 2, com os mesmos limites de sistema.
3. **Componentes e Código:** aprofundar a API; manter o diagrama UML de classes em Mermaid, sem tentar converter métodos C# em caixas do LikeC4.
4. **Fluxos dinâmicos:** modelar a baixa e o processamento eventual da outbox.
5. **CI/CD e publicação:** exportar, validar e disponibilizar as visões, atualizar índices e comparar ambas as representações.

**Orientação editorial:** ao alterar um componente ou relacionamento em uma das representações, revisar a outra no mesmo PR para não manter duas arquiteturas contraditórias. A eventual geração automática das representações será avaliada no encerramento da trilha.

### Referências

- [Documentação do LikeC4](https://likec4.dev/)
- [Tutorial da DSL](https://likec4.dev/tutorial/)
- [CLI e comando validate](https://likec4.dev/tooling/cli/)
- [Modelo C4 original](https://c4model.com/)
