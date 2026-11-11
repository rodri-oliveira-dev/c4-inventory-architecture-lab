# Mermaid e LikeC4: duas formas de comunicar a mesma arquitetura

Este laboratório representa um **único Sistema de Gestão de Estoque** em duas abordagens: capítulos Markdown com diagramas Mermaid e um [modelo LikeC4](../likec4/README.md) compartilhado. A arquitetura é didática; não há aplicação .NET executável nem infraestrutura de produção.

## Comparação por objetivo

| Aspecto | Mermaid | LikeC4 |
| --- | --- | --- |
| Fonte dos diagramas | Cada bloco `mermaid` no Markdown define sua representação. | Elementos e relações declarados em `model.c4`, projetados nas visões. |
| Contexto (C4 L1) | [`C4Context`](01-contexto.md) | `index`, com sistema, pessoas e integrações. |
| Contêineres (C4 L2) | [`C4Container`](02-containers.md) | `conteineres`, ampliando a fronteira de `estoque`. |
| Componentes (C4 L3) | [`C4Component`](03-componentes.md) | `componentes`, abrindo apenas `estoque.api`. |
| Código (C4 L4) | [`classDiagram`](04-codigo.md) com classes e interfaces C#. | **Mantido em Mermaid**: LikeC4 não substitui a representação UML de métodos/atributos. |
| Fluxos | Dois [`sequenceDiagram`](fluxo-movimentacao.md), com mensagens e alternativas. | `registrarSaida` e `entregarAlerta`, visões dinâmicas com participantes do modelo. |
| Navegação | Índice de documentos e links entre capítulos no GitHub. | Site interativo com navegação entre as cinco visões. |
| Validação | Extração, links locais e renderização em SVG no Documentation Quality. | `likec4 validate` e build de site no LikeC4 Site CI. |
| Publicação | Markdown é renderizado diretamente pelo GitHub. | GitHub Pages com build estático do LikeC4. |

**O principal benefício do LikeC4 é evitar repetição das definições** nas visões 1 a 3. A vantagem do Mermaid é a proximidade com o Markdown e a variedade de diagramas, em particular o UML de classes.

## Trade-offs e critérios de decisão

Esta comparação distingue **o que foi observado neste repositório** de **tendências qualitativas** que dependem da equipe e do contexto. Ela não é um benchmark de produtividade, de renderização ou de custo. Não medimos horas de implementação, quantidade de defeitos, tempo de build, acessibilidade ou satisfação dos leitores.

### Matriz de trade-offs

| Critério | Vantagem potencial do Mermaid | Vantagem potencial do LikeC4 | Custo ou restrição a considerar |
| --- | --- | --- | --- |
| **Entrada e curva de aprendizado** | Diagramas pequenos podem ser escritos no próprio Markdown, sem aprender o modelo completo. | DSL orientada a elementos, relações e visões, com vocabulário consistente. | LikeC4 requer entender especificação, escopos e predicados; Mermaid também possui sintaxes específicas por diagrama. **Avaliação qualitativa**, não medida com usuários. |
| **Fonte de verdade dentro da ferramenta** | Cada diagrama fica próximo da explicação textual e pode evoluir isoladamente. | Elementos e relações de níveis 1–3 são definidos em [`model.c4`](../likec4/model.c4) e reutilizados nas visões. | Mermaid pode repetir descrições; LikeC4 exige disciplina para manter o modelo semanticamente correto. **Verificado na estrutura do laboratório.** |
| **Consistência entre níveis** | Dá liberdade para simplificar ou adaptar cada representação ao público. | Uma alteração no modelo pode refletir automaticamente nas visões derivadas. | Reutilização **não garante** que relações, responsabilidades ou níveis tenham sido modelados corretamente. **Verificado no desenho e validação da DSL, não no comportamento de manutenção de longo prazo.** |
| **Mudanças localizadas** | Um pequeno ajuste de classe ou fluxo pode afetar apenas um bloco Mermaid. | Uma alteração de elemento central fica concentrada no modelo, beneficiando múltiplas vistas. | Centralizar pode ampliar o impacto de uma alteração incorreta. Convém revisar todas as visões afetadas. **Avaliação arquitetural.** |
| **Modelos grandes** | Permite separar diagramas por arquivo ou capítulo sem introduzir estrutura global. | Hierarquia e visões com escopo favorecem exploração progressiva de arquiteturas maiores. | Nenhuma das ferramentas foi submetida a um modelo grande neste laboratório. **Hipótese de escalabilidade, não benchmark.** |
| **C4 Contexto, Contêineres e Componentes** | `C4Context`, `C4Container` e `C4Component` estão embutidos nos capítulos. | `index`, `conteineres` e `componentes` são projeções da mesma arquitetura. | A sintaxe C4 do Mermaid é oficialmente **experimental**; as duas abordagens exigem revisão de fronteiras. **Ambas implementadas neste projeto.** |
| **Nível 4: classes e contratos C#** | `classDiagram` mostra atributos, métodos, interfaces e dependências UML. | É possível aprofundar o modelo com elementos customizados e outra visão estrutural. | **Não há equivalente direto a um `classDiagram` UML completo no modelo atual do LikeC4**. O nível 4 LikeC4 **não foi implementado nem comparado visualmente** neste laboratório. |
| **Fluxos temporais** | `sequenceDiagram` oferece uma notação dedicada, adequada a mensagens, retornos e alternativas. | Visões `dynamic` reutilizam participantes identificados no modelo. | Fluxos podem requerer detalhamento diferente; blocos de controle dinâmico do LikeC4 possuem recursos **experimentais**. **Ambos implementados para baixa e outbox.** |
| **Navegação e público** | Leitura direta de capítulos no GitHub, útil para revisão textual e diffs de PR. | Site interativo permite navegar Contexto → Contêineres → Componentes e abrir fluxos. | Interatividade depende do site ou ambiente LikeC4; os diagramas Mermaid permanecem mais próximos do texto. **Publicado e validado no CI; usabilidade não medida.** |
| **Build e distribuição** | O GitHub renderiza Markdown; o CI também produz SVGs com Mermaid CLI. | O LikeC4 gera um site estático e artefato de prévia em PR. | LikeC4 exige build e deploy específicos; Mermaid CLI traz dependências de renderização. **Ambos os pipelines passaram no projeto.** |
| **Dependência tecnológica e portabilidade** | O formato é texto Markdown, com renderização compatível em vários ambientes que suportam Mermaid. | A DSL centraliza a arquitetura e pode ser versionada como código. | `.c4` requer ferramentas compatíveis com LikeC4; Markdown não garante renderização Mermaid idêntica em todos os ambientes/versões. **Comparação qualitativa.** |
| **Revisão e governança** | Mudanças de texto e blocos são avaliadas juntas no mesmo PR. | A revisão separa declarações do modelo e critérios de visibilidade das vistas. | A validação sintática de ambas as ferramentas **não verifica a equivalência semântica** entre Mermaid e LikeC4. É necessária uma conferência humana. **Limitação observada na automação.** |

**Interpretação:** não há vencedor universal. A escolha depende da quantidade de relações compartilhadas, do detalhamento desejado, do público, da necessidade de navegação e do custo de manter o pipeline e o conteúdo coerentes.

### O que o laboratório efetivamente demonstrou

- **Reutilização estrutural:** um único [modelo LikeC4](../likec4/model.c4) alimenta três [visões estáticas](../likec4/views.c4), que agregam relações entre níveis sem redeclará-las por diagrama. As [duas visões dinâmicas](../likec4/dynamics.c4) referenciam participantes desse mesmo modelo, mas descrevem mensagens próprias do cenário.
- **Documentação especializada em Mermaid:** os níveis [1](01-contexto.md), [2](02-containers.md), [3](03-componentes.md) e [4](04-codigo.md) e as [duas sequências](fluxo-movimentacao.md) são mantidos em blocos Markdown. O `classDiagram` preserva o detalhamento de tipos C# que não foi reproduzido em LikeC4.
- **Publicação automatizada:** [Documentation Quality](../.github/workflows/docs-quality.yml) verifica links Markdown e renderiza os diagramas Mermaid; [LikeC4 Site](../.github/workflows/likec4-pages.yml) valida a DSL, gera artefatos de prévia e publica o site. O [ADR Guard](../.github/workflows/adr-guard.yml) valida os registros de decisões arquiteturais.
- **Não foi demonstrado:** redução quantitativa de esforço, vantagem de performance, equivalência automática entre as duas fontes, nível 4 em LikeC4, fidelidade visual sistematicamente revisada ou adequação a uma arquitetura muito maior.

Essas constatações são **evidências do repositório e dos workflows**, não resultados de um estudo controlado entre ferramentas.

### Quando escolher cada abordagem

**Mermaid como abordagem principal** faz sentido quando o objetivo é manter documentação centrada em Markdown, produzir diagramas pontuais ou representar classes C# com métodos e atributos. A equipe aceita manter relações repetidas em diferentes capítulos e revisá-las manualmente. Convém lembrar que a família C4 do Mermaid ainda é experimental, apesar de o `classDiagram` ser uma notação distinta e específica.

**LikeC4 como abordagem principal** faz sentido quando os mesmos atores, sistemas e relacionamentos aparecem em muitas visões e a equipe quer um modelo estruturado com exploração interativa. O investimento em DSL, validação e publicação pode compensar a repetição evitada, mas esse benefício precisa ser reavaliado conforme a escala real e a maturidade da equipe.

**Abordagem híbrida** faz sentido quando cada ferramenta cobre uma necessidade distinta: LikeC4 como representação estrutural e navegável dos níveis 1–3, Mermaid para UML de classes no nível 4 e, se útil, sequências ricas em detalhes. O trade-off é manter **duas fontes de documentação sobre uma mesma arquitetura**, sem sincronização automática entre as ferramentas.

### Decisão adotada neste laboratório

**Manter Mermaid + LikeC4 em paralelo com responsabilidades explícitas.** O LikeC4 concentra os elementos estruturais compartilhados e oferece navegação no [site publicado](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/); os capítulos Mermaid preservam o detalhamento textual, as sequências e a visão UML de código. Isso permite comparação didática **sem afirmar que uma DSL substitui integralmente a outra**.

O custo aceito é a **sincronização editorial manual**. Para reduzir divergência, qualquer PR que mude ator, fronteira, relacionamento, tecnologia ou regra funcional deve revisar o modelo LikeC4, as vistas impactadas, os diagramas Mermaid e, quando necessário, os ADRs. As verificações automatizadas devem passar, mas o autor e o revisor continuam responsáveis pela consistência **semântica**.

### Limites da conclusão e próxima hipótese

O [nível 4 Mermaid](04-codigo.md) tem classes e interfaces C# ilustrativas. Como **não existe visão de código no LikeC4 deste laboratório**, não é correto dizer que avaliamos empiricamente a comparação visual do nível 4. Um experimento futuro pode adicionar classes e interfaces como tipos de elementos customizados em LikeC4 e comparar clareza das dependências, manutenção, legibilidade e utilidade para revisão. Isso seria **complementar**, não uma promessa de equivalência com UML.

Não há métricas objetivas suficientes para classificar uma abordagem como mais rápida, barata ou simples em qualquer equipe. Para uma comparação quantitativa futura, seria necessário definir tarefas equivalentes e medir tempo de alteração, retrabalho, divergências detectadas, tempo de build e feedback de leitores.

## As cinco visões publicadas

O site estático é publicado pelo workflow [LikeC4 Site](../.github/workflows/likec4-pages.yml), com as seguintes visualizações:

1. `index`: Contexto do sistema.
2. `conteineres`: Web, API, worker e PostgreSQL.
3. `componentes`: cinco componentes internos da API.
4. `registrarSaida`: saída de 10 unidades de `SKU-001`, saldo 15 → 5, com commit antes da resposta.
5. `entregarAlerta`: processamento posterior da outbox e alternativa de falha/timeout.

**Site interativo publicado:** [C4 Inventory Architecture Lab no GitHub Pages](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/). O deploy da etapa 5 foi concluído com sucesso pelo [workflow LikeC4 Site](https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/actions/runs/42922493495).

## Consistência e governança

**As fontes continuam distintas nesta etapa.** Mermaid e LikeC4 não são gerados um a partir do outro automaticamente. Ao alterar um relacionamento, ator, contêiner ou regra de estoque, revisar os dois conjuntos de diagramas e os ADRs relacionados no mesmo PR.

O LikeC4 reutiliza os mesmos IDs do seu modelo nas visões estáticas e dinâmicas, mas **mensagens temporais** não criam novas dependências estáticas.

O cenário deve permanecer coerente: produto `SKU-001`, saldo inicial **15**, baixa **10**, saldo final **5**, limite **5**, referência de origem `V-100`, outbox dentro da mesma transação, reenvios possíveis do provedor e ausência de garantia `exactly once`.

## Processo de publicação

- **Pull request:** o job `Build LikeC4 site` sempre executa a validação e o build, sem publicar; o artefato `likec4-site-preview` permite baixar a versão produzida.
- **Merge na `main`:** quando há alteração em `likec4/`, `package.json` ou no próprio workflow, o build executa e o job separado de deploy publica o site no GitHub Pages.
- **Execução manual:** `workflow_dispatch` permite reconstruir/publicar a versão atual da `main`, por exemplo após habilitar o GitHub Pages.

O build usa `--base /c4-inventory-architecture-lab/` para corrigir os caminhos de assets num Pages de projeto e `--use-hash-history` para permitir links diretos sem configurar redirecionamento de SPA.

É preciso configurar uma única vez **Settings → Pages → Build and deployment → Source: GitHub Actions**. Sem essa opção, o build pode passar sem que o site fique publicado. O workflow usa as permissões mínimas necessárias apenas no job de publicação: `pages: write` e `id-token: write`.

Para validação local (Node.js 22):

```bash
npm install
npm run likec4:validate
npm run likec4:build:pages
```

O conteúdo do site é gerado em `dist/` na raiz, ignorado pelo Git. Os arquivos do diretório não precisam ser versionados.

### Referências

- [Mermaid: diagramas C4 e status experimental](https://mermaid.js.org/syntax/c4.html)
- [Mermaid: diagramas UML de classes](https://mermaid.js.org/syntax/classDiagram.html)
- [LikeC4: visões e predicados](https://likec4.dev/dsl/views/predicates/)
- [LikeC4: visões dinâmicas e blocos de controle](https://likec4.dev/dsl/views/dynamic/)
- [Publicação de site estático no LikeC4](https://likec4.dev/pt-br/guides/static-website/)
- [LikeC4 no GitHub Pages](https://likec4.dev/pt-br/guides/deploy-github-pages/)
- [GitHub Docs: publicação via Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
