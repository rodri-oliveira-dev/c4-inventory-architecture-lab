# Adotar PostgreSQL como armazenamento transacional de estoque

## Status

Proposed

## Context

Entradas e saídas modificam saldos, precisam produzir histórico auditável e não podem gerar estoque negativo. A API deve registrar mudanças de saldo, movimentações, referências externas e alertas pendentes de modo consistente. Consideramos persistências independentes para cada necessidade, mas isso exigiria coordenação de alterações entre armazenamentos.

## Decision

Adotar PostgreSQL como banco relacional de referência. Armazenar produtos, saldos, movimentações, chaves de idempotência e registros de outbox sob a mesma fronteira transacional, com acesso de escrita centralizado na API. Consultas do worker à outbox são uma exceção delimitada para processamento de notificações.

## Consequences

Transações e restrições de unicidade oferecem meios concretos para manter saldo, histórico e deduplicação coerentes, além de permitir uma explicação precisa de concorrência no nível 4.

O banco se torna dependência crítica para operações e processamento de alertas. Será necessário pensar em índices, contenção por produto, evolução de schema, cópias de segurança e recuperação. O desenho não promete desempenho sem testes reais.

## Decision Drivers

- Gravar saldo, histórico, referência de origem e eventual outbox em uma unidade atômica.
- Proteger consistência do saldo e unicidade de operações externas diante de concorrência.
- Evitar coordenação de escrita entre armazenamentos diferentes num laboratório didático.

## Alternatives Considered

- **Persistências separadas por finalidade:** isolariam responsabilidades, mas exigiriam coordenação e reconciliação para efeitos de uma única baixa.
- **Estado em memória com persistência posterior:** útil para protótipos, mas insuficiente para durabilidade e concorrência.
- **PostgreSQL transacional (proposto):** restrições e transações atendem às invariantes sem distribuir os dados.

## Risks

- O banco torna-se dependência crítica da API e do worker; a permissão do worker deve se limitar ao estado operacional da outbox.
- Índices, locks, backups, recuperação e contenção precisam ser projetados e testados antes de qualquer operação real.
- Uma transação confirmada significa baixa persistida, não alerta entregue ao destinatário.

## References

- [Fluxo de movimentação e fronteira transacional](../fluxo-movimentacao.md)
- [Contrato de persistência](../../examples/persistencia-transacional.md)
