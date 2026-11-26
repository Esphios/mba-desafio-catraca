# ADR-002 | Lock por evento como protocolo comum

Status: proposto | 26/11/2026 | Autor: planejamento inicial; aprovação no kickoff.

## Contexto
R07 e R03 compartilham estado sob concorrência; R11 pode competir com gateway e venda.

## Decisão
READ COMMITTED; lock do evento e contagem em comando posterior; event→ticket→job.

## Alternativas e trade-offs
Mutex de processo não cobre processos; SERIALIZABLE exige retry; contador materializado exige sincronização adicional.

## Consequências
Serializa por evento, não globalmente; contenção por evento em picos.

## Validação
A11,A14,A24,A25,A26,X05. Ver `requirements-matrix.md` na raiz; resultados pendentes.

## Ciclo de vida
Após aprovação humana, marcar accepted com data. Se substituída, criar novo ADR que referencie este e marcar superseded, preservando histórico. Não reescrever motivação passada. Referências: `design.md`, `docs/architecture/transactions.md`, `docs/architecture/research.md`.
