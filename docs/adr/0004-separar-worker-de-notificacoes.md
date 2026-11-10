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
