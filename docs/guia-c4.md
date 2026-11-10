# Convenções do C4 e Mermaid

## 1. Objetivo

Mostrar a mesma arquitetura com diferentes níveis de abstração, sem confundir conceitos de negócio, unidades executáveis, componentes e classes.

## 2. Notação planejada

| Nível | Mermaid | Escopo |
| --- | --- | --- |
| 1 | [`C4Context`](01-contexto.md) | Operador, gestor, sistema de estoque e sistemas externos |
| 2 | [`C4Container`](02-containers.md) | Web, API, worker, PostgreSQL e sistemas externos |
| 3 | `C4Component` | Componentes **da API**, dentro do contêiner escolhido |
| 4 | `classDiagram` | Recorte das classes C# do caso de uso de saída |

**Atenção:** o suporte do Mermaid a C4 é experimental e a apresentação pode variar conforme a versão e o renderizador. `classDiagram` representa o nível de código neste laboratório, mas não é uma sintaxe C4 específica. A validação automatizada e a escolha da versão do renderizador serão abordadas na etapa 7.

Referências:
- [Modelo C4, site oficial](https://c4model.com/)
- [Documentação Mermaid: C4 Diagrams](https://mermaid.js.org/syntax/c4.html)
- [Documentação Mermaid: Class Diagrams](https://mermaid.js.org/syntax/classDiagram.html)
- [Diagramas Mermaid no GitHub](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)

## 3. Regras de consistência

1. **Mesmo sistema:** usar o nome `Sistema de Gestão de Estoque` em todos os níveis.
2. **Mesmas integrações:** sistema de vendas e provedor de notificações permanecem externos.
3. **Relações explícitas:** cada seta deve indicar direção, propósito e, quando útil, o protocolo.
4. **Responsabilidades claras:** a API executa regras; o worker entrega alertas; o banco persiste dados.
5. **Sem nível implícito:** código não deve aparecer no contexto; classes não devem substituir componentes.
6. **Zoom definido:** o nível 3 examina **somente a API**; o nível 4 aprofunda a operação de saída.
7. **Cenário constante:** manter a movimentação de 10 unidades como fio condutor.
8. **Não exagerar a arquitetura:** não incluir broker, cache, gateway ou microsserviços sem necessidade explícita.

## 4. Exemplo disponível

O [diagrama do nível 1](01-contexto.md) utiliza `C4Context` com um único sistema central, duas pessoas e duas integrações externas. O [diagrama do nível 2](02-containers.md) amplia **o mesmo sistema** com quatro contêineres internos. As descrições e tabelas que acompanham o Mermaid são parte da documentação: os diagramas não substituem contexto e justificativas arquiteturais.

## 5. Formato dos documentos futuros

Cada capítulo de nível deverá conter:

- Objetivo, público-alvo e pergunta que o diagrama responde.
- Fronteira do nível e elementos representados.
- Diagrama Mermaid embutido no Markdown para renderização no GitHub.
- Explicação das relações e decisões relevantes.
- Conexão com o capítulo anterior e com o próximo.
- Limitações: o que o diagrama deliberadamente omite.

## 6. Fonte de verdade e versionamento

Os **blocos Mermaid nos capítulos Markdown** serão a fonte editável e renderizável no GitHub. Se forem necessários arquivos `.mmd` independentes em `diagrams/`, eles devem ser extraídos desses blocos, para evitar divergência entre duas cópias mantidas manualmente. A extração e a validação ficarão para a etapa 7.

Exemplos em C# também serão documentais. O repositório não deve exigir a execução de uma aplicação para que os níveis possam ser compreendidos.
