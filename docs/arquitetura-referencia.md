# Arquitetura de referência

## 1. Natureza do desenho

Esta é uma **arquitetura hipotética para ensino do C4**, não a descrição de um serviço implementado. Escolhemos poucos elementos e um único caso de uso para manter os quatro níveis coerentes.

**Sistema sob análise:** Sistema de Gestão de Estoque. Consulte os diagramas [nível 1: Contexto](01-contexto.md), [nível 2: Contêineres](02-containers.md), [nível 3: Componentes da API](03-componentes.md) e [nível 4: Código](04-codigo.md).

## 2. Contêineres previstos

No C4, **contêiner** significa unidade executável ou de armazenamento, e não necessariamente contêiner Docker.

| Contêiner | Tecnologia de referência | Responsabilidade |
| --- | --- | --- |
| **Aplicação Web** | SPA web (framework não definido) | Interface para cadastro, consulta e movimentação manual. |
| **API de Estoque** | ASP.NET Core, C# / .NET 10 | Expor operações, executar casos de uso e aplicar regras de negócio. |
| **Worker de Notificações** | .NET Worker Service / C# | Consultar solicitações pendentes e enviá-las ao provedor externo, com tentativas controladas. |
| **Banco de Dados** | PostgreSQL | Persistir produtos, saldos, movimentações, idempotência e outbox. |

### Dependências externas

- **Sistema de Vendas:** chama a API para solicitar baixa de estoque.
- **Provedor de Notificações:** recebe solicitações de envio feitas pelo worker.

**Decisão intencional:** não adicionar broker de mensagens nesta versão. O worker lê uma outbox persistida no PostgreSQL. Isso simplifica o exemplo sem acoplar a transação de estoque à disponibilidade do provedor.

## 3. Responsabilidades dentro da API (detalhadas no nível 3)

- **Interface de entrada:** endpoints HTTP para interface web e sistema de vendas.
- **Aplicação:** casos de uso `RegistrarEntrada`, `RegistrarSaida`, `ConsultarSaldo` e `ConsultarMovimentacoes`.
- **Domínio:** regras de saldo, limite mínimo e movimentação; sem dependência de transporte ou banco.
- **Infraestrutura:** mapeamento de persistência, controle de concorrência e implementação dos repositórios.

O [diagrama de componentes da API](03-componentes.md) apresenta Endpoints HTTP, Movimentações de Estoque, Gestão e Consultas, Regras de Estoque e Persistência Transacional. A organização é **modular em um único serviço**, com separação lógica inspirada em DDD e arquitetura hexagonal. Não pressupõe microsserviços nem projetos .NET separados para cada camada.

## 4. Modelo conceitual de domínio (base para nível 4)

| Conceito | Papel |
| --- | --- |
| **Produto** | Cadastro com ID, SKU, descrição e limite mínimo. |
| **EstoqueDoProduto** | Agregado responsável pelo saldo e pelas operações de entrada/saída. |
| **MovimentacaoDeEstoque** | Registro imutável de entrada ou saída associado ao produto. |
| **ReferenciaDeOrigem** | Chave que permite deduplicar solicitações externas. |
| **NotificacaoPendente** | Item da outbox para processamento assíncrono. |

O [nível 4](04-codigo.md) detalha um recorte de classes da saída de estoque, incluindo `RegistrarSaidaUseCase`, `EstoqueDoProduto` e `IRegistroSaidaTransacional`. Esses conceitos **não implicam** que um agregado mantenha todo o histórico de movimentações em memória; os registros podem ser persistidos separadamente na mesma transação.

## 5. Fluxo principal: baixa de 10 unidades

A [sequência da movimentação](fluxo-movimentacao.md) explicita a ordem de execução, a fronteira do commit e o envio eventual do alerta.

1. **Aplicação Web ou Sistema de Vendas → API:** solicita saída de 10 unidades.
2. **API:** valida entrada e idempotência; aplica regras do domínio.
3. **API → PostgreSQL:** realiza uma operação transacional que protege o saldo contra concorrência, registra a movimentação e, se necessário, cria item de outbox.
4. **API → solicitante:** informa sucesso ou rejeição de negócio.
5. **Worker → PostgreSQL:** consulta itens pendentes da outbox.
6. **Worker → Provedor de Notificações:** solicita envio de alerta; atualiza status/tentativas da outbox.

### Consistência e concorrência

A consulta inicial de saldo **não é suficiente** para garantir segurança concorrente. A implementação ilustrativa deverá usar transação e atualização condicional/bloqueio compatível com PostgreSQL, ou controle de versão com tratamento de conflito. O registro da movimentação e a mudança do saldo precisam pertencer à **mesma transação**.

Uma chamada repetida do sistema de vendas deve ser reconhecida por uma referência externa única no escopo da origem. A identificação da repetição também precisa ser assegurada no banco por restrição de unicidade e operação transacional, não somente por verificação prévia na API.

### Tratamento de alertas

O registro de outbox nasce na transação que cruza o estoque mínimo. O worker executa tentativas e guarda o resultado. Uma entrega a sistemas externos pode ser **pelo menos uma vez**; portanto, deduplicação no destinatário ou identificador de mensagem são desejáveis. Não é feita promessa de entrega exatamente uma vez.

## 6. Como ler os quatro níveis

| Nível | O que será detalhado | O que não aparecerá |
| --- | --- | --- |
| **1. Contexto** | Atores, sistema de estoque e integrações externas. | API, worker, banco e classes internas. |
| **2. Contêineres** | Web, API, worker, PostgreSQL e relações entre eles. | Classes, métodos e detalhes de implementação. |
| **3. Componentes** | Partes **internas da API** e seus relacionamentos. | Todas as classes do domínio e detalhes internos do worker. |
| **4. Código** | Classes e interfaces que concretizam a **saída de estoque na API**. | Todas as classes de uma aplicação hipotética. |

A progressão deve manter o mesmo limite de sistema, nomes e fluxo de negócio. Veja o [guia de modelagem](guia-c4.md) e as [decisões](decisoes-arquiteturais.md).
