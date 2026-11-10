# Exemplo C#: RegistrarSaida

Este exemplo **ilustra apenas o recorte do nível 4** documentado em [`docs/04-codigo.md`](../docs/04-codigo.md). Não é uma aplicação executável e não inclui adaptador PostgreSQL, endpoint HTTP, worker, configuração de injeção de dependências ou testes compilados.

A interface de persistência recebe uma função de domínio, que **deve ser invocada após o saldo ter sido bloqueado em uma transação**. Ela devolve o resultado somente após persistir as alterações e confirmar o commit. O exemplo abaixo representa a **API dessa colaboração**, mas **não implementa** a garantia transacional.

## Tipos e responsabilidades

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

namespace InventoryLab;

public enum OrigemSaida
{
    OperacaoManual,
    SistemaDeVendas
}

public sealed record RegistrarSaidaCommand(
    Guid ProdutoId,
    int Quantidade,
    OrigemSaida Origem,
    string? ReferenciaExterna);

public sealed record PlanoSaida(
    int SaldoAnterior,
    int SaldoFinal,
    bool DeveNotificar);

public sealed record SaidaRegistrada(
    Guid MovimentacaoId,
    int SaldoFinal,
    bool AlertaRegistrado);

public sealed record MovimentacaoDeEstoque(
    Guid Id,
    Guid ProdutoId,
    int Quantidade,
    OrigemSaida Origem,
    string? ReferenciaExterna);

public sealed record NotificacaoPendente(
    Guid Id,
    Guid MovimentacaoId,
    string Tipo);

public sealed class SaldoInsuficienteException()
    : Exception("A quantidade solicitada excede o saldo disponível.");

public sealed class EstoqueDoProduto
{
    public Guid ProdutoId { get; }
    public int Saldo { get; }
    public int EstoqueMinimo { get; }

    public EstoqueDoProduto(Guid produtoId, int saldo, int estoqueMinimo)
    {
        if (saldo < 0 || estoqueMinimo < 0)
            throw new ArgumentOutOfRangeException(nameof(saldo));

        ProdutoId = produtoId;
        Saldo = saldo;
        EstoqueMinimo = estoqueMinimo;
    }

    public PlanoSaida PlanejarSaida(int quantidade)
    {
        if (quantidade <= 0)
            throw new ArgumentOutOfRangeException(nameof(quantidade));

        if (quantidade > Saldo)
            throw new SaldoInsuficienteException();

        int saldoFinal = checked(Saldo - quantidade);
        bool cruzouMinimo = Saldo > EstoqueMinimo
            && saldoFinal <= EstoqueMinimo;

        return new PlanoSaida(Saldo, saldoFinal, cruzouMinimo);
    }
}

// Porta consumida pela aplicação; uma implementação PostgreSQL é futura.
public interface IRegistroSaidaTransacional
{
    Task<SaidaRegistrada> RegistrarAsync(
        RegistrarSaidaCommand comando,
        Func<EstoqueDoProduto, PlanoSaida> planejar,
        CancellationToken cancellationToken);
}

public sealed class RegistrarSaidaUseCase(
    IRegistroSaidaTransacional persistencia)
{
    public Task<SaidaRegistrada> ExecutarAsync(
        RegistrarSaidaCommand comando,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(comando);

        if (comando.Origem == OrigemSaida.SistemaDeVendas
            && string.IsNullOrWhiteSpace(comando.ReferenciaExterna))
        {
            throw new ArgumentException(
                "Baixas do sistema de vendas exigem referência de origem.");
        }

        // A implementação da porta verifica idempotência, bloqueia o
        // saldo, executa a regra e confirma movimento + outbox juntos.
        return persistencia.RegistrarAsync(
            comando,
            estoque => estoque.PlanejarSaida(comando.Quantidade),
            cancellationToken);
    }
}
```

## Como interpretar

- **`RegistrarSaidaUseCase` (aplicação):** coordena a solicitação, sem conhecer SQL ou detalhes do provedor de notificações. A identificação da origem é validada na borda do caso de uso.
- **`EstoqueDoProduto` (domínio):** não faz I/O; valida e calcula os efeitos da saída sobre um **snapshot protegido** do saldo. O método `PlanejarSaida` **não persiste nem altera** o estado do objeto.
- **`PlanoSaida` (valor imutável):** carrega os dados necessários para persistir saldo, movimento e alerta. A detecção do cruzamento do mínimo é uma regra do domínio.
- **`IRegistroSaidaTransacional` (porta):** define a expectativa de atomicidade, concorrência, idempotência e confirmação de commit; é uma abstração e **não** uma implementação.
- **`MovimentacaoDeEstoque` e `NotificacaoPendente`:** modelos de dados do exemplo. A implementação futura da porta os criaria e persistiria dentro de uma única transação, seguindo o `PlanoSaida`.
- **`SaidaRegistrada` (resultado):** `AlertaRegistrado` indica gravação da outbox, **não envio da notificação**.

O `RegistrarSaidaCommand` permite referência externa ausente em uma operação manual. Quando a origem é `SistemaDeVendas`, a referência é obrigatória. Para permitir deduplicação de operações manuais no futuro, a interface aceita uma referência opcional.

## Verificação conceitual

| Saldo anterior | Mínimo | Saída | Saldo final | DeveNotificar |
| ---: | ---: | ---: | ---: | --- |
| 15 | 5 | 10 | 5 | `true` |
| 5 | 5 | 1 | 4 | `false` |
| 16 | 5 | 2 | 14 | `false` |
| 8 | 5 | 10 | rejeitado | não gera outbox |
| 15 | 5 | 0 | rejeitado | não gera outbox |

O caso **5 → 4** não solicita um novo alerta: o saldo **já estava no limite mínimo** antes da baixa. Isso respeita a regra [RN-06](../docs/escopo-funcional.md#4-regras-de-negócio), que dispara o alerta apenas ao cruzar de **acima** do mínimo para **menor ou igual** ao mínimo.

## Limites do exemplo

Não há testes executados, banco de dados, commit ou schema. **Não copie a interface para um sistema de produção presumindo que a sua implementação automaticamente garantirá atomicidade ou idempotência**. Consulte a [descrição do contrato transacional e suas falhas](persistencia-transacional.md) e o [capítulo do nível 4](../docs/04-codigo.md).

Ao construir uma aplicação real, explicite os casos de erro, concorrência e os testes de integração com PostgreSQL antes de afirmar que a invariante do saldo está protegida.
