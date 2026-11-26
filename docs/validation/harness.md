# Harness e gates | especificação operacional

## Contrato dos comandos (F01 implementa)

`./bin/up`: bash POSIX-compatible ou shell declarado; valida Docker Compose v2 e porta; build images com dependências fixas; sobe DB, migra e executa seed em serviço one-shot, sobe web e worker, espera readiness com timeout e falha não zero se não saudável. Exibir URL e comandos; sem `.env` obrigatório, modo simulado default. Não depender de Make, jq, curl, Python ou browser instalados no host. Usar container para chamadas auxiliares. Compose project name/porta substituíveis para worktrees. `./bin/down`: `docker compose down --remove-orphans` no projeto atual, preserve volumes; verificar ausência de containers e listeners do produto. `./bin/gates [Fxx]`: executar em ambiente separado, verificar lint, docs, migrations (fresh e no pending migration), unitários, integração PostgreSQL, contratos HTTP, browser e timing padrão conforme features existentes; trap cleanup inclusive falha; sem skip de requisitos implementados. Gate final sem filtro roda tudo. Não executar teste destrutivo no DB da demo.

## Camadas e critérios

| Gate | Quando | Aceite |
|---|---|---|
| G0 docs | W0 e todo PR | `python3 scripts/validate_docs.py`; PRD/matriz/contratos/DAG íntegros, revisão semântica humana, Mermaid renderiza |
| G1 build/estático | Toda etapa | imagem constrói, Ruff lint/format, Django check, migrations sem drift; versões pinadas |
| G2 unitários | Toda etapa | classificações, validação, moeda, estados e mensagens; negativos e limites; sem skips |
| G3 integração | Toda feature | DB real, FKs, ownership, concorrência e rollback, serviços compartilhados |
| G4 contrato HTTP/UI | W5 e final | API fixa, browser real, sessão e CSRF, carga 30/5 duas rodadas, delays padrão |
| G5 avaliação | Toda feature | sessão nova, contrato por item, evidência, SHA, imutabilidade |
| G6 regressão/release | Após cada merge e W6 | fluxo 1–18, X14–X16, PRs, README/state, clone limpo e down/up |

Teste rápido pode injetar relógio/atrasos, separado de modo padrão. G4 deve testar tempos reais: medir monotonic e timestamps de criação; deadline fast 5s, slow 40s, polling <=200ms e sem estender o prazo para mascarar falha. Verificar ausência de transição antes de 2/30 segundos também com timestamps DB no teste de integração. No fluxo público aguardar 45s para provar estado tardio. Evitar paralelizar suites que competem por recurso e falseiam latência. Rodar G4 carga com Gunicorn concorrente e DB separado, não com servidor single-thread.

## Probe executável incluído

Depois de implementar F06, crie dois eventos publicados, vazios, capacidade 5, pelo produto (IDs distintos). Rodar com Python 3.12 em ambiente que alcança o web:

```sh
python3 scripts/partner_probe.py --base http://127.0.0.1:8080 --key catraca-local-partner-demo-v1 --events ID_E4 ID_E5
```

No container da aplicação, use URL interna do serviço conforme Compose final. O script testa autenticação/precedência, shape, duas rajadas HTTP de 30, 5/25, consulta e confirmação, esgotamento. É destrutivo para os dois eventos de teste: não usar eventos reais ou já vendidos. Ele não cria eventos, não testa UI, não mede precisão do limite inferior de timing do gateway, não substitui suite completa. Não imprimir chave/cartão. Runner deve integrar esse teste a G4 com fixtures criadas por UI ou setup de teste explícito.

## Evidências e diagnóstico

Salvar stdout/stderr, exit code, SHA, nome de projeto Compose, versão Docker/OS, horários UTC e IDs de fixture; evitar PII/segredo. Para falha: verificar health e logs do DB/worker/web, `docker compose ps`, migrations, seed; medir jobs overdue, lock waits e transações longas. Não aumentar timeout para disfarçar violação. Se porta ocupada, escolher WEB_PORT exclusivo e documentar; não matar processo alheio. Para clean clone, clone repo novo e execute somente up, não copie `.env` ou volumes. Teste down observa porta e `docker ps` filtrado por label de projeto, não exige que outros containers da máquina parem.
