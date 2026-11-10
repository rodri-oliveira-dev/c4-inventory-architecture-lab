# Escopo funcional do sistema de estoque

## 1. Problema e objetivo

Uma operação comercial precisa conhecer o saldo disponível de cada produto e registrar movimentações com rastreabilidade. Uma saída não pode consumir quantidade inexistente, mesmo quando requisições ocorrem simultaneamente.

**Objetivo do estudo:** oferecer um cenário suficientemente concreto para ilustrar os quatro níveis do C4 sem implementar um sistema completo.

## 2. Atores e sistemas externos

| Elemento | Papel |
| --- | --- |
| **Operador de estoque** | Cadastra produtos, registra entradas e saídas e consulta saldo/histórico. |
| **Gestor de estoque** | Consulta saldos críticos e configura o estoque mínimo dos produtos. |
| **Sistema de vendas (externo)** | Solicita baixa de estoque vinculada a uma venda, fornecendo um identificador único de origem. |
| **Provedor de notificações (externo)** | Recebe solicitações de envio de alerta para responsáveis pelo estoque. |

**Fronteira:** o sistema estudado é o **Sistema de Gestão de Estoque**. Sistema de vendas e provedor de notificações estão fora dessa fronteira.

## 3. Requisitos funcionais

| ID | Requisito |
| --- | --- |
| **RF-01** | Cadastrar produto com identificador, SKU único, descrição e estoque mínimo. |
| **RF-02** | Registrar entrada de quantidade positiva, com origem e data. |
| **RF-03** | Registrar saída de quantidade positiva, manualmente ou via integração com vendas. |
| **RF-04** | Consultar saldo disponível e histórico de movimentações de um produto. |
| **RF-05** | Consultar produtos em nível crítico (saldo menor ou igual ao mínimo). |
| **RF-06** | Solicitar alerta quando uma movimentação faz o saldo cruzar o limite mínimo de cima para baixo. |
| **RF-07** | Permitir ajustar o estoque mínimo sem alterar saldos anteriores. |

## 4. Regras de negócio

- **RN-01:** quantidades movimentadas são números inteiros e estritamente positivos.
- **RN-02:** saldo de estoque nunca pode ficar negativo.
- **RN-03:** cada movimentação concluída gera um registro auditável com tipo, quantidade, data, origem e referência de origem quando aplicável.
- **RN-04:** requisições repetidas da mesma operação de vendas, identificadas pela mesma chave de idempotência, **não** geram uma segunda baixa.
- **RN-05:** atualizações concorrentes no mesmo produto devem preservar o saldo correto e impedir retiradas acima do disponível.
- **RN-06:** um alerta de cruzamento é registrado quando o saldo passa de **acima do mínimo** para **menor ou igual ao mínimo**. Ajustar o limite, isoladamente, não dispara alerta nesta versão.
- **RN-07:** erros de notificação não desfazem movimentações de estoque já confirmadas.

A definição de `saldo disponível` aqui é **saldo físico não reservado**. Reserva de unidades está fora do escopo.

## 5. Cenário transversal: saída de 10 unidades

**Estado inicial:** o produto `SKU-001` tem 15 unidades e estoque mínimo de 5.

1. O operador (ou sistema de vendas) solicita uma saída de **10 unidades**, informando a origem da operação.
2. A API valida a quantidade, localiza o estoque do produto e verifica a disponibilidade.
3. Uma transação persistente registra a movimentação e atualiza o saldo de **15 para 5**.
4. Como o saldo cruzou o limite mínimo, uma solicitação de notificação é persistida na mesma transação.
5. A API confirma a operação; o worker posteriormente processa a notificação com o provedor externo.
6. Uma repetição da mesma solicitação externa retorna o resultado já associado à chave de origem, sem descontar outras 10 unidades.

**Variação negativa:** se o saldo inicial fosse 8, a saída de 10 seria recusada, sem registrar movimentação nem atualizar saldo.

Este é o **mesmo cenário** a ser retomado nos níveis 1 a 4 e no futuro diagrama de sequência.

## 6. Qualidades e restrições

| Qualidade | Expectativa didática |
| --- | --- |
| **Consistência** | Saída validada e atualização de saldo devem ser atômicas. |
| **Concorrência** | Duas saídas simultâneas não podem criar saldo negativo. |
| **Rastreabilidade** | Histórico de movimentações preservado. |
| **Resiliência** | Falha no envio de alerta não reverte alteração de estoque. |
| **Simplicidade** | Uma única implantação lógica de estoque, sem microsserviços. |
| **Segurança** | Atores e integrações autenticados/autorizados conceitualmente; implementação fora do escopo. |

Não são estabelecidas metas numéricas de disponibilidade, latência ou volume, pois não existe carga real a ser medida.

## 7. Fora do escopo

- Gestão de múltiplos depósitos e transferências entre locais.
- Reserva de estoque, carrinho de compras e expedição.
- Pedidos de compra, fornecedores, pagamentos e faturamento.
- Inventário físico, lotes, validade, serialização e devoluções.
- Integração real com provedor de e-mail, autenticação e sistema de vendas.
- UI funcional, implantação em nuvem e benchmark de desempenho.

## 8. Glossário

- **SKU:** código único comercial do produto neste sistema.
- **Movimentação:** entrada ou saída que altera o saldo.
- **Estoque mínimo:** limite configurável para identificar necessidade de reposição.
- **Chave de idempotência:** identificador estável da operação de origem, usado para reconhecer repetições.
- **Outbox:** registro transacional de uma notificação pendente de processamento assíncrono.
