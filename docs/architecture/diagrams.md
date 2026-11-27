# Diagramas de design

## C1: contexto
```mermaid
flowchart LR
    V[Visitante] --> C[Catraca]
    P[Participante] --> C
    O[Organizador] --> C
    S[Sistema parceiro] -->|HTTP local: JSON, chave| C
    C --> G[Gateway simulado interno]
```
Nota: transporte padrão HTTP em loopback; TLS fora de escopo. C2/C3 em design.md: web, bootstrap, worker, DB e módulos.

## C2: containers
```mermaid
flowchart TB
    H[Host browser / CLI] --> W[web: Django/Gunicorn]
    B[bootstrap: migrate + seed] --> D[(PostgreSQL)]
    B -->|exit 0| W
    B -->|exit 0| Q[worker]
    W --> D
    Q --> D
    T[test runner isolado] --> W
```

## ER lógico
```mermaid
erDiagram
    USER ||--o{ EVENT : owns
    USER o|--o{ TICKET : purchases_web
    EVENT ||--o{ TICKET : has
    TICKET ||--o| PAYMENT_JOB : schedules
```
Parceiro não é User. A cardinalidade física é zero-ou-um job por ticket; o serviço
canônico `reserve` cria ticket e exatamente um job no mesmo commit. Status,
constraints e índices estão no design. Modelagem física na migration F01.

## Reserva concorrente
```mermaid
sequenceDiagram
    participant A as Request A
    participant B as Request B
    participant DB as PostgreSQL
    A->>DB: BEGIN and event lock
    B->>DB: BEGIN and wait on event lock
    A->>DB: count 4 of 5, insert ticket and job
    A->>DB: COMMIT
    DB-->>B: lock granted
    B->>DB: fresh count 5 of 5
    B->>DB: ROLLBACK
    DB-->>B: sold_out
```

## Resolução e cancelamento
```mermaid
sequenceDiagram
    participant O as Organizer
    participant D as DB
    participant W as Worker
    O->>D: event lock
    O->>D: cancel event and transition all tickets
    O->>D: commit
    W->>D: discover due job, event lock
    W->>D: reread terminal ticket
    W->>D: mark ignored and commit
```
Se worker vence primeiro, cancelamento observa novo status e estorna se confirmado.

## Ciclo de entrega
```mermaid
flowchart LR
    D[Design aprovado] --> I[Implementar em branch]
    I --> L[Local gates]
    L --> E[Avaliador independente]
    E -->|FAIL| I
    E -->|Local PASS| M[Merge via PR]
    M --> G[Integração da wave]
    G -->|FAIL| I
    G --> R[Fluxo final e evidência]
    R --> F[Release]
```
Diagramas planejados, validar sintaxe Mermaid na W0. C4 Code-level será atualizado após implementação quando útil.
