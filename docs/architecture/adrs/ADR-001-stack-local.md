# ADR-001 | Monólito modular Django/PostgreSQL

Status: proposto | 26/11/2026 | Autor: planejamento inicial; aprovação no kickoff.

## Contexto
A stack é livre, prazo de MVP curto e host não garante Python.

## Decisão
Django 5.2 + PostgreSQL 17 em Compose; templates HTML e Gunicorn concorrente.

## Alternativas e trade-offs
SPA + API duplicaria interfaces de autenticação; SQLite não reproduz os locks escolhidos; microsserviços criariam falhas distribuídas.

## Consequências
Menos componentes, runtime dentro de Docker; exige migrations e controle de workers.

## Validação
A01,A03,A14,A24. Ver `requirements-matrix.md` na raiz; resultados pendentes.

## Ciclo de vida
Após aprovação humana, marcar accepted com data. Se substituída, criar novo ADR que referencie este e marcar superseded, preservando histórico. Não reescrever motivação passada. Referências: `design.md`, `docs/architecture/transactions.md`, `docs/architecture/research.md`.
