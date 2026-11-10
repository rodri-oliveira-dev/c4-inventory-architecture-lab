# Adotar outbox transacional sem broker de mensagens

## Status

Proposed

## Context

Um alerta de estoque mínimo não deve desaparecer entre a confirmação de uma baixa e a comunicação com o provedor de notificações. O fluxo precisa preservar atomicidade entre a movimentação e o registro da intenção de alertar. Consideramos chamada síncrona ao provedor, publicação direta em um broker e uma outbox persistida no mesmo banco das movimentações.

## Decision

Persistir uma notificação pendente em uma tabela de outbox no PostgreSQL, na mesma transação que atualiza saldo e histórico. O worker consulta a outbox e solicita envio ao provedor. Não introduzir broker externo nesta versão didática.

## Consequences

A criação da intenção de notificar acompanha a transação do estoque e simplifica a demonstração da consistência. A ausência de broker reduz os contêineres e ferramentas necessários.

O worker terá de administrar polling, tentativas, atrasos e itens presos. Uma notificação poderá ser enviada mais de uma vez em falhas de confirmação; a integração deve tratar deduplicação quando disponível. A estratégia não garante entrega exatamente uma vez.

## Decision Drivers

- Confirmar a intenção de alerta junto da movimentação que cruzou o estoque mínimo.
- Evitar chamada ao provedor de notificações dentro da transação de saldo.
- Manter a topologia didática sem broker externo.

## Alternatives Considered

- **Chamada direta ao provedor:** cria janela entre efeitos externos e confirmação da movimentação.
- **Publicação direta em broker:** ainda exige integração com as garantias da transação e acrescenta infraestrutura.
- **Outbox no PostgreSQL (proposto):** persiste a intenção de envio atomicamente e permite consumo posterior.

## Risks

- O evento lógico de alerta surge apenas quando o saldo cruza de **acima** do mínimo para **igual ou abaixo**; retry idempotente não deve gerar outra outbox.
- O worker precisa de reivindicação segura, polling, orçamento de retries e tratamento de itens presos, sem bloquear a API.
- Falha entre o provedor processar e a gravação do resultado pode causar reenvio. Um identificador estável ajuda somente quando o destinatário suporta deduplicação.
- Não há garantia de *exactly once* entre PostgreSQL e provedor externo.

## References

- [Sequência de outbox e cenários de falha](../fluxo-movimentacao.md)
