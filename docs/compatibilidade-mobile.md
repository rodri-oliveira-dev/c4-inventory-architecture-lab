# Compatibilidade mobile do site LikeC4

O [site de arquitetura](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/) usa a interface interativa do LikeC4 para contexto, contêineres, componentes e fluxos. Foi observado no iPhone um encerramento repetido da página no navegador embutido do ChatGPT, antes de ser possível explorar o modelo. **Esse sintoma não identifica por si só a causa**: pode estar associado a recursos do processo WebKit, memória ou um defeito de renderização específico. Não há registro de console ou reprodução automatizada num iPhone para estabelecer diagnóstico definitivo.

## Alternativa de baixo consumo

O endereço [**/mobile/**](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/mobile/) disponibiliza uma página **sem JavaScript** com seis diagramas SVG:

| Seção | Fonte original |
| --- | --- |
| Contexto (C4 nível 1) | [`01-contexto.md`](01-contexto.md) |
| Contêineres (C4 nível 2) | [`02-containers.md`](02-containers.md) |
| Componentes (C4 nível 3) | [`03-componentes.md`](03-componentes.md) |
| Código (C4 nível 4) | [`04-codigo.md`](04-codigo.md) |
| Baixa síncrona | [`fluxo-movimentacao.md`](fluxo-movimentacao.md) |
| Outbox e entrega eventual | [`fluxo-movimentacao.md`](fluxo-movimentacao.md) |

Os SVGs são gerados a cada build a partir dos **blocos Mermaid existentes**. Não existe um segundo modelo de estoque nem imagens estáticas mantidas manualmente. Cada diagrama oferece um link para abri-lo isoladamente e ampliar com os controles do navegador.

A interface leve **não substitui o LikeC4**: não apresenta drill-down interativo, informações contextuais sob demanda nem as duas `dynamic views` nativas. É uma alternativa de leitura quando o navegador não consegue executar a aplicação principal.

## Como a seleção funciona

- **iPhone e iPad em telas até 820 CSS px**: um script mínimo no início do `index.html` redireciona para `/mobile/` **antes dos bundles interativos**. Se o endereço original contiver uma das IDs de visão na hash, a alternativa tenta posicionar na seção correspondente.
- **Outros aparelhos e desktop**: a aplicação LikeC4 original continua sendo carregada normalmente.
- **Forçar a experiência completa no iPhone**: abrir [`/?full=1#/`](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/?full=1#/) ou usar o link na página leve. Esse parâmetro desativa o redirecionamento; o navegador pode continuar apresentando a falha original.
- **Acesso direto à versão leve**: [`/mobile/`](https://rodri-oliveira-dev.github.io/c4-inventory-architecture-lab/mobile/), inclusive em Android e desktop, sem depender de detecção de dispositivo.

O parâmetro `utm_source` que pode aparecer em links compartilhados é independente da seleção da versão leve.

## Testes automatizados e limitações

O [workflow LikeC4 Site](../.github/workflows/likec4-pages.yml) agora:

1. Executa testes Python da geração da página leve e da injeção antecipada.
2. Valida a DSL e compila o site LikeC4 normalmente.
3. Reutiliza `scripts/validate_docs.py` para extrair os seis blocos Mermaid e os renderiza em SVG com a versão fixada de Mermaid CLI.
4. Gera `dist/mobile/index.html`, injeta a detecção de iOS em `dist/index.html` e verifica que os seis SVGs foram criados.
5. Em PRs, publica somente o artefato de prévia; em `main`, implanta os dois modos no GitHub Pages.

O CI valida a geração, os arquivos e a presença do redirecionamento, **mas não emula WebKit nem comprova que o erro desapareceu no iPhone**. Após o deploy, é importante testar três cenários em um iPhone real: abrir o site pelo navegador do ChatGPT, abri-lo diretamente no Safari e selecionar o modo interativo com `?full=1`. Se o erro persistir até na página leve, investigar rede, extensões, cache e possíveis particularidades do navegador.

O [projeto LikeC4](../likec4/README.md) e os diagramas originais permanecem inalterados.
