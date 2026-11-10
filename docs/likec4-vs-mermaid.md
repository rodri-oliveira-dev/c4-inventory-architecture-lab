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

## As cinco visões publicadas

O site estático é publicado pelo workflow [LikeC4 Site](../.github/workflows/likec4-pages.yml), com as seguintes visualizações:

1. `index`: Contexto do sistema.
2. `conteineres`: Web, API, worker e PostgreSQL.
3. `componentes`: cinco componentes internos da API.
4. `registrarSaida`: saída de 10 unidades de `SKU-001`, saldo 15 → 5, com commit antes da resposta.
5. `entregarAlerta`: processamento posterior da outbox e alternativa de falha/timeout.

Endereço previsto após o deploy: [**Site interativo LikeC4**](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/). A existência desse endereço deve ser confirmada após o merge, execução do deploy e configuração da fonte do GitHub Pages.

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

- [Publicação de site estático no LikeC4](https://likec4.dev/pt-br/guides/static-website/)
- [LikeC4 no GitHub Pages](https://likec4.dev/pt-br/guides/deploy-github-pages/)
- [GitHub Docs: publicação via Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
