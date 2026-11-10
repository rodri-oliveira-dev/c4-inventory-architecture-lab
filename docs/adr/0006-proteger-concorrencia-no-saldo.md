# Proteger o saldo de estoque contra atualizações concorrentes

## Status

Proposed

## Context

Uma saída de 10 unidades deve ser recusada quando a quantidade disponível não for suficiente. Duas solicitações simultâneas podem ler o mesmo saldo e ambas tentar debitá-lo. Uma verificação feita somente em memória, antes de atualizar o banco, não previne perda de atualização nem saldo negativo.

## Decision

Exigir que a atualização de saldo e o registro da movimentação ocorram na mesma transação do PostgreSQL, com proteção de concorrência no banco. A implementação ilustrativa escolherá uma estratégia explícita, como atualização condicional baseada no saldo ou bloqueio de linha, e tratará conflitos como resultado esperado da operação.

## Consequences

Essa invariável torna possível demonstrar por que consistência e atomicidade importam no caso de uso de saída de 10 unidades. Uma operação que não conseguir reservar saldo suficiente não produzirá movimentação ou item de outbox.

Há custo de contenção sobre o mesmo produto e necessidade de tratar conflitos e retries com cuidado. O nível 4 ilustra bloqueio pessimista como uma possibilidade, sem descartar atualização condicional; a garantia ainda depende de implementação e testes transacionais reais.

## Decision Drivers

- Impedir saldos negativos mesmo quando saídas distintas começam com a mesma disponibilidade.
- Confirmar saldo, histórico e eventual outbox na mesma fronteira transacional.

## Alternatives Considered

- **Validação apenas em memória:** insuficiente contra leituras simultâneas.
- **UPDATE SQL condicional atômico:** alternativa viável, mas precisa integrar o cálculo do cruzamento e verificar linhas afetadas.
- **Bloqueio pessimista por produto (ilustrado):** `SELECT ... FOR UPDATE` dentro da transação, antes de `PlanejarSaida`.

## Risks

- Transações longas ampliam contenção, latência e chance de deadlocks; devem ser curtas e ter tratamento de conflitos.
- O domínio calcula o plano, mas não implementa isolamento. O estado usado em `PlanejarSaida` precisa ser lido sob proteção transacional.
- Para saldo inicial 15 e duas saídas distintas de 10, no máximo uma confirma; a outra deve observar saldo 5 e ser rejeitada.
- O desenho não substitui testes concorrentes com PostgreSQL real.

## References

- [Sequência síncrona e cenários de concorrência](../fluxo-movimentacao.md)
- [Contrato de bloqueio](../../examples/persistencia-transacional.md)
