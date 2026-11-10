# Exigir idempotência em solicitações externas de baixa

## Status

Proposed

## Context

O sistema de vendas pode repetir a mesma solicitação após timeout, falha de rede ou retry automático. Se cada chamada for tratada como uma nova movimentação, o produto poderá ser debitado mais de uma vez, embora haja apenas uma venda. Consideramos detectar duplicidade apenas na API ou persistir uma identidade da operação de origem.

## Decision

Exigir uma referência externa estável para baixas iniciadas pelo sistema de vendas, única dentro do escopo da origem. A API deve persistir e verificar essa identidade na mesma operação transacional que atualiza o saldo, com restrição de unicidade no PostgreSQL. Repetições reconhecidas não geram nova baixa.

## Consequences

Retries da mesma operação passam a ter comportamento previsível e não duplicam movimentações. O fluxo transversal de saída de 10 unidades poderá demonstrar tanto a primeira baixa quanto a sua repetição segura.

O contrato de integração deve distinguir repetição idêntica de reutilização indevida da mesma chave com dados diferentes; erros, concorrência e retenção das chaves exigem decisões explícitas. Idempotência não elimina a necessidade de controle de concorrência do saldo.
