# Separar o processamento de notificações em um worker

## Status

Proposed

## Context

Quando o saldo cruza o estoque mínimo, o sistema precisa solicitar um alerta a um provedor externo. Uma chamada síncrona ao provedor durante a baixa de estoque aumentaria latência e tornaria a disponibilidade do provedor parte do fluxo transacional. Consideramos realizar o envio dentro da API ou em uma unidade de execução separada.

## Decision

Definir um Worker Service .NET como contêiner executável distinto da API. O worker busca solicitações pendentes, tenta enviá-las ao provedor externo e registra resultados ou tentativas. Ele não aplica regras de entrada e saída nem altera saldos.

## Consequences

O fluxo da API não precisa aguardar um serviço externo para confirmar a movimentação. O nível 2 passa a ilustrar claramente responsabilidades diferentes entre dois contêineres executáveis.

Em contrapartida, haverá mais uma unidade a operar, observar e escalar, e o envio passa a ser eventual. O worker precisará tratar falhas, repetição de mensagens e retomada após interrupções.

## Decision Drivers

- Manter a confirmação síncrona da baixa independente da disponibilidade do provedor de notificações.
- Separar responsabilidades de negócio das tentativas de envio, monitoramento e recuperação.

## Alternatives Considered

- **Envio síncrono pela API:** tem menos processos, mas aumenta latência e acopla a disponibilidade do provedor à requisição.
- **Processamento em background dentro da API:** evita um executável adicional, mas compartilha implantação e capacidade com o tráfego de estoque.
- **Worker separado (proposto):** isola o processamento eventual ao custo de outra unidade operacional.

## Risks

- Tentativas exigem backoff, visibilidade, tratamento de falhas permanentes e monitoramento.
- Várias instâncias do worker precisam reivindicar itens de modo concorrência-seguro, sem prometer impedir duplicidade depois de falhas externas.
- O worker não deve alterar saldos nem movimentações: apenas o estado operacional dos itens de outbox.

## References

- [Fluxo assíncrono do worker](../fluxo-movimentacao.md)
