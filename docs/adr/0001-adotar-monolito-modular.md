# Adotar um monólito modular para o núcleo de estoque

## Status

Proposed

## Context

O laboratório precisa demonstrar a progressão entre contexto, contêineres, componentes e classes sem introduzir complexidade de distribuição que não faça parte do problema de negócio. O sistema concentra cadastro de produtos, saldos e movimentações; essas operações precisam de consistência transacional e regras coesas. Consideramos dividir o domínio em microsserviços desde o início ou concentrar o núcleo de estoque em um serviço modular.

## Decision

Adotar uma API de estoque como monólito modular, organizada internamente por responsabilidades de entrada, aplicação, domínio e infraestrutura. A aplicação web e o worker de notificações serão contêineres separados por necessidades operacionais distintas. A decisão não exige múltiplas soluções ou projetos .NET para representar cada módulo.

## Consequences

A fronteira transacional permanece simples, e o nível 3 poderá mostrar componentes internos da API sem pressupor chamadas remotas entre funcionalidades de estoque. A evolução didática exige menos infraestrutura e menos contratos distribuídos.

Por outro lado, o serviço concentra implantação e escalabilidade do núcleo. Uma separação posterior exigiria identificar limites de domínio, contratos, dados e dependências. A modularidade deve ser preservada por disciplina de código e revisões, já que o desenho não a garante automaticamente.
