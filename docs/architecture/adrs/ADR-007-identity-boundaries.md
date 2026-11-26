# ADR-007 | Sessão web e chave de parceiro separadas

Status: proposto | 26/11/2026 | Autor: planejamento inicial; aprovação no kickoff.

## Contexto
Atores têm permissões distintas, e R13 exige proteção direta por ID.

## Decisão
Guarda por papel/dono no servidor, sessão Django e chave isolada; parceiro sem vínculo de conta.

## Alternativas e trade-offs
Autorização só na UI ou e-mail como identidade falha contra acesso direto.

## Consequências
Dois mecanismos claros; testes de auth em cada rota.

## Validação
A06,A07,A20,A23,A28. Ver `requirements-matrix.md` na raiz; resultados pendentes.

## Ciclo de vida
Após aprovação humana, marcar accepted com data. Se substituída, criar novo ADR que referencie este e marcar superseded, preservando histórico. Não reescrever motivação passada. Referências: `design.md`, `docs/architecture/transactions.md`, `docs/architecture/research.md`.
