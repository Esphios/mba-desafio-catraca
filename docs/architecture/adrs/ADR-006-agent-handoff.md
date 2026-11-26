# ADR-006 | Contratos, branches e avaliação independente

Status: proposto | 26/11/2026 | Autor: planejamento inicial; aprovação no kickoff.

## Contexto
Agente implementador não pode atestar o próprio trabalho.

## Decisão
Baseline de interfaces antes de W5; branches distintas, avaliador contexto novo e relatórios append-only; integração serial.

## Alternativas e trade-offs
Agente único ou relatório atualizado in-place destrói independência e auditabilidade.

## Consequências
Mais trabalho de coordenação; histórico preservado.

## Validação
P01,P02,P03,P04,P05,P06. Ver `requirements-matrix.md` na raiz; resultados pendentes.

## Ciclo de vida
Após aprovação humana, marcar accepted com data. Se substituída, criar novo ADR que referencie este e marcar superseded, preservando histórico. Não reescrever motivação passada. Referências: `design.md`, `docs/architecture/transactions.md`, `docs/architecture/research.md`.
