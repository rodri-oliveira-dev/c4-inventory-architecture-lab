# LikeC4: fluxos dinâmicos de movimentação e outbox (etapa 4)

> **Pergunta:** em que ordem o sistema confirma a saída de estoque e, depois, processa a notificação?

A etapa 4 do LikeC4 adiciona duas visões dinâmicas em [`dynamics.c4`](dynamics.c4) que utilizam os **mesmos participantes definidos em [`model.c4`](model.c4)**. Uma *dynamic view* é uma representação temporal complementar às visões estruturais de [Contexto e Contêineres](visoes-contexto-conteineres.md) e [Componentes da API](visao-componentes.md), e **não** corresponde a um quinto nível C4.

As visões são exibidas na variante `sequence`, compatível com participantes que não contêm elementos filhos. Por isso o fluxo usa componentes internos da API, o banco, o worker e os sistemas externos, **não** o contêiner `estoque.api` como uma linha de vida.

## 1. `registrarSaida`: baixa e confirmação síncrona

O Sistema de Vendas solicita a baixa de **10 unidades de `SKU-001`**, cujo saldo inicial é **15** e estoque mínimo **5**. O resultado é **saldo 5** e a intenção de alerta gravada na outbox.

| Momento | Participantes LikeC4 | Consequência |
| --- | --- | --- |
| Entrada | `vendas → estoque.api.http → estoque.api.movimentacoes` | A solicitação informa quantidade, produto, origem e referência `V-100`. |
| Acesso protegido | `movimentacoes → persistencia → banco` | A transação inicia, bloqueia o registro do produto e reconsulta a chave externa. |
| Decisão de domínio | `persistencia → regras` | Com o saldo **já protegido**, a regra retorna o plano **15 → 5**, com `DeveNotificar=true`. |
| Escrita | `persistencia → banco` | Saldo, movimentação, unicidade da referência e outbox pertencem à **mesma transação**. |
| Confirmação | `banco → persistencia → movimentacoes → http → vendas` | O resultado `SaidaRegistrada` só é devolvido **depois do COMMIT**. |

O domínio não bloqueia registros SQL nem abre transações. A visão apresenta a execução da regra enquanto a persistência mantém o estado protegido, conforme o contrato ilustrativo `IRegistroSaidaTransacional`. O fato de uma chamada `persistencia → regras` aparecer no **fluxo temporal** não significa que o domínio dependa da infraestrutura: trata-se da invocação do callback `planejar` enquanto o adaptador mantém o bloqueio, como descrito no [nível 4](../docs/04-codigo.md).

**Saída não significa notificação entregue.** `AlertaRegistrado=true` indica somente a existência de uma notificação **pendente na outbox**. Não há chamada direta API → Worker ou API → Provedor.

### Alternativas importantes

A visão `registrarSaida` representa **o caminho de sucesso**, mantendo legível a sequência da transação. Os caminhos alternativos permanecem documentados com detalhes no [fluxo Mermaid original](../docs/fluxo-movimentacao.md):

| Situação | Resultado correto |
| --- | --- |
| Mesma origem, referência e payload já confirmados | Retorna resultado persistido, **sem segundo débito ou segunda outbox**. |
| Mesma referência, mas produto ou quantidade divergentes | Conflito; nenhuma nova baixa. |
| Saldo insuficiente, como 8 para uma saída de 10 | Rejeição sem mutação ou outbox. |
| Duas saídas **distintas** de 10 contra saldo 15 | Uma confirma; a outra observa saldo 5 após o lock e é rejeitada. |
| Falha na gravação da outbox antes do commit | **Rollback** de saldo, histórico e referência. |

Além da reconsulta de idempotência após o lock, uma **restrição única** de `(Origem, ReferenciaExterna)` cobre corridas, inclusive entre produtos distintos. Em caso de conflito na restrição, a transação perdedora faz rollback e relê o resultado vencedor para comparar o payload. A implementação e os testes de integração continuam fora do escopo documental.

## 2. `entregarAlerta`: outbox e entrega eventual

Depois que a baixa é confirmada, o **Worker de Notificações** consulta a outbox no mesmo PostgreSQL e faz uma solicitação de envio ao **Provedor de Notificações**. A visão contém alternativas `when` e `else`:

- **Confirmação:** o provedor confirma o processamento e o worker atualiza o item da outbox.
- **Falha, timeout ou confirmação perdida:** o worker registra a tentativa e mantém o item elegível para uma nova execução. A ausência de resposta **não** é desenhada como resposta enviada pelo provedor.

O saldo permanece **5**, independentemente do resultado do envio. A entrega é **eventual**, e um timeout pode levar ao reenvio de uma mensagem já processada externamente. O identificador estável só possibilita deduplicação se o provedor oferecer essa capacidade. **Não há garantia de exactly once** entre banco e sistema externo.

A reivindicação concorrente de itens da outbox, os limites de tentativas, o tratamento de falhas permanentes e a observabilidade ainda dependeriam de especificação numa implementação real.

## 3. Comparação com Mermaid

| Critério | Mermaid (`docs/fluxo-movimentacao.md`) | LikeC4 (`dynamics.c4`) |
| --- | --- | --- |
| Fonte dos participantes | Nomes declarados em cada `sequenceDiagram`. | IDs reutilizados do modelo arquitetural único. |
| Baixa síncrona | Mensagens com endpoints, aplicação, persistência, domínio e banco. | Sequência equivalente com elementos já presentes nos níveis 1–3. |
| Outbox | Separação explícita após o commit, com alternativas. | Outra `dynamic view`, com `variant sequence` e `alt`. |
| Casos alternativos da baixa | Documentados na tabela de situações. | Também documentados na tabela acima, sem poluir o fluxo principal. |
| Saída renderizada no GitHub | Mermaid embutido no Markdown. | Fonte LikeC4 em `.c4`; prévia local no LikeC4 e exportação prevista para a etapa 5. |

Os diagramas descrevem a mesma arquitetura de referência, **não dois sistemas diferentes**. As mensagens em `dynamic view` representam um caso de uso e não acrescentam relações estáticas nem elementos ao `model.c4`. O Worker nunca altera saldos, e o provedor de notificações não é chamado por componentes da API.

## 4. Executar e validar

Na raiz do projeto, com Node.js 22:

```bash
npm install
npm run likec4:validate
npm run likec4:dev
```

Abra as visões `registrarSaida` e `entregarAlerta` no navegador do LikeC4. O workflow [Documentation Quality](../.github/workflows/docs-quality.yml) valida a DSL, mas **não exporta imagens LikeC4** nesta etapa. A inspeção visual ainda é recomendada e a exportação automatizada é parte da **etapa 5**.

### Decisões relacionadas

- [ADR 0003: PostgreSQL](../docs/adr/0003-adotar-postgresql-transacional.md)
- [ADR 0004: Worker separado](../docs/adr/0004-separar-worker-de-notificacoes.md)
- [ADR 0005: Outbox sem broker](../docs/adr/0005-adotar-outbox-sem-broker.md)
- [ADR 0006: Concorrência](../docs/adr/0006-proteger-concorrencia-no-saldo.md)
- [ADR 0007: Idempotência](../docs/adr/0007-exigir-idempotencia-em-baixas-externas.md)

Os ADRs permanecem **Proposed** e o projeto continua um laboratório sem aplicação executável.

### Referências

- [LikeC4: Dynamic Views](https://likec4.dev/dsl/views/dynamic/)
- [Modelo C4: Dynamic Diagram](https://c4model.com/diagrams/dynamic)
