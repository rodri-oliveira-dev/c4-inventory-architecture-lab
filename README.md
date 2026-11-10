# C4 Inventory Architecture Lab

[![ADR Guard](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/adr-guard.yml/badge.svg)](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/adr-guard.yml)

Um laboratório **didático e orientado à documentação** para aprender a comunicar a arquitetura de um sistema de gestão de estoque com os **quatro níveis do Modelo C4**, diagramas **Mermaid** e pequenos exemplos em **C#/.NET**.

> **Objetivo:** demonstrar como a mesma solução pode ser apresentada, do contexto de negócio às classes de código, preservando consistência entre os níveis. **Não** se trata de um produto de estoque pronto para produção.

## O cenário

Uma operação precisa cadastrar produtos, registrar entradas e saídas de mercadorias, consultar saldos e emitir alertas quando um produto atinge seu estoque mínimo.

O fio condutor da documentação é uma **saída de 10 unidades**: um operador ou sistema de vendas solicita a baixa; a aplicação valida as regras, registra a movimentação, atualiza o saldo e, quando necessário, agenda uma notificação.

Consulte o [escopo funcional](docs/escopo-funcional.md) e a [arquitetura de referência](docs/arquitetura-referencia.md).

## Os quatro níveis

| Nível | Pergunta principal | Representação planejada |
| --- | --- | --- |
| **1. System Context** | Quem utiliza o sistema e com quais sistemas ele interage? | [C4Context: ver diagrama](docs/01-contexto.md) |
| **2. Containers** | Quais aplicações e armazenamentos compõem a solução? | [C4Container: ver diagrama](docs/02-containers.md) |
| **3. Components** | Como a API é organizada internamente? | [C4Component: ver diagrama](docs/03-componentes.md) |
| **4. Code** | Como as responsabilidades aparecem nas classes C#? | `classDiagram` |

O Mermaid oferece sintaxes experimentais para os diagramas C4 dos três primeiros níveis. Para o quarto nível, usamos um **diagrama de classes**, não uma sintaxe `C4Code` inexistente. Saiba mais no [guia de modelagem](docs/guia-c4.md).

## Arquitetura que será documentada

- **Aplicação web:** consultas e operações realizadas por pessoas.
- **API ASP.NET Core (.NET 10):** casos de uso, regras de negócio, integrações e acesso aos dados.
- **Worker .NET:** entrega assíncrona de alertas de estoque mínimo.
- **PostgreSQL:** persistência transacional de produtos, saldos, movimentações e mensagens pendentes de notificação.
- **Integrações externas:** sistema de vendas e provedor de notificações.

Essas escolhas são **hipóteses didáticas**, não recomendações universais. Os motivos e limites estão em [decisões arquiteturais](docs/decisoes-arquiteturais.md).

## Roteiro de construção

1. **Fundação:** README, escopo, arquitetura de referência e convenções.
2. **Nível 1:** [contexto do sistema](docs/01-contexto.md) (disponível).
3. **Nível 2:** [contêineres do sistema](docs/02-containers.md) (disponível).
4. **Nível 3:** [componentes internos da API](docs/03-componentes.md) (disponível).
5. **Nível 4:** classes e exemplos ilustrativos em C#.
6. **Fluxos e decisões:** sequência da movimentação e aprofundamento dos ADRs iniciais.
7. **Qualidade e publicação:** validação de diagramas e links, revisão e preparação da versão 1.0.0. A validação dos ADRs foi antecipada para a etapa 1.

Os diagramas dos [níveis 1 (Contexto)](docs/01-contexto.md), [2 (Contêineres)](docs/02-containers.md) e [3 (Componentes)](docs/03-componentes.md) estão disponíveis em Mermaid. O nível 4 e os fluxos complementares serão incorporados nas próximas etapas.

## Comece por aqui

1. [Nível 1: Contexto do Sistema de Gestão de Estoque](docs/01-contexto.md)
2. [Nível 2: Contêineres do Sistema de Gestão de Estoque](docs/02-containers.md)
3. [Nível 3: Componentes da API de Estoque](docs/03-componentes.md)
4. [Índice da documentação](docs/README.md)
5. [Escopo e regras de negócio](docs/escopo-funcional.md)
6. [Arquitetura de referência](docs/arquitetura-referencia.md)
7. [Guia dos níveis C4 e Mermaid](docs/guia-c4.md)
8. [Decisões arquiteturais e ADRs](docs/decisoes-arquiteturais.md)

## Validação de decisões arquiteturais

As decisões são registradas como [ADRs propostos](docs/decisoes-arquiteturais.md). Para instalar a versão fixada do **ADR Guard** e validar localmente (requer SDK .NET 10):

```bash
dotnet tool restore
dotnet tool run adr-guard -- check docs/adr
```

O [GitHub Actions](.github/workflows/adr-guard.yml) executa a **Action oficial ADR Guard v1.10.0** em pull requests e na `main`, independentemente de quais arquivos mudaram.

Para contribuir, consulte [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

Distribuído sob a [licença MIT](LICENSE). © 2026 Rodrigo de Oliveira.
