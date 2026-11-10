# LikeC4: Componentes da API de Estoque (etapa 3)

> **Pergunta:** quais componentes organizam a API de Estoque, quais responsabilidades possuem e como colaboram com os contêineres externos à API?

Esta é a visão **C4 nível 3 (Components)** da mesma arquitetura hipotética já documentada em [Mermaid](../docs/03-componentes.md). O LikeC4 usa o modelo em [`model.c4`](model.c4), com a visão `componentes` declarada em [`views.c4`](views.c4). Não há uma segunda cópia dos componentes nem uma implementação de API em execução.

A fronteira desta visão é **somente** `estoque.api`, contêiner ASP.NET Core / C# (.NET 10). A Aplicação Web, o Sistema de Vendas, o PostgreSQL e o Worker aparecem **fora da API** como colaboradores. O Provedor de Notificações não está desenhado neste zoom porque é acionado pelo **Worker**, não pelos componentes da API.

## Os cinco componentes

| Identificador LikeC4 | Responsabilidade | Papel no desenho |
| --- | --- | --- |
| `estoque.api.http` | Receber solicitações, validar contratos de entrada e chamar casos de uso. | **Endpoints HTTP**, ASP.NET Core |
| `estoque.api.movimentacoes` | Orquestrar `RegistrarEntrada` e `RegistrarSaida`, incluindo a identidade da operação externa. | **Movimentações de Estoque**, aplicação |
| `estoque.api.gestao` | Cadastrar produtos, consultar saldos e configurar estoques mínimos. | **Gestão e Consultas**, aplicação |
| `estoque.api.regras` | Aplicar invariantes de quantidade, disponibilidade e cruzamento do estoque mínimo. | **Regras de Estoque**, domínio |
| `estoque.api.persistencia` | Coordenar transação, controle de concorrência, chave única, movimentação e gravação da outbox. | **Persistência Transacional**, infraestrutura |

O agrupamento corresponde aos cinco componentes do [diagrama Mermaid nível 3](../docs/03-componentes.md). Um *componente* representa um agrupamento lógico de responsabilidades, **não** um microsserviço, processo separado, assembly obrigatório ou classe.

## Relacionamentos e direção

| Origem → destino | Propósito |
| --- | --- |
| Web → Endpoints HTTP | Consultas e operações, via JSON/HTTPS |
| Sistema de Vendas → Endpoints HTTP | Solicitar baixa com referência externa, via JSON/HTTPS |
| Endpoints HTTP → Movimentações | Encaminhar entradas e saídas |
| Endpoints HTTP → Gestão e Consultas | Encaminhar cadastros e consultas |
| Movimentações → Regras | Aplicar invariantes de estoque |
| Gestão e Consultas → Regras | Aplicar regras de produto e mínimo |
| Movimentações → Persistência | Confirmar saldo, movimentação e eventual outbox |
| Gestão e Consultas → Persistência | Consultar e persistir informações de produtos |
| Persistência → PostgreSQL | Ler e gravar dados em transação |
| Worker → PostgreSQL | Consumir e atualizar o estado da outbox, **posteriormente** |

Os **nove vínculos envolvendo os componentes** (dois de entrada, seis entre componentes e um de saída para o banco) estão definidos uma só vez em `model.c4`. O relacionamento **Worker → PostgreSQL** já existe desde a fundação e aparece no nível 3 para esclarecer que o consumo da outbox não passa pela API.

**Atenção:** entre componentes, as setas indicam dependência **lógica**, e não requisições de rede. O banco é acessado pelo adaptador de persistência; o domínio não possui dependência SQL. O worker não altera saldo nem histórico de movimentações.

## O que acontece nos níveis anteriores?

A etapa 2 já apresentava **sete relações no nível de contêineres**. A etapa 3 especializa três delas, preservando seu significado agregado:

| Relação vista no nível 2 | Relação autoritativa no modelo |
| --- | --- |
| Web → API | `estoque.web → estoque.api.http` |
| Vendas → API | `vendas → estoque.api.http` |
| API → Banco | `estoque.api.persistencia → estoque.banco` |

As outras quatro relações de nível 2 permanecem: Operador → Web, Gestor → Web, Worker → Banco e Worker → Provedor.

O LikeC4 **agrega relações dos filhos** quando os níveis superiores ocultam os componentes. Portanto, não adicionamos simultaneamente `web → api` e `web → api.http`, evitando uma segunda declaração da mesma comunicação. A visão `index` continua representando o sistema central com seus atores e integrações, sem mostrar a estrutura interna.

## Como navegar nas visões

Na raiz do repositório, com Node.js 22:

```bash
npm install
npm run likec4:validate
npm run likec4:dev
```

As vistas disponíveis são `index` (Contexto), `conteineres` (Contêineres) e `componentes` (Componentes da API). Na navegação do LikeC4: **Contexto → Sistema de Gestão de Estoque → Contêineres → API de Estoque → Componentes**.

O modelo LikeC4 é verificado no [Documentation Quality](../.github/workflows/docs-quality.yml). A validação da DSL **não confirma por si só** o acabamento visual; a geração de previews publicáveis fica para a etapa 5.

## O mesmo exemplo: saldo 15 → 5

Uma saída de **10 unidades** para `SKU-001`, com saldo inicial **15** e mínimo **5**, percorre:

1. Sistema de Vendas → Endpoints HTTP → Movimentações de Estoque.
2. Movimentações de Estoque → Regras de Estoque, para validar a quantidade e calcular o cruzamento do mínimo.
3. Movimentações de Estoque → Persistência Transacional, para proteger concorrência, verificar idempotência por `(Origem, ReferenciaExterna)` e confirmar saldo **5**, histórico e item da outbox **na mesma transação**.
4. Depois do commit, a API responde ao solicitante. O Worker, em outro momento, acessa o PostgreSQL e solicita o envio do alerta ao Provedor de Notificações.

Essa descrição é **conceitual**: a implementação transacional deve carregar o saldo sob bloqueio ou outra proteção adequada **antes** de aplicar `PlanejarSaida`. Consulte o [nível 4](../docs/04-codigo.md) e o [fluxo de sequência](../docs/fluxo-movimentacao.md) para as garantias e alternativas. Nenhum componente realiza envio síncrono ao provedor.

## E o nível 4 (Code)?

O [diagrama de classes `classDiagram`](../docs/04-codigo.md) permanece no **Mermaid**, junto dos [exemplos C# ilustrativos](../examples/registrar-saida.md). O LikeC4 foi utilizado para os níveis **1, 2 e 3**, mas não para substituir UML de classes, atributos e assinaturas de método. Esta divisão é intencional e não deixa o nível 4 sem documentação.

## Próximas etapas

- **Etapa 4:** usar visões dinâmicas LikeC4 para a confirmação síncrona de `RegistrarSaida` e o processamento eventual do alerta.
- **Etapa 5:** automatizar exportação e publicação, revisar visualmente e comparar as duas abordagens sem perder a fonte única do modelo LikeC4.

### Referências

- [LikeC4: Scoped Views](https://likec4.dev/dsl/views/)
- [LikeC4: View Predicates](https://likec4.dev/dsl/views/predicates/)
- [Modelo C4: Component Diagram](https://c4model.com/diagrams/component)
