# Proteger o saldo de estoque contra atualizações concorrentes

## Status

Proposed

## Context

Uma saída de 10 unidades deve ser recusada quando a quantidade disponível não for suficiente. Duas solicitações simultâneas podem ler o mesmo saldo e ambas tentar debitá-lo. Uma verificação feita somente em memória, antes de atualizar o banco, não previne perda de atualização nem saldo negativo.

## Decision

Exigir que a atualização de saldo e o registro da movimentação ocorram na mesma transação do PostgreSQL, com proteção de concorrência no banco. A implementação ilustrativa escolherá uma estratégia explícita, como atualização condicional baseada no saldo ou bloqueio de linha, e tratará conflitos como resultado esperado da operação.

## Consequences

Essa invariável torna possível demonstrar por que consistência e atomicidade importam no caso de uso de saída de 10 unidades. Uma operação que não conseguir reservar saldo suficiente não produzirá movimentação ou item de outbox.

Há custo de contenção sobre o mesmo produto e necessidade de tratar conflitos e retries com cuidado. A escolha entre atualização condicional e bloqueio será demonstrada no nível 4; a garantia depende de implementação e testes transacionais reais.
