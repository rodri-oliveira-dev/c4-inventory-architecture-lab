# C4 Inventory Architecture Lab

[![ADR Guard](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/adr-guard.yml/badge.svg)](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/adr-guard.yml)
[![Documentation Quality](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/docs-quality.yml/badge.svg)](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/docs-quality.yml)
[![LikeC4 Site](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/likec4-pages.yml/badge.svg)](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/likec4-pages.yml)

Um laboratório **didático e orientado à documentação** para aprender a comunicar a arquitetura de um sistema de gestão de estoque com os **quatro níveis do Modelo C4**, diagramas **Mermaid** e pequenos exemplos em **C#/.NET**.

> **Objetivo:** demonstrar como a mesma solução pode ser apresentada, do contexto de negócio às classes de código, preservando consistência entre os níveis. **Não** se trata de um produto de estoque pronto para produção.

## O que é o Modelo C4?

O **Modelo C4**, criado por Simon Brown, é uma abordagem para **visualizar e comunicar a arquitetura de software**. Em vez de tentar mostrar tudo em um único desenho, ele propõe diferentes níveis de detalhe, como o zoom de um mapa: primeiro vemos o sistema em seu ambiente; depois, aproximamos a visão para entender sua estrutura interna e, quando necessário, sua implementação.

O nome **C4** vem dos quatro níveis de diagramas: **Contexto (Context)**, **Contêineres (Containers)**, **Componentes (Components)** e **Código (Code)**. Cada nível responde a perguntas diferentes e se destina a públicos com necessidades distintas. A tabela abaixo apresenta essas perguntas no cenário deste laboratório.

### Três conceitos para começar

- **Contêiner não significa Docker:** no C4, pode ser uma aplicação executável ou um armazenamento de dados, como a aplicação web, a API ou o PostgreSQL deste exemplo.
- **Componente não é necessariamente uma classe:** é um conjunto coeso de funcionalidades e responsabilidades dentro de um contêiner. As classes e interfaces que o implementam aparecem em um nível mais detalhado.
- **C4 não é uma ferramenta de desenho:** o modelo é independente de notação e tecnologia. Neste repositório, usamos **Mermaid** e **LikeC4** para representar a mesma arquitetura.

**É preciso usar os quatro níveis?** Não. Em projetos reais, escolha os diagramas que ajudam a comunicar a solução; muitas equipes precisam apenas de Contexto e Contêineres. Aqui, mostramos os quatro para fins de aprendizado. O nível de Código é opcional e usa um recorte de classes C#, sem exigir a execução de uma aplicação.

**Referência:** [documentação oficial do Modelo C4](https://c4model.com/) e [visão geral dos diagramas](https://c4model.com/diagrams).

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
| **4. Code** | Como as responsabilidades aparecem nas classes C#? | [classDiagram: ver diagrama](docs/04-codigo.md) |

O Mermaid oferece sintaxes experimentais para os diagramas C4 dos três primeiros níveis. Para o quarto nível, usamos um **diagrama de classes**, não uma sintaxe `C4Code` inexistente. Saiba mais no [guia de modelagem](docs/guia-c4.md).

## LikeC4: segunda representação arquitetural

Além dos diagramas Mermaid existentes, iniciamos a [alternativa LikeC4](likec4/README.md), baseada em **um modelo arquitetural compartilhado**. A fundação define atores, integrações e contêineres; a etapa 2 acrescentou as visões de [**Contexto e Contêineres**](likec4/visoes-contexto-conteineres.md), e a etapa 3 abre [**os cinco Componentes da API**](likec4/visao-componentes.md) a partir do mesmo modelo. A etapa 4 acrescenta [**dois fluxos dinâmicos**](likec4/fluxos-dinamicos.md): baixa transacional e entrega eventual da outbox. Os capítulos Mermaid continuam disponíveis em paralelo.

**Site publicado:** [C4 Inventory Architecture Lab — LikeC4](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/). Navegue entre Contexto, Contêineres, Componentes e os dois fluxos dinâmicos. Para iPhone ou navegadores móveis com dificuldades de renderização, existe uma [**versão leve sem JavaScript**](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/mobile/) com os seis diagramas Mermaid em SVG; ela é escolhida automaticamente na entrada em telas iOS compactas, com opção explícita de abrir o modo interativo. Veja a [compatibilidade mobile](docs/compatibilidade-mobile.md) e o [guia de publicação](docs/likec4-vs-mermaid.md#processo-de-publicação).

Para explorar o modelo (Node.js 22):

```bash
npm install
npm run likec4:validate
npm run likec4:dev
npm run likec4:build:pages
```

O servidor de prévia LikeC4 usa o modelo em `likec4/`. A visualização `index` representa o **nível 1**, com navegação para `conteineres` (**nível 2**) e, na API, para `componentes` (**nível 3**). O **nível 4** segue com `classDiagram` Mermaid. As duas visões de sequência LikeC4 são `registrarSaida` e `entregarAlerta`. A etapa 5 acrescenta a [publicação automática no GitHub Pages](.github/workflows/likec4-pages.yml) e uma [comparação didática Mermaid vs. LikeC4](docs/likec4-vs-mermaid.md). Consulte as [convenções e o roteiro](likec4/README.md). A validação inicial do modelo está incluída no workflow [Documentation Quality](.github/workflows/docs-quality.yml).

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
5. **Nível 4:** [classes e exemplos ilustrativos em C#](docs/04-codigo.md) (disponível).
6. **Fluxos e decisões:** [sequência da movimentação](docs/fluxo-movimentacao.md) e aprofundamento dos ADRs 0003 a 0007 (disponível).
7. **Qualidade e publicação:** [validação automática de Mermaid e links](.github/workflows/docs-quality.yml), revisão e [preparação da v1.0.0](docs/publicacao.md) (disponível).

Os quatro níveis já estão documentados: [Contexto](docs/01-contexto.md), [Contêineres](docs/02-containers.md), [Componentes](docs/03-componentes.md) e [Código](docs/04-codigo.md). O nível 4 utiliza `classDiagram` e pequenos [exemplos C#](examples/registrar-saida.md). O [fluxo de movimentação](docs/fluxo-movimentacao.md) ilustra a confirmação transacional e a entrega eventual. A validação de diagramas e links Markdown está configurada na etapa 7.

## Comece por aqui

1. [Nível 1: Contexto do Sistema de Gestão de Estoque](docs/01-contexto.md)
2. [Nível 2: Contêineres do Sistema de Gestão de Estoque](docs/02-containers.md)
3. [Nível 3: Componentes da API de Estoque](docs/03-componentes.md)
4. [Nível 4: Código do caso de uso RegistrarSaida](docs/04-codigo.md)
5. [Fluxo de movimentação: sequência e falhas](docs/fluxo-movimentacao.md)
6. [Exemplos C# e persistência](examples/README.md)
7. [Índice da documentação](docs/README.md)
8. [Escopo e regras de negócio](docs/escopo-funcional.md)
9. [Arquitetura de referência](docs/arquitetura-referencia.md)
10. [Guia dos níveis C4 e Mermaid](docs/guia-c4.md)
11. [Decisões arquiteturais e ADRs](docs/decisoes-arquiteturais.md)
12. [Preparação da release v1.0.0](docs/publicacao.md)
13. [Mermaid vs. LikeC4 e publicação do site](docs/likec4-vs-mermaid.md)

## Validação de decisões arquiteturais

As decisões são registradas como [ADRs propostos](docs/decisoes-arquiteturais.md). Para instalar a versão fixada do **ADR Guard** e validar localmente (requer SDK .NET 10):

```bash
dotnet tool restore
dotnet tool run adr-guard -- check docs/adr
```

O [GitHub Actions](.github/workflows/adr-guard.yml) executa a **Action oficial ADR Guard v1.10.0** em pull requests e na `main`, independentemente de quais arquivos mudaram.

## Qualidade da documentação

O workflow [Documentation Quality](.github/workflows/docs-quality.yml) roda em todo pull request para `main`, pushes para `main` e manualmente. Ele verifica links e âncoras Markdown locais, extrai os blocos Mermaid dos capítulos e tenta renderizá-los com **Mermaid CLI 11.17.1**, sem manter cópias `.mmd` no Git. Os SVGs gerados ficam disponíveis como artefatos do workflow. A versão do Mermaid CLI é declarada em [`package.json`](package.json) e instalada pelo CI a partir desse manifesto, permitindo atualizações propostas pelo Dependabot.

Verificação local (Python 3.12+):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_docs.py --output-dir .tmp/mermaid
```

O comando Python verifica links e a estrutura dos blocos. Para comprovar **renderização**, execute também o Mermaid CLI `11.17.1` sobre cada `.mmd` extraído, como no workflow. Links externos não são consultados via HTTP no CI para evitar instabilidade de rede e limites de requisição.

## Atualizações de dependências

O [Dependabot](.github/dependabot.yml) verifica semanalmente:

- **GitHub Actions** nos workflows, incluindo ações oficiais e a ação ADR Guard.
- **npm** no `package.json` da raiz, utilizado para instalar `@mermaid-js/mermaid-cli` e `likec4` no workflow de documentação.

As atualizações `minor` e `patch` são agrupadas, enquanto mudanças `major` recebem PRs próprios e precisam passar pelo CI antes de merge. O manifesto local [`.config/dotnet-tools.json`](.config/dotnet-tools.json) contém o ADR Guard da CLI, cuja versão deve ser conferida manualmente: este repositório não contém um projeto .NET para o Dependabot NuGet atualizar. Não há dependências Python de terceiros ou uma imagem Docker neste laboratório.

Para contribuir, consulte [CONTRIBUTING.md](CONTRIBUTING.md). Para publicar, consulte o [checklist de v1.0.0](docs/publicacao.md).

## Licença

Distribuído sob a [licença MIT](LICENSE). © 2026 Rodrigo de Oliveira.
