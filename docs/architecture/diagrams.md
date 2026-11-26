# Diagramas | visão C4 e fluxos Mermaid

C4 nível 1 (contexto), nível 2 (containers) e nível 3 (componentes) são suficientes; nível 4 de classes será derivado do código se necessário, sem inventar classes existentes. Mermaid textual, sem depender de plugin externo.

## C4 L1: contexto (representação em flowchart)

```mermaid
flowchart LR
 V[Visitante] --> C[Catraca]
 P[Participante] --> C
 O[Organizador] --> C
 S[Sistema parceiro] -->|HTTPS local ou HTTP loopback + chave| C
 C --> G[Gateway simulado interno]
```

## C4 L2: containers

```mermaid
flowchart TB
 U[Navegador] -->|HTML e sessão| W[Web Django + Gunicorn]
 A[Parceiro] -->|JSON + chave| W
 W -->|SQL transacional| D[(PostgreSQL)]
 K[Worker Python] -->|jobs vencidos e finalize| D
 I[Migrate e seed one-shot] --> D
```

## C4 L3: módulos

```mermaid
flowchart TD
 S[storefront] --> I[identity]
 S --> C[catalog]
 S --> L[ledger]
 P[partner] --> C
 P --> L
 O[operations] --> I
 O --> C
 O --> L
 L --> C
 C --> I
 C --> D[(Schema platform)]
 I --> D
 L --> D
 O --> D
```

## Compra e gateway

```mermaid
sequenceDiagram
 participant U as Canal web/API
 participant S as Reserve
 participant D as PostgreSQL
 participant W as Worker
 U->>S: Entrada válida
 S->>D: BEGIN e lock evento
 S->>D: COUNT e valida capacidade
 alt sem vaga
  S-->>U: sold_out
 else vaga
  S->>D: INSERT ticket e job; COMMIT
  S-->>U: pending
  W->>D: Buscar job vencido sem lock
  W->>D: BEGIN; lock evento; reler ticket/job
  alt evento publicado e pending
   W->>D: Confirmar ou recusar; job done
  else terminal
   W->>D: job ignored
  end
  W->>D: COMMIT
 end
```

## Estado de evento e ingresso

```mermaid
stateDiagram-v2
 [*] --> draft
 draft --> published
 published --> cancelled
 cancelled --> [*]
```

```mermaid
stateDiagram-v2
 [*] --> pending
 pending --> confirmed: gateway aprova
 pending --> declined: gateway recusa
 pending --> cancelled: evento cancela
 confirmed --> refunded: evento cancela
 declined --> [*]
 cancelled --> [*]
 refunded --> [*]
```

## Modelo de dados

```mermaid
erDiagram
 ACCOUNT ||--o{ EVENT : owns
 ACCOUNT o|--o{ TICKET : participates
 EVENT ||--o{ TICKET : contains
 TICKET ||--|| PAYMENT_JOB : schedules
 ACCOUNT {
  uuid id PK
  string email UK
  string role
 }
 EVENT {
  uuid id PK
  uuid owner_id FK
  int capacity
  bigint price_cents
  string state
 }
 TICKET {
  uuid id PK
  uuid event_id FK
  uuid participant_id FK
  string code UK
  string status
  bigint price_cents
  datetime checked_in_at
 }
 PAYMENT_JOB {
  uuid ticket_id PK,FK
  datetime due_at
  string outcome
  string state
 }
```

## Avaliação e waves

```mermaid
flowchart TD
 D[Baseline aprovada] --> F[Implementador em branch]
 F --> G[Gates e commit SHA]
 G --> E[Avaliador independente]
 E --> V{Contrato passa?}
 V -->|Não| C[Relatório imutável e correção]
 C --> F
 V -->|Sim| P[PR e integração]
 P --> R[Regressão cross-feature]
 R -->|Falha| C
 R -->|Passa| N[Estado atualizado e próxima wave]
```

O DAG de implementação fica no PRD. Rever diagramas quando contrato ou arquitetura mudar; rodar renderizador Mermaid no gate documental após instalar ferramenta com versão fixa. Esses diagramas foram redigidos, mas ainda não renderizados automaticamente neste pacote.
