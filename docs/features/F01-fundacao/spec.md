# F01 | FDD: Ambiente reproduzível e persistência

Status: proposto · Wave W1 · Fonte normativa: PRD e design.

## Resultado e interfaces

Provides: Ambiente Compose, schema compartilhado, clock, runner, dados de demonstração e interfaces de registro de rotas.

Consumes: Nenhuma feature anterior.

Ownership: platform, migrations, boot, bin, CI. Não alterar módulos de outras features sem amendment.

## Low-level design

A fundação fixa o schema compartilhado e fornece um ambiente real, mesmo antes de existirem jornadas. Use um app Django `coredata` para os quatro modelos de negócio e `accounts.User` como AUTH_USER_MODEL antes da primeira migration. Django migrations são o dono do DDL; nenhuma segunda ferramenta de migration. O banco utiliza volume por projeto. F01 fornece `accounts/email_policy.py` com a normalização canônica da seed, reutilizada sem duplicação em F02 e na validação de comprador do ledger. Bootstrap usa role de migração; web/worker usam role runtime sem DDL. Configuração vem de defaults locais + variáveis de ambiente, não de cópia manual de arquivo. O serviço bootstrap aplica migrate e seed uma vez por subida. Web e worker só começam após bootstrap exit 0; health do worker confirma loop e conexão, não apenas PID. No início o worker é scaffolding que só sinaliza prontidão e não consome jobs. F04 o substitui. Gates usam banco de teste separado e projeto distinto da demo.

**Contrato de configuração:** CAT_PROJECT, CAT_PORT, CAT_PARTNER_KEY, CAT_SECRET, CAT_PROFILE, CAT_GATEWAY_SCALE. `CAT_PROFILE=demo` exige escala 1. O bootstrap se recusa a rodar seed fora de demo/teste; idempotência por chave natural de conta, sem alterar usuários que não pertencem à seed. Dependências pinadas em lockfile e imagem por versão/digest selecionados em W0.

**Falhas:** rede de registry, porta ocupada, schema inválido, bootstrap abortado, worker indisponível, gate com falha. Em todos, diagnóstico com serviço e saída; sem falso health verde. Seed usa senha hash do Django. Não publicar porta DB. O comando down não remove dados por padrão.

**Handoff:** schema e app label imutáveis sem alteração formal; portas `normalize_email`, `clock_now`, `fixture_factory` e `worker_command` conforme o registro interno; F04 recebe o entrypoint do worker e consome a normalização para `PartnerBuyer`; documentação de bootstrap e teste de volume/portas.

## Critérios e limites
| ID | Fase | Aceite |
| --- | --- | --- |
| A01 | local | Clone limpo: ./bin/up constrói, migra, semeia e espera web/worker/DB prontos; /health/ready retorna 200 sem configuração manual. |
| A02 | local | ./bin/down encerra todos os containers e portas iniciados; nova subida conserva dados e seed não duplica contas. |
| A03 | local | ./bin/gates falha com teste quebrado, executa testes reais e lint, usa DB isolado e passa com testes válidos. |
| A04 | local | README e AGENTS.md descrevem os comandos, endpoints, contas e mapa; o padrão local usa somente simulador e não requer configuração de pagamento. |
| A05 | local | Schema possui FKs, código único no formato [A-Z0-9]{12}, restrições de status, lotação e preço; migrações reexecutáveis. |
| A29 | local | Gates rodam em projeto Compose distinto do ambiente de demonstração, sem remover volumes alheios; falha de bootstrap ou cleanup retorna não zero. |
| A37 | local | Gate documental diferencia baseline, candidato local e release; relatório incompleto, falso PASS, arquivo alterado ou estado inconsistente causam falha na fase apropriada. |

## Evolução e rollback
Mudança de contrato exige ADR/amendment aprovado e reavaliação de consumidores. Em falha de implementação, corrigir em commit novo; não alterar migrations aplicadas nem relatórios. No MVP local usar ambiente de testes descartável para rollback de schema; não apagar volume de demonstração.
