# Requirements Matrix

Status inicial: todos planejados. R01–R13 são do brief; API contrato externo; H01–H04 agrupam harness; SDD/EVAL/STATE/PAR/DELIVERY são processo. Axx local, Xxx cruzado, Pxx entrega. A matriz é gerada do manifesto `docs/validation/traceability.json` e não prova execução. Atualizar status somente com relatório independente e revisão do coordenador.

| Requisito | Critério PRD | Feature/Wave | Item contrato | Teste | Tarefa | Aceite verificável | Estado |
|---|---|---|---|---|---|---|---|
| API | A21 | F06 | C-F06-A21 | TEST-A21 | T-F06-02 | GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos. | planejado |
| API | A22 | F06 | C-F06-A22 | TEST-A22 | T-F06-02 | POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out. | planejado |
| API | A23 | F06 | C-F06-A23 | TEST-A23 | T-F06-02 | GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized. | planejado |
| API | A24 | F06 | C-F06-A24 | TEST-A24 | T-F06-03 | Em duas rodadas HTTP reais, cada evento novo de capacidade 5 recebe 30 POST simultâneos com cartão 0001: 5×202 e 25×409, sem 5xx; depois 5 confirmados. | planejado |
| API | X09 | F06 | C-F06-X09 | TEST-X09 | T-F06-04 | API usa catálogo e centavos/ocupação canônicos; edição preço/capacidade reflete na listagem. | planejado |
| API | X10 | F06 | C-F06-X10 | TEST-X10 | T-F06-04 | API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture. | planejado |
| API | X15 | F07 | C-F07-X15 | TEST-X15 | T-W6-02 | Integração final: compra partner soma painel, é validada no check-in e deixa API após cancelamento. | planejado |
| API | X16 | F06 | C-F06-X16 | TEST-X16 | T-W6-02 | Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web. | planejado |
| DELIVERY | P06 | W6 | C-RELEASE-P06 | TEST-P06 | T-W6-03 | Repo público único, main com README completo; fluxo externo 1–18 aprovado em clone limpo. | planejado |
| EVAL | P03 | W6 | C-RELEASE-P03 | TEST-P03 | T-W6-03 | Cada feature aprovada em avaliação independente; relatório imutável com data, SHA, ferramenta, modelo, evidência por item. | planejado |
| H01 | A01 | F01 | C-F01-A01 | TEST-A01 | T-F01-03 | Clone limpo: ./bin/up constrói, migra, semeia e espera web/worker/DB prontos; /health/ready retorna 200 sem configuração manual. | planejado |
| H01 | X01 | F02 | C-F02-X01 | TEST-X01 | T-F02-04 | Após up com seed, A/B/P autenticam; duas execuções da seed não duplicam contas. | planejado |
| H01 | X02 | F03 | C-F03-X02 | TEST-X02 | T-F03-04 | Migração e clock da fundação permitem criação e rejeição de data vencida. | planejado |
| H01 | X04 | F04 | C-F04-X04 | TEST-X04 | T-F04-04 | Worker do Compose consome job persistido após reinício sem chave real. | planejado |
| H02 | A02 | F01 | C-F01-A02 | TEST-A02 | T-F01-03 | ./bin/down encerra todos os containers e portas iniciados; nova subida conserva dados e seed não duplica contas. | planejado |
| H02 | X01 | F02 | C-F02-X01 | TEST-X01 | T-F02-04 | Após up com seed, A/B/P autenticam; duas execuções da seed não duplicam contas. | planejado |
| H03 | A03 | F01 | C-F01-A03 | TEST-A03 | T-F01-01 | ./bin/gates falha com teste quebrado, executa testes reais e lint, usa DB isolado e passa com testes válidos. | planejado |
| H04 | A04 | F01 | C-F01-A04 | TEST-A04 | T-F01-03 | AGENTS.md e README contêm comandos, endereços, credenciais de seed, mapa; modo padrão não exige gateway real. | planejado |
| PAR | P05 | W6 | C-RELEASE-P05 | TEST-P05 | T-W6-03 | Pelo menos uma wave paralela via PRs mergeados; primeiro commit de cada PR anterior ao último de todos os demais. | planejado |
| R01 | A09 | F03 | C-F03-A09 | TEST-A09 | T-F03-01 | Nome/local não vazios; lotação inteira >=1; preço em centavos >0; início estritamente futuro em criar e editar, inclusive requisição direta. | planejado |
| R01 | X02 | F03 | C-F03-X02 | TEST-X02 | T-F03-04 | Migração e clock da fundação permitem criação e rejeição de data vencida. | planejado |
| R02 | A10 | F03 | C-F03-A10 | TEST-A10 | T-F03-03 | Evento nasce draft; publicar torna visível a consulta pública; gestão tem URL estável e lista apenas próprios eventos. | planejado |
| R02 | A18 | F05 | C-F05-A18 | TEST-A18 | T-F05-01 | Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem. | planejado |
| R02 | A21 | F06 | C-F06-A21 | TEST-A21 | T-F06-02 | GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos. | planejado |
| R02 | X05 | F04 | C-F04-X05 | TEST-X05 | T-F04-04 | Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação. | planejado |
| R02 | X07 | F05 | C-F05-X07 | TEST-X07 | T-F05-04 | Publicar/lotar/cancelar reflete na vitrine sem cache obsoleto. | planejado |
| R02 | X09 | F06 | C-F06-X09 | TEST-X09 | T-F06-04 | API usa catálogo e centavos/ocupação canônicos; edição preço/capacidade reflete na listagem. | planejado |
| R03 | A11 | F03 | C-F03-A11 | TEST-A11 | T-F03-02 | Editar sob lock do evento; capacidade abaixo de pending+confirmed é rejeitada; igual/acima aceita; preço novo não altera snapshot de ingressos. | planejado |
| R03 | A16 | F04 | C-F04-A16 | TEST-A16 | T-F04-03 | Snapshot de preço é capturado sob lock; finalize só altera pending de evento publicado; resultado duplicado/tardio não revive terminal; job sobrevive reinício. | planejado |
| R03 | X05 | F04 | C-F04-X05 | TEST-X05 | T-F04-04 | Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação. | planejado |
| R03 | X09 | F06 | C-F06-X09 | TEST-X09 | T-F06-04 | API usa catálogo e centavos/ocupação canônicos; edição preço/capacidade reflete na listagem. | planejado |
| R04 | A10 | F03 | C-F03-A10 | TEST-A10 | T-F03-03 | Evento nasce draft; publicar torna visível a consulta pública; gestão tem URL estável e lista apenas próprios eventos. | planejado |
| R04 | A28 | F07 | C-F07-A28 | TEST-A28 | T-F07-03 | Check-in, cancelar e painel ficam na URL de gestão de cada evento; todas as ações exigem dono inclusive requisição direta. | planejado |
| R04 | X03 | F03 | C-F03-X03 | TEST-X03 | T-F03-04 | URL de gestão e listagem usam dono da sessão; B não pode editar/publicar A. | planejado |
| R04 | X12 | F07 | C-F07-X12 | TEST-X12 | T-F07-04 | Cancelamento bloqueia publicação/edição e integra gestão em URL existente. | planejado |
| R05 | A05 | F01 | C-F01-A05 | TEST-A05 | T-F01-02 | Schema possui FKs, unicidade de código, restrições de status, lotação e preço; migrações reexecutáveis. | planejado |
| R05 | A11 | F03 | C-F03-A11 | TEST-A11 | T-F03-02 | Editar sob lock do evento; capacidade abaixo de pending+confirmed é rejeitada; igual/acima aceita; preço novo não altera snapshot de ingressos. | planejado |
| R05 | A13 | F04 | C-F04-A13 | TEST-A13 | T-F04-02 | Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga. | planejado |
| R05 | A18 | F05 | C-F05-A18 | TEST-A18 | T-F05-01 | Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem. | planejado |
| R05 | A21 | F06 | C-F06-A21 | TEST-A21 | T-F06-02 | GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos. | planejado |
| R05 | A27 | F07 | C-F07-A27 | TEST-A27 | T-F07-03 | Painel mostra seis métricas com snapshots de preço e ambos os canais; check-ins somente confirmed; cancelado tem receita/vagas/confirmados/pendentes/check-ins zero. | planejado |
| R05 | X05 | F04 | C-F04-X05 | TEST-X05 | T-F04-04 | Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação. | planejado |
| R05 | X07 | F05 | C-F05-X07 | TEST-X07 | T-F05-04 | Publicar/lotar/cancelar reflete na vitrine sem cache obsoleto. | planejado |
| R05 | X09 | F06 | C-F06-X09 | TEST-X09 | T-F06-04 | API usa catálogo e centavos/ocupação canônicos; edição preço/capacidade reflete na listagem. | planejado |
| R05 | X15 | F07 | C-F07-X15 | TEST-X15 | T-W6-02 | Integração final: compra partner soma painel, é validada no check-in e deixa API após cancelamento. | planejado |
| R05 | X16 | F06 | C-F06-X16 | TEST-X16 | T-W6-02 | Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web. | planejado |
| R06 | A13 | F04 | C-F04-A13 | TEST-A13 | T-F04-02 | Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga. | planejado |
| R06 | A17 | F04 | C-F04-A17 | TEST-A17 | T-F04-01 | Cartão diferente de 16 dígitos ASCII falha antes de criar ingresso; e-mail malformado na compra de parceiro falha; PAN não persiste nem aparece em logs. | planejado |
| R06 | A19 | F05 | C-F05-A19 | TEST-A19 | T-F05-02 | Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001. | planejado |
| R06 | A22 | F06 | C-F06-A22 | TEST-A22 | T-F06-02 | POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out. | planejado |
| R06 | X08 | F05 | C-F05-X08 | TEST-X08 | T-F05-04 | Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine. | planejado |
| R06 | X10 | F06 | C-F06-X10 | TEST-X10 | T-F06-04 | API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture. | planejado |
| R06 | X14 | F07 | C-F07-X14 | TEST-X14 | T-W6-02 | Integração final (não dependência de implementação): compra web aparece no painel e permite check-in; cancelamento aparece em Meus ingressos. | planejado |
| R07 | A14 | F04 | C-F04-A14 | TEST-A14 | T-F04-02 | Quando lotação esgota, não cria ingresso/job; 30 reservas concorrentes sobre capacidade 5 dão exatamente 5 sucessos/25 sold_out, em duas rodadas novas. | planejado |
| R07 | A18 | F05 | C-F05-A18 | TEST-A18 | T-F05-01 | Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem. | planejado |
| R07 | A22 | F06 | C-F06-A22 | TEST-A22 | T-F06-02 | POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out. | planejado |
| R07 | A24 | F06 | C-F06-A24 | TEST-A24 | T-F06-03 | Em duas rodadas HTTP reais, cada evento novo de capacidade 5 recebe 30 POST simultâneos com cartão 0001: 5×202 e 25×409, sem 5xx; depois 5 confirmados. | planejado |
| R07 | X05 | F04 | C-F04-X05 | TEST-X05 | T-F04-04 | Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação. | planejado |
| R07 | X10 | F06 | C-F06-X10 | TEST-X10 | T-F06-04 | API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture. | planejado |
| R07 | X15 | F07 | C-F07-X15 | TEST-X15 | T-W6-02 | Integração final: compra partner soma painel, é validada no check-in e deixa API após cancelamento. | planejado |
| R07 | X16 | F06 | C-F06-X16 | TEST-X16 | T-W6-02 | Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web. | planejado |
| R08 | A15 | F04 | C-F04-A15 | TEST-A15 | T-F04-03 | Gateway padrão confirma 0001 e recusa 0002/outros em 2–5s; confirma 0003 e recusa 0004 em 30–40s; recusa libera uma vaga. | planejado |
| R08 | A19 | F05 | C-F05-A19 | TEST-A19 | T-F05-02 | Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001. | planejado |
| R08 | X04 | F04 | C-F04-X04 | TEST-X04 | T-F04-04 | Worker do Compose consome job persistido após reinício sem chave real. | planejado |
| R08 | X08 | F05 | C-F05-X08 | TEST-X08 | T-F05-04 | Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine. | planejado |
| R09 | A05 | F01 | C-F01-A05 | TEST-A05 | T-F01-02 | Schema possui FKs, unicidade de código, restrições de status, lotação e preço; migrações reexecutáveis. | planejado |
| R09 | A08 | F02 | C-F02-A08 | TEST-A08 | T-F02-02 | Participante só tem acesso aos próprios recursos; parceiro não cria sessão web nem vincula conta pelo e-mail. | planejado |
| R09 | A13 | F04 | C-F04-A13 | TEST-A13 | T-F04-02 | Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga. | planejado |
| R09 | A19 | F05 | C-F05-A19 | TEST-A19 | T-F05-02 | Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001. | planejado |
| R09 | A20 | F05 | C-F05-A20 | TEST-A20 | T-F05-02 | Meus ingressos filtra por participant_id autenticado, não por e-mail, e mostra todos os cinco rótulos; visitante não compra. | planejado |
| R09 | A23 | F06 | C-F06-A23 | TEST-A23 | T-F06-02 | GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized. | planejado |
| R09 | X06 | F05 | C-F05-X06 | TEST-X06 | T-F05-04 | Sessão define dono do ingresso; anônimo e outra conta não veem compra pessoal. | planejado |
| R09 | X08 | F05 | C-F05-X08 | TEST-X08 | T-F05-04 | Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine. | planejado |
| R09 | X10 | F06 | C-F06-X10 | TEST-X10 | T-F06-04 | API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture. | planejado |
| R09 | X14 | F07 | C-F07-X14 | TEST-X14 | T-W6-02 | Integração final (não dependência de implementação): compra web aparece no painel e permite check-in; cancelamento aparece em Meus ingressos. | planejado |
| R09 | X16 | F06 | C-F06-X16 | TEST-X16 | T-W6-02 | Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web. | planejado |
| R10 | A25 | F07 | C-F07-A25 | TEST-A25 | T-F07-01 | Check-in aplica exatamente as cinco mensagens na ordem definida; só confirmed não utilizado recebe checkedIn=true; dois check-ins concorrentes liberam uma entrada. | planejado |
| R10 | X13 | F07 | C-F07-X13 | TEST-X13 | T-F07-04 | Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive. | planejado |
| R10 | X14 | F07 | C-F07-X14 | TEST-X14 | T-W6-02 | Integração final (não dependência de implementação): compra web aparece no painel e permite check-in; cancelamento aparece em Meus ingressos. | planejado |
| R10 | X15 | F07 | C-F07-X15 | TEST-X15 | T-W6-02 | Integração final: compra partner soma painel, é validada no check-in e deixa API após cancelamento. | planejado |
| R11 | A12 | F03 | C-F03-A12 | TEST-A12 | T-F03-02 | Evento cancelled não pode ser alterado/republicado; catálogo e disponibilidade pública o excluem. | planejado |
| R11 | A16 | F04 | C-F04-A16 | TEST-A16 | T-F04-03 | Snapshot de preço é capturado sob lock; finalize só altera pending de evento publicado; resultado duplicado/tardio não revive terminal; job sobrevive reinício. | planejado |
| R11 | A26 | F07 | C-F07-A26 | TEST-A26 | T-F07-02 | Cancelar publicado é irreversível; na mesma transação confirmed→refunded e pending→cancelled, sem alteração de declined; gateway posterior não modifica; edit/publish/compra rejeitados. | planejado |
| R11 | X12 | F07 | C-F07-X12 | TEST-X12 | T-F07-04 | Cancelamento bloqueia publicação/edição e integra gestão em URL existente. | planejado |
| R11 | X13 | F07 | C-F07-X13 | TEST-X13 | T-F07-04 | Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive. | planejado |
| R11 | X14 | F07 | C-F07-X14 | TEST-X14 | T-W6-02 | Integração final (não dependência de implementação): compra web aparece no painel e permite check-in; cancelamento aparece em Meus ingressos. | planejado |
| R11 | X15 | F07 | C-F07-X15 | TEST-X15 | T-W6-02 | Integração final: compra partner soma painel, é validada no check-in e deixa API após cancelamento. | planejado |
| R12 | A27 | F07 | C-F07-A27 | TEST-A27 | T-F07-03 | Painel mostra seis métricas com snapshots de preço e ambos os canais; check-ins somente confirmed; cancelado tem receita/vagas/confirmados/pendentes/check-ins zero. | planejado |
| R12 | X13 | F07 | C-F07-X13 | TEST-X13 | T-F07-04 | Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive. | planejado |
| R12 | X14 | F07 | C-F07-X14 | TEST-X14 | T-W6-02 | Integração final (não dependência de implementação): compra web aparece no painel e permite check-in; cancelamento aparece em Meus ingressos. | planejado |
| R12 | X15 | F07 | C-F07-X15 | TEST-X15 | T-W6-02 | Integração final: compra partner soma painel, é validada no check-in e deixa API após cancelamento. | planejado |
| R13 | A06 | F02 | C-F02-A06 | TEST-A06 | T-F02-01 | Cadastro público cria somente participante, e-mail normalizado único; senha armazenada como hash; login válido e logout invalidam sessão; erro genérico em credenciais inválidas. | planejado |
| R13 | A07 | F02 | C-F02-A07 | TEST-A07 | T-F02-02 | Visitante e participante não acessam rotas de gestão; B não lê nem modifica eventos de A, incluindo URL direta e POST forjado. | planejado |
| R13 | A08 | F02 | C-F02-A08 | TEST-A08 | T-F02-02 | Participante só tem acesso aos próprios recursos; parceiro não cria sessão web nem vincula conta pelo e-mail. | planejado |
| R13 | A20 | F05 | C-F05-A20 | TEST-A20 | T-F05-02 | Meus ingressos filtra por participant_id autenticado, não por e-mail, e mostra todos os cinco rótulos; visitante não compra. | planejado |
| R13 | A23 | F06 | C-F06-A23 | TEST-A23 | T-F06-02 | GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized. | planejado |
| R13 | A28 | F07 | C-F07-A28 | TEST-A28 | T-F07-03 | Check-in, cancelar e painel ficam na URL de gestão de cada evento; todas as ações exigem dono inclusive requisição direta. | planejado |
| R13 | X03 | F03 | C-F03-X03 | TEST-X03 | T-F03-04 | URL de gestão e listagem usam dono da sessão; B não pode editar/publicar A. | planejado |
| R13 | X06 | F05 | C-F05-X06 | TEST-X06 | T-F05-04 | Sessão define dono do ingresso; anônimo e outra conta não veem compra pessoal. | planejado |
| R13 | X11 | F07 | C-F07-X11 | TEST-X11 | T-F07-04 | Todas as ações operacionais respeitam guarda de dono. | planejado |
| SDD | P01 | W6 | C-RELEASE-P01 | TEST-P01 | T-W6-03 | PRD >=5 features, fornece/consome, DAG e waves; todas R01–R13 citadas, cada aresta coberta. | planejado |
| SDD | P02 | W6 | C-RELEASE-P02 | TEST-P02 | T-W6-03 | Spec, plano e contrato por feature, todos os critérios e cross-feature mapeados. | planejado |
| STATE | P04 | W6 | C-RELEASE-P04 | TEST-P04 | T-W6-03 | Estado final bate com relatórios existentes e mais recentes; sem status concluído sem aprovação. | planejado |
