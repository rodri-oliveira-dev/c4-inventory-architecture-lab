# Registro inicial de decisões arquiteturais

Este documento registra **premissas para o laboratório**, não ADRs formais nem evidências de uma implementação. Na etapa 6, decisões relevantes poderão ser convertidas em ADRs com contexto, alternativas e consequências.

| ID | Decisão de referência | Justificativa / consequência |
| --- | --- | --- |
| **D-01** | Monólito modular para o núcleo de estoque | Reduz complexidade operacional; permite demonstrar componentes bem delimitados dentro da API. |
| **D-02** | ASP.NET Core e C# / .NET 10 | Aproxima o nível 4 de um ecossistema amplamente usado e permite exemplos curtos. |
| **D-03** | PostgreSQL para persistência transacional | Mantém saldo, movimentação, idempotência e outbox na mesma fronteira transacional. |
| **D-04** | Worker .NET separado da API | Ilustra um segundo contêiner executável e isola a entrega assíncrona de alertas. |
| **D-05** | Outbox no banco, sem broker externo | Evita que a indisponibilidade do provedor impeça uma movimentação confirmada; exige controle de tentativas e duplicações. |
| **D-06** | Concorrência protegida no banco | A validação apenas em memória não impede duas saídas simultâneas de consumirem o mesmo saldo. |
| **D-07** | Idempotência de baixas originadas em vendas | Reenvio ou retry não podem repetir a movimentação. |
| **D-08** | SPA sem framework front-end escolhido | O estudo trata arquitetura e responsabilidades, não comparação de frameworks de interface. |
| **D-09** | Diagrama de classes no nível 4 | Mermaid não dispõe de sintaxe `C4Code`; usar `classDiagram` deixa a representação explícita. |

## Alternativas intencionalmente não adotadas

- **Microsserviços:** adicionariam descoberta, contratos distribuídos e consistência entre serviços sem melhorar o objetivo didático.
- **Broker de mensagens:** poderia ser uma evolução, mas acrescentaria mais um contêiner e novas preocupações operacionais.
- **Event sourcing:** desnecessário para representar histórico de movimentações e saldo transacional neste exemplo.
- **Aplicação executável completa:** desviaria o foco da documentação arquitetural.

## Pontos para refinar nas próximas etapas

- Contratos conceituais das integrações e semântica das respostas idempotentes.
- Estratégia ilustrativa de concorrência: atualização condicional, bloqueio ou versão.
- Política de tentativas, falhas permanentes e duplicidade do worker.
- Delimitação final das interfaces e classes mostradas no nível 4.

As decisões devem evoluir com os diagramas, sem gerar inconsistência com o [escopo](escopo-funcional.md) e a [arquitetura de referência](arquitetura-referencia.md).
