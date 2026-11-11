# C4 Inventory Architecture Lab

[![ADR Guard](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/adr-guard.yml/badge.svg)](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/adr-guard.yml)
[![Documentation Quality](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/docs-quality.yml/badge.svg)](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/docs-quality.yml)
[![LikeC4 Site](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/likec4-pages.yml/badge.svg)](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/workflows/likec4-pages.yml)

Um laboratório de documentação arquitetural para **aprender o Modelo C4 na prática**, usando um sistema fictício de gestão de estoque, diagramas **Mermaid** e **LikeC4** e exemplos ilustrativos em **C#/.NET**.

> **Objetivo:** mostrar como comunicar a mesma arquitetura em diferentes níveis de detalhe, do contexto do sistema ao código. Os diagramas e exemplos são didáticos: **não existe uma aplicação de estoque pronta para executar ou usar em produção**.

**Primeiro contato com C4?** Leia a introdução abaixo e siga a [trilha dos quatro níveis](#os-quatro-níveis), começando pelo Contexto. Não é necessário instalar ferramentas.

## O que é o Modelo C4?

O **Modelo C4**, criado por Simon Brown, é uma abordagem para **visualizar e comunicar a arquitetura de software**. Em vez de tentar mostrar tudo em um único desenho, ele propõe diferentes níveis de detalhe, como o zoom de um mapa: primeiro vemos o sistema em seu ambiente; depois, aproximamos a visão para entender sua estrutura interna e, quando necessário, sua implementação.

O nome **C4** vem dos quatro níveis de diagramas: **Contexto (Context)**, **Contêineres (Containers)**, **Componentes (Components)** e **Código (Code)**. Cada nível responde a perguntas diferentes e se destina a públicos com necessidades distintas. A [trilha dos quatro níveis](#os-quatro-níveis) relaciona essas perguntas ao cenário deste laboratório.

### Três conceitos para começar

- **Contêiner não significa Docker:** no C4, pode ser uma aplicação executável ou um armazenamento de dados, como a aplicação web, a API ou o PostgreSQL deste exemplo.
- **Componente não é necessariamente uma classe:** é um conjunto coeso de funcionalidades e responsabilidades dentro de um contêiner. As classes e interfaces que o implementam aparecem em um nível mais detalhado.
- **C4 não é uma ferramenta de desenho:** o modelo é independente de notação e tecnologia. Neste repositório, usamos **Mermaid** e **LikeC4** para representar a mesma arquitetura.

**É preciso usar os quatro níveis?** Não. Em projetos reais, escolha os diagramas que ajudam a comunicar a solução; muitas equipes precisam apenas de Contexto e Contêineres. Aqui, mostramos os quatro para fins de aprendizado. O nível de Código é opcional e usa um recorte de classes C#, sem exigir a execução de uma aplicação.

**Referência:** [documentação oficial do Modelo C4](https://c4model.com/) e [visão geral dos diagramas](https://c4model.com/diagrams).

## O cenário

Imagine uma operação comercial que precisa cadastrar produtos, registrar entradas e saídas de mercadorias, consultar saldos e avisar quando é necessário repor um item. Para estudar o C4, vamos acompanhar **a mesma saída de estoque** em todos os níveis, mudando apenas a quantidade de detalhes apresentada.

### Um exemplo concreto: saída de 10 unidades

| Informação | Valor |
| --- | --- |
| **Produto** | `SKU-001` |
| **Saldo inicial** | 15 unidades |
| **Estoque mínimo** | 5 unidades |
| **Saída solicitada** | 10 unidades |
| **Saldo após a saída** | 5 unidades |

O que acontece nesse exemplo?

1. Um **operador de estoque** solicita a saída pela aplicação web. A mesma operação também pode ser solicitada pelo **Sistema de Vendas**, uma integração externa.
2. A **API de Estoque** verifica se a quantidade é válida e se há saldo suficiente. Em uma transação, registra a movimentação e reduz o saldo de **15 para 5**.
3. Como o saldo passou de **acima do mínimo** para **igual ao mínimo**, a API grava uma notificação pendente **na mesma transação**. Esse registro é chamado de *outbox*: ele permite enviar o alerta depois, sem depender da disponibilidade do serviço de notificações para confirmar a saída.
4. A saída é confirmada. Posteriormente, o **worker** lê a pendência e solicita o alerta ao provedor externo. Uma falha no envio não desfaz a movimentação já confirmada.

**E se a operação não puder ser concluída?** Com apenas 8 unidades disponíveis, uma saída de 10 seria recusada, sem alterar o saldo. Se o Sistema de Vendas repetir uma solicitação externa já processada com a mesma referência, ela não deve descontar outras 10 unidades. Essa proteção contra processamento duplicado é chamada de **idempotência**.

### Como o mesmo exemplo aparece em cada nível?

| Nível C4 | O que observar no exemplo |
| --- | --- |
| **[1. Contexto](docs/01-contexto.md)** | **Quem** solicita a saída, qual sistema é responsável pelo estoque e quais sistemas externos participam. Não detalha aplicações nem processamento interno. |
| **[2. Contêineres](docs/02-containers.md)** | **Onde** estão as responsabilidades: aplicação web, API, PostgreSQL e worker. Mostra também as relações com os serviços externos. |
| **[3. Componentes](docs/03-componentes.md)** | **Como a API se organiza** para receber a solicitação, aplicar regras e persistir a movimentação e a notificação pendente. O foco é apenas o interior da API. |
| **[4. Código](docs/04-codigo.md)** | **Quais classes e interfaces** participam do caso de uso `RegistrarSaida`, incluindo regras de estoque e o contrato da operação transacional. |

**Importante:** os quatro diagramas mostram principalmente **a estrutura** do sistema em diferentes níveis de aproximação, não uma sequência detalhada de eventos. Para ver a ordem das interações, a confirmação da transação e o envio posterior do alerta, consulte o [fluxo de movimentação](docs/fluxo-movimentacao.md), uma visão dinâmica complementar.

Para conhecer todas as regras e os limites do exemplo, leia o [escopo funcional](docs/escopo-funcional.md) e a [arquitetura de referência](docs/arquitetura-referencia.md).

## Os quatro níveis

Esta é a **trilha principal de aprendizado**. Siga os capítulos de cima para baixo: cada nível aproxima a visão do mesmo Sistema de Gestão de Estoque, sem mudar seu objetivo de negócio.

| Etapa | Pergunta que o diagrama responde | O que você aprenderá | Leia o capítulo |
| --- | --- | --- | --- |
| **1. Contexto (System Context)** | Quem usa o sistema e com quais sistemas externos ele interage? | Identificar pessoas, sistemas externos e a fronteira do sistema em estudo. | [Começar pelo Contexto](docs/01-contexto.md) |
| **2. Contêineres (Containers)** | Quais aplicações e armazenamentos formam a solução? | Reconhecer a aplicação web, a API, o worker, o banco e suas comunicações. | [Avançar para Contêineres](docs/02-containers.md) |
| **3. Componentes (Components)** | Como a API se organiza internamente? | Distinguir responsabilidades dentro de um único contêiner e suas dependências. | [Explorar Componentes](docs/03-componentes.md) |
| **4. Código (Code)** | Como um comportamento é implementado em classes e interfaces? | Relacionar o caso de uso `RegistrarSaida` aos objetos de domínio e contratos C#. | [Examinar o Código](docs/04-codigo.md) |

### Como acompanhar cada capítulo

1. **Comece pela pergunta** do nível: ela define o que o diagrama precisa comunicar.
2. **Observe a fronteira e os relacionamentos**: identifique o que está dentro e fora do recorte.
3. **Acompanhe o mesmo exemplo**: uma saída de 10 unidades reduz o saldo de 15 para 5 e pode gerar um alerta.
4. **Compare com o próximo nível**: veja quais detalhes aparecem quando a visão se aproxima.

É possível percorrer toda a trilha **diretamente pelo GitHub**, sem instalar .NET, Node.js ou executar a aplicação. Os capítulos apresentam o desenho e explicam também **o que foi deixado de fora** de cada visão.

O Mermaid oferece sintaxes experimentais para os diagramas C4 dos três primeiros níveis. Para o quarto, utilizamos um **diagrama de classes** (`classDiagram`), pois não existe uma sintaxe Mermaid `C4Code`. Veja as [convenções de modelagem](docs/guia-c4.md).

### Depois dos quatro níveis

- **Entenda a ordem das interações:** [fluxo de movimentação, confirmação e falhas](docs/fluxo-movimentacao.md). O diagrama de sequência é complementar, **não** um quinto nível do C4.
- **Aproxime-se da implementação:** [exemplo C# de `RegistrarSaida`](examples/registrar-saida.md) e [índice de exemplos e persistência](examples/README.md), que ilustram o comportamento sem constituir uma aplicação pronta.
- **Investigue as escolhas:** [decisões arquiteturais e ADRs](docs/decisoes-arquiteturais.md), com justificativas e trade-offs.
- **Consulte outros materiais:** [índice completo da documentação](docs/README.md), para explorar os assuntos por tema.

## Arquitetura de referência

Para tornar os diagramas concretos, o laboratório adota estas **tecnologias e responsabilidades hipotéticas**:

| Elemento | Responsabilidade no exemplo |
| --- | --- |
| **Aplicação web** | Interface para consultas e movimentações realizadas por pessoas. |
| **API ASP.NET Core (.NET 10)** | Receber solicitações, aplicar regras de estoque e registrar operações transacionais. |
| **Worker .NET** | Processar posteriormente as notificações pendentes. |
| **PostgreSQL** | Persistir produtos, saldos, movimentações e registros de notificação pendente (*outbox*). |
| **Sistemas externos** | Sistema de Vendas solicita baixas; Provedor de Notificações entrega alertas. |

Essas escolhas **não são recomendações universais** nem evidência de sistemas implantados. Para entender os limites de cada responsabilidade, consulte a [arquitetura de referência detalhada](docs/arquitetura-referencia.md) e as [decisões arquiteturais propostas](docs/decisoes-arquiteturais.md).

## Visualize a arquitetura: Mermaid e LikeC4

**Você não precisa instalar nada para estudar este laboratório.** Há duas formas complementares de explorar o **mesmo Sistema de Gestão de Estoque**:

- **[Ler os diagramas Mermaid no GitHub](docs/01-contexto.md):** siga os capítulos dos quatro níveis, com diagramas embutidos no Markdown e explicações sobre cada decisão de modelagem. É a opção recomendada para quem está começando.
- **[Explorar o site interativo LikeC4](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/):** navegue do **Contexto** aos **Contêineres** e aos **Componentes da API**, ampliando progressivamente a mesma arquitetura. O site também apresenta dois fluxos dinâmicos: registro da saída e entrega do alerta.

**Em dispositivos móveis:** se a visualização interativa não funcionar bem, abra a [versão leve com seis diagramas SVG](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/mobile/). Ela inclui os quatro níveis e dois fluxos de sequência, mas **não** oferece a navegação interativa do LikeC4. Consulte as [limitações de compatibilidade](docs/compatibilidade-mobile.md).

### Qual é a diferença entre Mermaid e LikeC4?

O **C4 é o modelo de arquitetura**, enquanto Mermaid e LikeC4 são ferramentas utilizadas para representá-lo. Elas **não criam sistemas diferentes** neste laboratório.

| Aspecto | Mermaid | LikeC4 |
| --- | --- | --- |
| **Como os diagramas são definidos** | Cada capítulo Markdown contém seu próprio diagrama. | Elementos e relações são definidos em um modelo compartilhado, utilizado por diferentes visões. |
| **Níveis disponíveis aqui** | Contexto, Contêineres, Componentes e Código. | Contexto, Contêineres e Componentes. |
| **Nível 4 (Código)** | Um `classDiagram` mostra um recorte de classes e interfaces C#. | Não há uma visão equivalente de código implementada neste laboratório. |
| **Fluxos dinâmicos** | Diagramas de sequência nos capítulos. | Duas visões dinâmicas que reutilizam os participantes do modelo. |
| **Como explorar** | Leitura guiada e links entre documentos no GitHub. | Navegação visual interativa no site publicado. |

**Como comparar na prática:** leia primeiro o [Contexto em Mermaid](docs/01-contexto.md) e depois abra a visão inicial do [site LikeC4](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/). Observe que os atores, os sistemas externos e a fronteira do sistema continuam os mesmos. Repita o exercício nos níveis de [Contêineres](docs/02-containers.md) e [Componentes](docs/03-componentes.md).

**Importante:** os modelos Mermaid e LikeC4 são mantidos em paralelo; **um não é gerado automaticamente a partir do outro**. A consistência entre os dois precisa ser revisada quando a arquitetura muda. Para entender os critérios de escolha, os trade-offs e as limitações observadas, consulte [Mermaid vs. LikeC4](docs/likec4-vs-mermaid.md).

### Quer executar ou modificar o LikeC4 localmente?

Essa parte é **opcional** para o aprendizado dos níveis C4. Para usar Node.js 22, validar o modelo, abrir a prévia local ou gerar o site, siga os [comandos e requisitos no guia LikeC4](likec4/README.md). A [publicação automatizada](.github/workflows/likec4-pages.yml) e seus detalhes estão explicados no [guia de comparação e publicação](docs/likec4-vs-mermaid.md#processo-de-publicação).

## Manutenção e contribuição

Esta seção é **opcional para quem deseja apenas estudar o C4**. Os detalhes de desenvolvimento e governança estão em [Como contribuir](CONTRIBUTING.md).

### Decisões arquiteturais

As escolhas técnicas são documentadas em [Architecture Decision Records (ADRs)](docs/decisoes-arquiteturais.md): registros que explicam o contexto, a decisão e suas consequências. Os ADRs deste laboratório permanecem com status **Proposed** (propostos), sem aprovação formal.

O workflow [ADR Guard](.github/workflows/adr-guard.yml) verifica a conformidade desses registros. Para validar localmente, use o SDK .NET 10 e a versão da ferramenta declarada em [`.config/dotnet-tools.json`](.config/dotnet-tools.json):

```bash
dotnet tool restore
dotnet tool run adr-guard -- check docs/adr
```

### Qualidade da documentação

O workflow [Documentation Quality](.github/workflows/docs-quality.yml) executa testes, verifica **links e âncoras Markdown locais**, valida o modelo LikeC4 e tenta renderizar os seis diagramas Mermaid. As versões das ferramentas JavaScript são declaradas no [`package.json`](package.json). Links externos não são verificados automaticamente por HTTP.

Para executar os testes e a validação estrutural localmente (Python 3.12+):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_docs.py --output-dir .tmp/mermaid
```

**Atenção:** esses comandos Python não comprovam a renderização visual dos diagramas. O CI usa a Mermaid CLI para gerar SVGs, disponibilizados como artefatos; a inspeção humana das imagens e da coerência arquitetural continua necessária.

O [Dependabot](.github/dependabot.yml) propõe atualizações de GitHub Actions e dependências npm. Para executar ou publicar o site LikeC4, veja o [guia específico](likec4/README.md). Para preparar uma versão documental, consulte o [checklist de publicação](docs/publicacao.md).

## Licença

Distribuído sob a [licença MIT](LICENSE). © 2026 Rodrigo de Oliveira.
