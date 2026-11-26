# ADR-004 | Snapshot monetário e estado derivado

Status: proposto | 26/11/2026 | Autor: planejamento inicial; aprovação no kickoff.

## Contexto
R12 precisa somar preço da compra, não preço atual; check-in não é status.

## Decisão
Centavos inteiros imutáveis em ticket; checked_in_at independente; painel agrega apenas confirmed.

## Alternativas e trade-offs
Preço via join com evento distorce histórico; contador de receita duplicado pode divergir.

## Consequências
Leitura agregada em banco; índices necessários.

## Validação
A11,A27,X13. Ver `requirements-matrix.md` na raiz; resultados pendentes.

## Ciclo de vida
Após aprovação humana, marcar accepted com data. Se substituída, criar novo ADR que referencie este e marcar superseded, preservando histórico. Não reescrever motivação passada. Referências: `design.md`, `docs/architecture/transactions.md`, `docs/architecture/research.md`.
