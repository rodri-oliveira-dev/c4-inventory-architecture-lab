# Decisões arquiteturais

Este documento é o **índice comentado** das escolhas arquiteturais deste laboratório. Os arquivos individuais em [`docs/adr/`](adr/) seguem o formato **canonical** do [ADR Guard](https://github.com/rodri-oliveira-dev/adr-guard) e são verificados automaticamente a cada pull request.

> Todos os registros começam com status **Proposed**. São propostas que sustentam o desenho didático, **não** decisões aprovadas por uma equipe nem evidências de implementação. A aprovação requer revisão humana; o sucesso do ADR Guard significa apenas conformidade estrutural e de políticas documentais.

## Catálogo de decisões

| ID | ADR | Motivação e principal consequência | Status |
| --- | --- | --- | --- |
| D-01 | [ADR 0001 — Adotar um monólito modular para o núcleo de estoque](adr/0001-adotar-monolito-modular.md) | Organizar o núcleo de estoque em um único serviço modular, sem complexidade distribuída. | Proposed |
| D-02 | [ADR 0002 — Usar ASP.NET Core, C# e .NET 10 na API de estoque](adr/0002-usar-aspnet-core-e-net-10.md) | Usar C#/.NET 10 nos exemplos para dar concretude às responsabilidades. | Proposed |
| D-03 | [ADR 0003 — Adotar PostgreSQL como armazenamento transacional de estoque](adr/0003-adotar-postgresql-transacional.md) | Manter saldo, histórico, idempotência e outbox na mesma base transacional. | Proposed |
| D-04 | [ADR 0004 — Separar o processamento de notificações em um worker](adr/0004-separar-worker-de-notificacoes.md) | Isolar o envio eventual de alertas da API transacional. | Proposed |
| D-05 | [ADR 0005 — Adotar outbox transacional sem broker de mensagens](adr/0005-adotar-outbox-sem-broker.md) | Registrar intenções de notificação de maneira atômica, sem broker nesta versão. | Proposed |
| D-06 | [ADR 0006 — Proteger o saldo de estoque contra atualizações concorrentes](adr/0006-proteger-concorrencia-no-saldo.md) | Impedir saídas concorrentes acima do saldo disponível. | Proposed |
| D-07 | [ADR 0007 — Exigir idempotência em solicitações externas de baixa](adr/0007-exigir-idempotencia-em-baixas-externas.md) | Impedir que retries de vendas gerem movimentações duplicadas. | Proposed |
| D-08 | [ADR 0008 — Adiar a escolha de framework da interface web](adr/0008-adiar-escolha-framework-da-interface.md) | Manter a UI independente de um framework específico. | Proposed |
| D-09 | [ADR 0009 — Usar Mermaid classDiagram para o nível 4 do C4](adr/0009-usar-classdiagram-no-nivel-quatro.md) | Representar classes do nível 4 com Mermaid classDiagram, não C4Code. | Proposed |

## Decisões aplicadas ao fluxo da etapa 6

O [diagrama de sequência da movimentação](fluxo-movimentacao.md) relaciona a confirmação transacional e a entrega eventual aos ADRs **0003 a 0007**, aprofundados nesta etapa com direcionadores, alternativas e riscos operacionais. Todos permanecem **Proposed** e exigem revisão humana para qualquer mudança de status.

## Alternativas intencionalmente não adotadas

- **Microsserviços:** introduziriam contratos e consistência distribuída sem benefício para o objetivo do laboratório ([ADR 0001](adr/0001-adotar-monolito-modular.md)).
- **Broker de mensagens:** acrescentaria infraestrutura e processamento distribuído desnecessários para o exemplo ([ADR 0005](adr/0005-adotar-outbox-sem-broker.md)).
- **Event sourcing:** não é requisito para manter movimentações auditáveis com saldo transacional; poderá ser discutido como alternativa futura.
- **Aplicação executável completa:** desviaria o projeto da documentação arquitetural ([ADR 0002](adr/0002-usar-aspnet-core-e-net-10.md)).

## Como validar com ADR Guard

O projeto fixa a versão **1.10.0** da ferramenta como .NET local tool, em [`.config/dotnet-tools.json`](../.config/dotnet-tools.json), e utiliza a [Action oficial v1.10.0](../.github/workflows/adr-guard.yml) no CI.

Com o SDK .NET 10 instalado, execute na raiz do repositório:

```bash
dotnet tool restore
dotnet tool run adr-guard -- check docs/adr
```

Para criar um novo registro, use `dotnet tool run adr-guard -- new docs/adr --title "Título da decisão" --culture pt-BR`, edite o conteúdo e mantenha o status `Proposed` até aprovação explícita. Os cabeçalhos obrigatórios são `Status`, `Context`, `Decision` e `Consequences`, mesmo quando o texto é escrito em português.

A validação do ADR Guard incide **sobre `docs/adr/`**, não sobre este quadro-resumo. O GitHub Actions executa `check` em todas as PRs para `main` e após merges; uma falha de validação fará o job falhar, mas é preciso configurar a proteção de branch para torná-lo obrigatório.

## Pontos para refinar nas próximas etapas

- Contrato do provedor de notificações e deduplicação quando suportada.
- Retenção de chaves e política para operações rejeitadas.
- Política de reivindicação da outbox, tentativas, falhas permanentes e observabilidade.
- Testes de integração de concorrência e falhas numa eventual implementação.

As mudanças devem ser refletidas nos ADRs e nos diagramas, preservando consistência com o [escopo](escopo-funcional.md) e a [arquitetura de referência](arquitetura-referencia.md).
