# LikeC4: Contexto e Contêineres (etapa 2)

Esta etapa apresenta **duas visões do mesmo modelo arquitetural**, sem duplicar elementos ou relações. O arquivo [`views.c4`](views.c4) contém as projeções; o [`model.c4`](model.c4) continua sendo a única definição dos atores, sistemas, contêineres e interações.

**Público:** o nível 1 atende também pessoas de negócio; o nível 2 é voltado principalmente a arquitetura, desenvolvimento e operações. Trata-se de um **modelo hipotético**, não de um serviço em produção.

## Nível 1: Contexto (`index`)

**Pergunta:** quem utiliza o Sistema de Gestão de Estoque e com quais sistemas ele se integra?

A visão `index` é a página inicial do LikeC4 (`view index`) e representa o C4 System Context. Ela utiliza `include *`, que seleciona **os elementos de topo** e **deriva as relações do sistema** a partir das interações com seus contêineres internos.

| Elemento visível | Fronteira | Papel |
| --- | --- | --- |
| **Operador de estoque** | Pessoa externa | Cadastra, movimenta e consulta. |
| **Gestor de estoque** | Pessoa externa | Consulta críticos e configura mínimos. |
| **Sistema de Gestão de Estoque** | Sistema sob análise | Mantém produtos, saldos, movimentações e solicita alertas. |
| **Sistema de Vendas** | Sistema externo | Solicita baixa por venda. |
| **Provedor de Notificações** | Sistema externo | Recebe pedidos de envio de alertas. |

As relações de negócio são **Operador → Estoque**, **Gestor → Estoque**, **Vendas → Estoque** e **Estoque → Notificações**. Não aparecem web, API, worker, banco, classes ou protocolos internos, como no [diagrama Mermaid de contexto](../docs/01-contexto.md).

**Detalhe de implementação:** essas relações em nível de sistema são **inferidas**, não declaradas em duplicidade. Por exemplo, `operador -> estoque.web` no modelo é apresentado no nível 1 como uma interação com `estoque`. Os rótulos podem ser agregados ou simplificados pelo mecanismo de projeção do LikeC4; o conteúdo funcional completo permanece descrito nos capítulos Mermaid.

## Nível 2: Contêineres (`conteineres`)

**Pergunta:** que aplicações e dados estão **dentro do sistema** e como se comunicam?

A visão `conteineres` tem escopo `of estoque`. Nesse escopo, `include *` traz os quatro contêineres imediatos e os participantes externos ligados a eles; o sistema central permanece a fronteira, não se converte em outro executável.

| Elemento dentro de `estoque` | Tecnologia | Responsabilidade |
| --- | --- | --- |
| `estoque.web` — Aplicação Web | SPA, framework não definido | Operações humanas e consultas. |
| `estoque.api` — API de Estoque | ASP.NET Core / C# (.NET 10) | Regras e transações de estoque. |
| `estoque.worker` — Worker de Notificações | .NET Worker Service / C# | Consumo posterior da outbox e solicitação de alertas. |
| `estoque.banco` — Banco de Dados | PostgreSQL | Saldo, movimentações, referência de origem e outbox. |

São preservadas as **sete relações direcionais em nível de contêiner** do [nível 2 Mermaid](../docs/02-containers.md). Três delas são agregações das relações detalhadas entre [componentes da API](visao-componentes.md), sem duplicação no modelo:

| Origem → destino | Mecanismo informado no modelo |
| --- | --- |
| Operador → Web | HTTPS |
| Gestor → Web | HTTPS |
| Web → API | JSON/HTTPS |
| Sistema de Vendas → API | JSON/HTTPS |
| API → PostgreSQL | PostgreSQL/TCP |
| Worker → PostgreSQL | PostgreSQL/TCP |
| Worker → Provedor de Notificações | API externa, contrato a definir |

**Não há relação API → Worker.** A API persiste a intenção de notificar na outbox durante a transação; o worker consulta posteriormente o mesmo PostgreSQL. Não foi introduzido broker, API gateway, cache ou microsserviço. As tecnologias associadas às relações representam **escolhas de referência**.

## Como navegar

A experiência LikeC4 oferece **drill-down**: ao abrir a visão inicial `index` e selecionar o Sistema de Gestão de Estoque, a propriedade `navigateTo conteineres` leva à visão dos quatro contêineres.

Na raiz do repositório, com Node.js 22:

```bash
npm install
npm run likec4:validate
npm run likec4:dev
```

O servidor local abre normalmente na porta **5173**. Selecione `index` para contexto e `conteineres` para contêineres. Os arquivos `.c4` **não** são renderizados como imagens diretamente no GitHub; a publicação e exportação de prévias permanentes estão previstas para a **etapa 5** da trilha.

O workflow [Documentation Quality](../.github/workflows/docs-quality.yml) verifica o modelo LikeC4 por meio de `npm run likec4:validate`. Como essa verificação não substitui uma inspeção visual do layout, revise também as duas vistas na interface local.

## Comparação de fronteiras com Mermaid

| Critério | Mermaid nível 1 / LikeC4 `index` | Mermaid nível 2 / LikeC4 `conteineres` |
| --- | --- | --- |
| Sistema central | Uma unidade abstrata | A mesma fronteira contendo quatro contêineres |
| Atores | Dois atores humanos externos | Os mesmos dois atores externos |
| Integrações | Sistema de Vendas e Provedor externos | Os mesmos sistemas, conectados à API e ao worker |
| Banco | Não aparece | PostgreSQL, dentro da fronteira |
| Comunicação | Relações de negócio agregadas | Sete relações técnicas direcionais |
| Código C# e componentes | Não aparece | Não aparece |

No LikeC4, `index` e `conteineres` são **projeções de um mesmo grafo**. No Mermaid, os dois diagramas são blocos independentes mantidos como documentação. As duas abordagens coexistem para comparação didática; não existe geração automática de uma a partir da outra nesta etapa.

O fio condutor segue sendo a baixa de **10 unidades do SKU-001** (saldo **15 → 5**, mínimo **5**) e o registro atômico da outbox. A sequência detalhada permanece em [fluxo de movimentação](../docs/fluxo-movimentacao.md).

## Limitações e próximas etapas

Esta visão não expõe componentes internos da API nem classes, endpoints, diagramas dinâmicos ou deployment. A [etapa 3 do LikeC4](visao-componentes.md) abre a API no nível 3 e preserva o `classDiagram` Mermaid como nível 4. A etapa 4 cobrirá os fluxos; a etapa 5 configurará exportação, publicação e revisão final.

### Referências

- [LikeC4: Views](https://likec4.dev/dsl/views/)
- [LikeC4: View Predicates](https://likec4.dev/dsl/views/predicates/)
- [LikeC4: Relationships](https://likec4.dev/dsl/relationships/)
- [Modelo C4](https://c4model.com/)
