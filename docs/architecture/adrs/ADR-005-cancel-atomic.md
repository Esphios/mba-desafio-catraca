# ADR-005 | Cancelamento transacional

Status: proposto | 26/11/2026 | Autor: planejamento inicial; aprovação no kickoff.

## Contexto
R11 exige irreversibilidade e até 10 s; estados terminais precisam dominar callback.

## Decisão
Cancelar evento e mudar tickets em um commit; worker ignora terminal; preservar timestamp de check-in.

## Alternativas e trade-offs
Compensação assíncrona de estorno exigiria janela inconsistente; pagamento real fora de escopo.

## Consequências
Transação pode conter muitos tickets; medir duração na escala do MVP.

## Validação
A12,A26,A27,X12,X15. Ver `requirements-matrix.md` na raiz; resultados pendentes.

## Ciclo de vida
Após aprovação humana, marcar accepted com data. Se substituída, criar novo ADR que referencie este e marcar superseded, preservando histórico. Não reescrever motivação passada. Referências: `design.md`, `docs/architecture/transactions.md`, `docs/architecture/research.md`.
