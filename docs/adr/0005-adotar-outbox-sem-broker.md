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
