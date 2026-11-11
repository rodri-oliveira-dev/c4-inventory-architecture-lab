#!/usr/bin/env python3
"""Create a JavaScript-free mobile companion and an early iOS fallback redirect.

The Mermaid diagrams are rendered to SVG by the GitHub Actions workflow.
No user-generated HTML or JavaScript is embedded in the lightweight page.
"""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import re

PAGES_BASE = "/c4-inventory-architecture-lab/"
REDIRECT_MARKER = "data-mobile-fallback"
VIEWS = (
    ("contexto", "Nível 1 · Contexto", "docs--01-contexto-01.svg",
     "Pessoas, sistema de estoque e integrações externas."),
    ("conteineres", "Nível 2 · Contêineres", "docs--02-containers-01.svg",
     "Aplicação Web, API de Estoque, worker e PostgreSQL."),
    ("componentes", "Nível 3 · Componentes", "docs--03-componentes-01.svg",
     "Responsabilidades internas da API ASP.NET Core."),
    ("codigo", "Nível 4 · Código", "docs--04-codigo-01.svg",
     "Classes e interfaces C# do caso de uso RegistrarSaida, em UML Mermaid."),
    ("registrarSaida", "Fluxo · Baixa de estoque", "docs--fluxo-movimentacao-01.svg",
     "Saída de 10 unidades, saldo de 15 para 5 e commit antes da resposta."),
    ("entregarAlerta", "Fluxo · Notificação", "docs--fluxo-movimentacao-02.svg",
     "Worker, outbox e envio eventual com possibilidade de retry."),
)

# This runs before the Vite JavaScript bundles, preventing costly initialization
# in small-screen iOS browsers where the interactive viewer may crash.
EARLY_REDIRECT = """<script data-mobile-fallback="true">
(function () {
  try {
    var ua = navigator.userAgent || '';
    var ios = /iPhone|iPad|iPod/i.test(ua) ||
      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    var compact = window.matchMedia('(max-width: 820px)').matches;
    var full = new URLSearchParams(window.location.search).get('full') === '1';
    if (!ios || !compact || full) return;
    var hash = window.location.hash || '';
    var names = ['conteineres', 'componentes', 'registrarSaida', 'entregarAlerta', 'index'];
    var target = '';
    for (var i = 0; i < names.length; i++) {
      if (hash.indexOf(names[i]) !== -1) {
        target = names[i] === 'index' ? 'contexto' : names[i];
        break;
      }
    }
    window.location.replace('/c4-inventory-architecture-lab/mobile/' +
      (target ? '#' + target : ''));
  } catch (e) {
    // If detection is unavailable, keep the original LikeC4 experience.
  }
})();
</script>"""


def inject_fallback(index: str) -> str:
    """Inject once, immediately after <head>, before the app's module scripts."""
    if REDIRECT_MARKER in index:
        return index
    match = re.search(r"<head(?:\s[^>]*)?>", index, flags=re.IGNORECASE)
    if not match:
        raise ValueError("LikeC4 index.html has no <head> element")
    return index[: match.end()] + "\n" + EARLY_REDIRECT + "\n" + index[match.end() :]


def mobile_html() -> str:
    navigation = " ".join(
        f'<a href="#{escape(key)}">{escape(title)}</a>' for key, title, _, _ in VIEWS
    )
    diagrams = "\n".join(
        f"""<section id="{escape(key)}" class="card">
  <h2>{escape(title)}</h2>
  <p>{escape(description)}</p>
  <div class="diagram"><img loading="lazy" decoding="async"
    src="diagrams/{escape(filename)}" alt="{escape(title)}: {escape(description)}"></div>
  <a class="detail" href="diagrams/{escape(filename)}" target="_blank" rel="noopener">
    Abrir diagrama ampliado
  </a>
</section>"""
        for key, title, filename, description in VIEWS
    )
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="description" content="Visão leve para celulares dos quatro níveis C4 e fluxos do laboratório de arquitetura de estoque.">
  <title>C4 Inventory Architecture Lab · Visão leve</title>
  <style>
    :root {{ color-scheme: light dark; font-family: system-ui, -apple-system, sans-serif; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; line-height: 1.55; background: light-dark(#f6f7fb, #17191d); color: light-dark(#222733, #e8eaf0); }}
    header {{ padding: 1.25rem 1rem 1rem; background: light-dark(#e6eafa, #242b39); }}
    h1 {{ margin: 0 0 .4rem; font-size: clamp(1.35rem, 5vw, 2rem); }}
    h2 {{ margin: 0 0 .3rem; font-size: 1.15rem; }}
    p {{ margin: .45rem 0 .85rem; }}
    .intro {{ font-size: .95rem; max-width: 68ch; }}
    nav {{ display: flex; gap: .5rem; overflow-x: auto; padding: .85rem 1rem; scrollbar-width: thin; }}
    a {{ color: light-dark(#2554ae, #a9c2ff); }}
    nav a {{ display: inline-block; flex: 0 0 auto; padding: .35rem .7rem; border: 1px solid currentColor; border-radius: 1rem; text-decoration: none; font-size: .86rem; }}
    main {{ max-width: 1040px; margin: auto; padding: 0 1rem 2rem; }}
    .card {{ background: light-dark(white, #22252b); padding: 1rem; border-radius: 1rem; margin: .9rem 0; box-shadow: 0 2px 9px #0001; scroll-margin-top: 1rem; }}
    .diagram {{ width: 100%; overflow-x: auto; background: #fff; border: 1px solid #d7dbe4; border-radius: .5rem; }}
    .diagram img {{ display: block; width: auto; max-width: none; min-width: 100%; height: auto; }}
    .detail {{ display: inline-block; margin-top: .8rem; font-weight: 600; }}
    .footer {{ padding: 1rem; text-align: center; font-size: .85rem; }}
    @media (min-width: 800px) {{ .diagram img {{ max-width: 100%; }} }}
  </style>
</head>
<body>
<header>
  <h1>C4 Inventory Architecture Lab</h1>
  <p class="intro"><strong>Visão leve para celulares.</strong> Diagramas pré-renderizados em SVG,
  sem executar a aplicação interativa. O conteúdo permanece didático e usa a
  documentação Mermaid existente; as visões navegáveis LikeC4 estão no modo completo.</p>
  <p><a href="../?full=1#/" rel="noopener">Tentar abrir o LikeC4 interativo</a>
  · <a href="https://github.com/rodri-oliveira-dev/c4-inventory-architecture-lab/tree/main/docs">Ler documentação no GitHub</a></p>
</header>
<nav aria-label="Escolha um diagrama">{navigation}</nav>
<main>
{diagrams}
</main>
<footer class="footer">Arquitetura demonstrativa · Sem API de estoque em produção</footer>
</body>
</html>
"""


def create_mobile_site(site_dir: Path) -> None:
    site = site_dir.resolve()
    index_file = site / "index.html"
    if not index_file.is_file():
        raise FileNotFoundError(f"LikeC4 index.html missing: {index_file}")
    images = site / "mobile" / "diagrams"
    missing = [name for _, _, name, _ in VIEWS if not (images / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Mobile SVG diagrams missing: {', '.join(missing)}")
    mobile_index = site / "mobile" / "index.html"
    mobile_index.write_text(mobile_html(), encoding="utf-8")
    existing = index_file.read_text(encoding="utf-8")
    index_file.write_text(inject_fallback(existing), encoding="utf-8")
    print(f"Mobile fallback available at {PAGES_BASE}mobile/ ({len(VIEWS)} static SVG diagrams).")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", required=True, type=Path)
    options = parser.parse_args()
    create_mobile_site(options.site_dir)


if __name__ == "__main__":
    main()
