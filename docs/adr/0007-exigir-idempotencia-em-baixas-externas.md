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

## Decision Drivers

- Tornar retries do Sistema de Vendas seguros quando respostas são perdidas.
- Distinguir repetição legítima de reutilização incorreta da mesma chave com outros dados.
- Persistir a identidade da operação para funcionar após reinício ou com múltiplas instâncias.

## Alternatives Considered

- **Deduplicação em memória:** frágil contra reinício e concorrência entre instâncias.
- **Consulta prévia sem restrição única:** mantém janela de corrida entre leitura e escrita.
- **Chave (Origem, ReferenciaExterna) persistida e única (proposta):** exige comparação do payload antes de reutilizar resultado.

## Risks

- Chave já confirmada com mesmo produto, quantidade e origem recupera o resultado, sem nova baixa/outbox.
- Chave reutilizada com payload divergente é conflito, nunca um segundo débito ou sucesso reutilizado.
- Uma nova consulta após bloquear o produto em `READ COMMITTED` evita leituras antigas para a mesma mercadoria; a restrição única cobre também a disputa entre produtos distintos.
- Em violação de unicidade durante o INSERT, a transação perdedora deve fazer rollback, reler o registro vencedor e comparar os dados.
- Retenção de chaves e idempotência de operações rejeitadas seguem como **questões abertas**.

## References

- [Cenários alternativos da movimentação](../fluxo-movimentacao.md)
- [Unicidade e tratamento de concorrência](../../examples/persistencia-transacional.md)
