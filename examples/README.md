# Exemplos ilustrativos em C#

Os exemplos da **etapa 5** apoiam o [nível 4 (Code)](../docs/04-codigo.md), sem criar um projeto ou uma aplicação executável.

| Exemplo | Objetivo |
| --- | --- |
| [`RegistrarSaida` em C#](registrar-saida.md) | Mostrar a porta transacional, o caso de uso, o objeto de domínio, o plano e o resultado de uma saída. |
| [Persistência transacional](persistencia-transacional.md) | Explicar bloqueio, idempotência, atomicidade e outbox com roteiro e SQL ilustrativos. |

**Convenções:** os blocos `csharp` são ilustrações, **não foram compilados nem executados**; o SQL é **esquemático**, não uma migration ou um script de produção. Não há implementação do adaptador, endpoint, worker ou testes automatizados.

Os [diagramas de sequência](../docs/fluxo-movimentacao.md) mostram essas responsabilidades em execução. O cenário permanece a saída de **10 unidades** do `SKU-001`, com saldo inicial **15**, limite mínimo **5** e saldo final **5**. Consulte o [escopo funcional](../docs/escopo-funcional.md), os [ADRs](../docs/decisoes-arquiteturais.md) e a [arquitetura de referência](../docs/arquitetura-referencia.md).
