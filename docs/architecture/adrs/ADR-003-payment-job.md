# ADR-003 | Fila durável no banco

Status: proposto | 26/11/2026 | Autor: planejamento inicial; aprovação no kickoff.

## Contexto
Compra responde antes de gateway; falha entre ticket e agendamento não pode perder job.

## Decisão
Persistir job com due_at/outcome no commit da reserva; worker revalida estado após lock.

## Alternativas e trade-offs
Sleep na requisição viola R06; timer em memória se perde; broker externo exigiria outbox.

## Consequências
Polling e latência devem ser medidos; recuperação após restart.

## Validação
A13,A15,A16,X04. Ver `requirements-matrix.md` na raiz; resultados pendentes.

## Ciclo de vida
Após aprovação humana, marcar accepted com data. Se substituída, criar novo ADR que referencie este e marcar superseded, preservando histórico. Não reescrever motivação passada. Referências: `design.md`, `docs/architecture/transactions.md`, `docs/architecture/research.md`.
