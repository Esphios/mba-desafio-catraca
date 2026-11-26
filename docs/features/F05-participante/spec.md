# F05 | FDD: Vitrine e meus ingressos

Status: planejado. Wave W5. Fonte: PRD e HLD; ADRs propostos. Este FDD não atesta código existente.

## Objetivo, provides e consumes
Vitrine pública, compra autenticada e página de ingressos pessoais.

F02: participante/sessão; F03: catálogo; F04: reserve e consulta.

## Limites de escrita
storefront/, templates/storefront/, tests/storefront; no shared model edits.

## Design detalhado
`storefront/` owns public catalog and participant UI. GET / uses catalog DTO; detail returns 404 if unavailable. Display esgotado when zero seats and map SoldOut from reserve into exact text, including stale-tab race. GET my-tickets uses participant identity and ledger query, shows status label and code; no partner entries even same buyer email. POST purchase is CSRF-protected and actor ID from session. Redirect 303 to my-tickets on success; pending observation tested immediately, then reload. Never duplicate lock/occupancy or mutate tickets directly. Tests use actual F01–F04 from common base, not mock substitute for acceptance.

## Dependências e integração
F02, F03, F04. Consumir interfaces do HLD, não importar views de outras features. Em caso de interface insuficiente, registrar bloqueio e pedir amendment; não criar cópia de regra. Contratos externos e códigos do brief têm precedência. Dependências cross-feature: X06, X07, X08; ver contrato.

## Critérios locais e casos de falha
- A18 (R02,R05,R07): Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem.
- A19 (R06,R08,R09): Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001.
- A20 (R09,R13): Meus ingressos filtra por participant_id autenticado, não por e-mail, e mostra todos os cinco rótulos; visitante não compra.

## Testabilidade e segurança
Usar fixtures mínimas isoladas; relógio injetável para lógica, modo padrão para prazo real. Validar entradas e falhas além de happy path. Nenhum dado real, nenhuma modificação de contrato para mascarar falha. Evidência independente no contrato.

## Rollback e evolução
Em falha, manter branch sem merge e corrigir com novo commit. Mudanças de schema após F01 exigem migração revisada, teste fresh/upgrade e coordenação. Não desfazer migração de dados em ambiente de usuário sem backup; neste MVP usar ambiente descartável de teste. Regressão final obrigatória após última integração.
