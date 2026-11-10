# Usar ASP.NET Core, C# e .NET 10 na API de estoque

## Status

Proposed

## Context

O repositório tem caráter educacional e não pretende oferecer uma aplicação pronta. O nível 4 precisa representar classes, interfaces e casos de uso de maneira reconhecível para quem desenvolve aplicações corporativas. Avaliamos usar pseudocódigo independente de linguagem ou selecionar uma stack concreta para ilustrar contratos e responsabilidades.

## Decision

Usar ASP.NET Core e C#/.NET 10 como tecnologias de referência da API de estoque e do worker. Representar o comportamento em exemplos pequenos de C# quando o laboratório chegar ao nível 4. Nenhum runtime ou implantação real será exigido para compreender os diagramas.

## Consequences

A concretude dos tipos e interfaces reduz ambiguidades no diagrama de classes e facilita conectar o nível 3 ao nível 4. .NET 10 permite empregar convenções atuais do ecossistema.

A escolha restringe a neutralidade tecnológica e pode requerer atualização de exemplos no futuro. Como a aplicação não será implementada integralmente, os exemplos não substituem testes de integração nem atestam prontidão para produção.
