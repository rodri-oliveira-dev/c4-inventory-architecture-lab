# Contrato de persistência: concorrência, idempotência e outbox

Este capítulo complementa o [nível 4: Código](../docs/04-codigo.md) e o [exemplo C# de `RegistrarSaida`](registrar-saida.md). **Não é uma implementação de banco, uma migration ou SQL de produção**: descreve quais garantias uma implementação de `IRegistroSaidaTransacional` precisa oferecer.

## 1. Invariantes que pertencem à transação

Ao registrar uma saída confirmada, a implementação precisa persistir na **mesma transação PostgreSQL**:

1. o novo saldo de `EstoqueDoProduto`;
2. uma `MovimentacaoDeEstoque` auditável com origem/referência quando houver;
3. um item de `NotificacaoPendente` na outbox **somente quando** `PlanoSaida.DeveNotificar` for verdadeiro.

**Tudo ou nada:** se qualquer parte falhar antes do commit, as demais mudanças devem ser desfeitas. O envio real ao provedor é realizado pelo **Worker**, fora dessa transação.

## 2. Exclusão mútua por produto e regra de domínio

A estratégia ilustrativa usa **bloqueio pessimista por produto** dentro de transação:

```sql
-- Trecho ilustrativo, NÃO uma migration completa
BEGIN;

SELECT saldo, estoque_minimo
  FROM estoque_do_produto
 WHERE produto_id = @produto_id
 FOR UPDATE;

-- Com o saldo agora bloqueado:
-- 1. Validar a chave de origem/idempotência.
-- 2. Hidratar EstoqueDoProduto a partir desta leitura.
-- 3. Invocar PlanejarSaida(quantidade).
-- 4. Atualizar o saldo; inserir movimentação e outbox.
-- 5. Somente então confirmar COMMIT.
```

O bloqueio deve permanecer até o **commit ou rollback**. Em `READ COMMITTED`, aguardar o bloqueio de outro escritor obriga a ler o estado atualizado na operação seguinte. Para o cenário **saldo 15, duas saídas distintas de 10**, apenas a primeira poderá reduzir o saldo para 5. A outra observará 5 e falhará por insuficiência.

Uma leitura de saldo **antes** de abrir a transação não constitui a fonte autoritativa para `PlanejarSaida`; o callback da porta deve receber o `EstoqueDoProduto` hidratado com o saldo lido **sob bloqueio**.

## 3. Idempotência de integrações de vendas

O par `(origem, referencia_externa)` deve identificar **uma única operação externa** persistida. Um índice único parcial é uma alternativa ilustrativa quando a referência pode ser nula para baixas manuais:

```sql
-- Esquema ilustrativo, nomes a adaptar à modelagem definitiva
CREATE UNIQUE INDEX uq_movimentacao_origem_referencia
    ON movimentacao_estoque (origem, referencia_externa)
 WHERE referencia_externa IS NOT NULL;
```

Uma consulta prévia de duplicidade **não basta**, porque duas transações podem observar ausência ao mesmo tempo. Para evitar uma segunda baixa, o adaptador precisa:

1. Consultar se a chave já existe antes de movimentar o produto.
2. Depois de adquirir o bloqueio do estoque, **repetir** a consulta com leitura atualizada (por exemplo, em `READ COMMITTED`) antes de calcular nova saída.
3. Quando a chave já existir, comparar **produto, quantidade e origem** com o registro anterior: se iguais, devolver a saída já confirmada; se divergentes, retornar erro de conflito sem movimentar estoque.
4. Manter o **índice único** mesmo com as verificações acima. Se outra transação confirmar a mesma chave em produto diferente entre consultas, o `INSERT` perdedor deverá falhar; a implementação faz rollback e relê o registro vencedor para comparar os dados.
5. Não retornar sucesso de `SaidaRegistrada` antes que a transação da operação vencedora esteja confirmada.

A escolha de retenção de referências e o tratamento idempotente de **operações rejeitadas** ainda exigem decisão explícita em uma implementação real. Neste laboratório, a garantia documentada cobre operações **confirmadas**.

## 4. Outbox e entrega eventual

Para o caso **15 → 5** com mínimo **5**:

- `EstoqueDoProduto.PlanejarSaida(10)` devolve `DeveNotificar = true`.
- A transação grava o novo saldo, a movimentação e uma `NotificacaoPendente` vinculada à movimentação.
- O worker consulta a outbox e solicita envio ao **Provedor de Notificações** depois do commit.
- Se o provedor falhar, o worker mantém o item pendente para nova tentativa; o saldo **não é revertido**.
- Se houver falha após o provedor processar a notificação, o worker pode repetir o envio. **A entrega é potencialmente pelo menos uma vez**, não exatamente uma vez.

A semântica de cruzamento do mínimo é **exclusivamente uma regra de domínio**: saldos que já estavam iguais ou abaixo do mínimo não geram um novo registro de alerta a cada baixa.

## 5. Riscos a explicar, não esconder

| Risco | Controle ilustrativo |
| --- | --- |
| Duas saídas usam o mesmo saldo | `FOR UPDATE` ou alternativa condicional atômica com verificação do resultado. |
| A mesma venda é reenviada | Chave única persistida, leitura de duplicidade e comparação de payload. |
| Duas vendas compartilham acidentalmente a mesma chave | Conflito; não reaproveitar resultado com produto/quantidade diferentes. |
| Gravação de outbox falha | Reverter a transação e **não** confirmar a baixa. |
| Worker envia mas falha antes de atualizar status | Repetição possível; destinatário deve suportar deduplicação quando aplicável. |
| Worker e API utilizam o mesmo banco | Limitar acesso do worker à outbox; não permitir que ele altere saldos. |

## 6. Rastreabilidade

- [ADR 0003: PostgreSQL transacional](../docs/adr/0003-adotar-postgresql-transacional.md)
- [ADR 0005: Outbox sem broker](../docs/adr/0005-adotar-outbox-sem-broker.md)
- [ADR 0006: Concorrência no saldo](../docs/adr/0006-proteger-concorrencia-no-saldo.md)
- [ADR 0007: Idempotência em baixas externas](../docs/adr/0007-exigir-idempotencia-em-baixas-externas.md)

Todos os ADRs seguem com status **Proposed**. A validação do ADR Guard verifica sua estrutura, **não** as garantias transacionais aqui descritas.
