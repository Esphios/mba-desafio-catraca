# Matriz de requisitos e verificação

Baseline proposta; a matriz indica cobertura planejada, não aprovação. Cada linha liga uma exigência a critério, item de contrato, teste e tarefa. `local` exige provider já entregue; `integrated` exige ambas as features integradas; `release` exige a main e evidências de processo. A regra `API` é o contrato fixo; H01–H04, SDD, EVAL, STATE, PAR e DELIVERY são requisitos de engenharia do brief.

| Requisito | Critério PRD | Responsável | Fase | Item contrato | Teste | Tarefa | Aceite |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H01 | A01 | F01 | local | C-F01-A01 | TEST-A01 | T-F01-03 | Clone limpo: ./bin/up constrói, migra, semeia e espera web/worker/DB prontos; /health/ready retorna 200 sem configuração manual. |
| H02 | A02 | F01 | local | C-F01-A02 | TEST-A02 | T-F01-03 | ./bin/down encerra todos os containers e portas iniciados; nova subida conserva dados e seed não duplica contas. |
| H03 | A03 | F01 | local | C-F01-A03 | TEST-A03 | T-F01-01 | ./bin/gates falha com teste quebrado, executa testes reais e lint, usa DB isolado e passa com testes válidos. |
| H04 | A04 | F01 | local | C-F01-A04 | TEST-A04 | T-F01-03 | README e AGENTS.md descrevem os comandos, endpoints, contas e mapa; o padrão local usa somente simulador e não requer configuração de pagamento. |
| R05 | A05 | F01 | local | C-F01-A05 | TEST-A05 | T-F01-02 | Schema possui FKs, unicidade de código, restrições de status, lotação e preço; migrações reexecutáveis. |
| R09 | A05 | F01 | local | C-F01-A05 | TEST-A05 | T-F01-02 | Schema possui FKs, unicidade de código, restrições de status, lotação e preço; migrações reexecutáveis. |
| R13 | A06 | F02 | local | C-F02-A06 | TEST-A06 | T-F02-01 | Cadastro público cria somente participante, e-mail normalizado único; senha armazenada como hash; login válido e logout invalidam sessão; erro genérico em credenciais inválidas. |
| R13 | A07 | F02 | local | C-F02-A07 | TEST-A07 | T-F02-02 | Guarda de papel e predicado de dono são aplicados em todos os recursos de gestão; no contrato local, validar com fixtures e endpoints de teste; as rotas reais são validadas em X03 e X11. |
| R09 | A08 | F02 | local | C-F02-A08 | TEST-A08 | T-F02-02 | O serviço de identidade identifica participante por ID de sessão, não por e-mail ou parâmetro; parceiro não é uma identidade web. Titularidade real de ingressos é validada em X06/X16. |
| R13 | A08 | F02 | local | C-F02-A08 | TEST-A08 | T-F02-02 | O serviço de identidade identifica participante por ID de sessão, não por e-mail ou parâmetro; parceiro não é uma identidade web. Titularidade real de ingressos é validada em X06/X16. |
| R01 | A09 | F03 | local | C-F03-A09 | TEST-A09 | T-F03-01 | Nome/local não vazios; lotação inteira >=1; preço em centavos >0; início estritamente futuro em criar e editar, inclusive requisição direta. |
| R02 | A10 | F03 | local | C-F03-A10 | TEST-A10 | T-F03-03 | Evento nasce draft; publicar torna visível a consulta pública; gestão tem URL estável e lista apenas próprios eventos. |
| R04 | A10 | F03 | local | C-F03-A10 | TEST-A10 | T-F03-03 | Evento nasce draft; publicar torna visível a consulta pública; gestão tem URL estável e lista apenas próprios eventos. |
| R03 | A11 | F03 | local | C-F03-A11 | TEST-A11 | T-F03-02 | Editar sob lock do evento; capacidade abaixo de pending+confirmed é rejeitada; igual/acima aceita; preço novo não altera snapshot de ingressos. |
| R05 | A11 | F03 | local | C-F03-A11 | TEST-A11 | T-F03-02 | Editar sob lock do evento; capacidade abaixo de pending+confirmed é rejeitada; igual/acima aceita; preço novo não altera snapshot de ingressos. |
| R11 | A12 | F03 | local | C-F03-A12 | TEST-A12 | T-F03-02 | Evento cancelled não pode ser alterado/republicado; catálogo e disponibilidade pública o excluem. |
| R05 | A13 | F04 | local | C-F04-A13 | TEST-A13 | T-F04-02 | Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga. |
| R06 | A13 | F04 | local | C-F04-A13 | TEST-A13 | T-F04-02 | Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga. |
| R09 | A13 | F04 | local | C-F04-A13 | TEST-A13 | T-F04-02 | Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga. |
| R07 | A14 | F04 | local | C-F04-A14 | TEST-A14 | T-F04-02 | Quando lotação esgota, não cria ingresso/job; 30 reservas concorrentes sobre capacidade 5 dão exatamente 5 sucessos/25 sold_out, em duas rodadas novas. |
| R08 | A15 | F04 | local | C-F04-A15 | TEST-A15 | T-F04-03 | Gateway padrão confirma 0001 e recusa 0002/outros em 2–5s; confirma 0003 e recusa 0004 em 30–40s; recusa libera uma vaga. |
| R03 | A16 | F04 | local | C-F04-A16 | TEST-A16 | T-F04-03 | Snapshot de preço é capturado sob lock; finalize só altera pending de evento publicado; resultado duplicado/tardio não revive terminal; job sobrevive reinício. |
| R11 | A16 | F04 | local | C-F04-A16 | TEST-A16 | T-F04-03 | Snapshot de preço é capturado sob lock; finalize só altera pending de evento publicado; resultado duplicado/tardio não revive terminal; job sobrevive reinício. |
| R06 | A17 | F04 | local | C-F04-A17 | TEST-A17 | T-F04-01 | Cartão diferente de 16 dígitos ASCII falha antes de criar ingresso; e-mail malformado na compra de parceiro falha; PAN não persiste nem aparece em logs. |
| R02 | A18 | F05 | local | C-F05-A18 | TEST-A18 | T-F05-01 | Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem. |
| R05 | A18 | F05 | local | C-F05-A18 | TEST-A18 | T-F05-01 | Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem. |
| R07 | A18 | F05 | local | C-F05-A18 | TEST-A18 | T-F05-01 | Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem. |
| R06 | A19 | F05 | local | C-F05-A19 | TEST-A19 | T-F05-02 | Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001. |
| R08 | A19 | F05 | local | C-F05-A19 | TEST-A19 | T-F05-02 | Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001. |
| R09 | A19 | F05 | local | C-F05-A19 | TEST-A19 | T-F05-02 | Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001. |
| R09 | A20 | F05 | local | C-F05-A20 | TEST-A20 | T-F05-02 | Meus ingressos filtra por participant_id autenticado, não por e-mail, e mostra todos os cinco rótulos; visitante não compra. |
| R13 | A20 | F05 | local | C-F05-A20 | TEST-A20 | T-F05-02 | Meus ingressos filtra por participant_id autenticado, não por e-mail, e mostra todos os cinco rótulos; visitante não compra. |
| API | A21 | F06 | local | C-F06-A21 | TEST-A21 | T-F06-02 | GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos. |
| R02 | A21 | F06 | local | C-F06-A21 | TEST-A21 | T-F06-02 | GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos. |
| R05 | A21 | F06 | local | C-F06-A21 | TEST-A21 | T-F06-02 | GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos. |
| API | A22 | F06 | local | C-F06-A22 | TEST-A22 | T-F06-02 | POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out. |
| R06 | A22 | F06 | local | C-F06-A22 | TEST-A22 | T-F06-02 | POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out. |
| R07 | A22 | F06 | local | C-F06-A22 | TEST-A22 | T-F06-02 | POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out. |
| API | A23 | F06 | local | C-F06-A23 | TEST-A23 | T-F06-02 | GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized. |
| R09 | A23 | F06 | local | C-F06-A23 | TEST-A23 | T-F06-02 | GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized. |
| R13 | A23 | F06 | local | C-F06-A23 | TEST-A23 | T-F06-02 | GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized. |
| R07 | A24 | F06 | local | C-F06-A24 | TEST-A24 | T-F06-03 | Em duas rodadas HTTP reais, cada evento novo de capacidade 5 recebe 30 POST simultâneos com cartão 0001: 5×202 e 25×409, sem 5xx; depois 5 confirmados. |
| API | A24 | F06 | local | C-F06-A24 | TEST-A24 | T-F06-03 | Em duas rodadas HTTP reais, cada evento novo de capacidade 5 recebe 30 POST simultâneos com cartão 0001: 5×202 e 25×409, sem 5xx; depois 5 confirmados. |
| R10 | A25 | F07 | local | C-F07-A25 | TEST-A25 | T-F07-01 | A decisão de check-in respeita a precedência R10 e somente um pedido concorrente pode marcar entrada; no evento cancelado, a página oculta o formulário, e POST direto mantém precedência. |
| R11 | A26 | F07 | local | C-F07-A26 | TEST-A26 | T-F07-02 | Cancelar evento publicado é uma operação terminal; em até 10 s (baseline: no mesmo commit), pending passa a cancelled e confirmed a refunded; declined permanece; nenhuma resposta tardia reabre ingresso. Rejeitar edição e republicação por POST. |
| R05 | A27 | F07 | local | C-F07-A27 | TEST-A27 | T-F07-03 | As seis métricas usam uma consulta coerente sobre evento e ingressos, sem contadores de canal; preço histórico apenas de confirmed. Cancelamento zera tudo exceto estornados. |
| R12 | A27 | F07 | local | C-F07-A27 | TEST-A27 | T-F07-03 | As seis métricas usam uma consulta coerente sobre evento e ingressos, sem contadores de canal; preço histórico apenas de confirmed. Cancelamento zera tudo exceto estornados. |
| R04 | A28 | F07 | local | C-F07-A28 | TEST-A28 | T-F07-03 | Check-in, cancelar e painel ficam na URL de gestão de cada evento; todas as ações exigem dono inclusive requisição direta. |
| R13 | A28 | F07 | local | C-F07-A28 | TEST-A28 | T-F07-03 | Check-in, cancelar e painel ficam na URL de gestão de cada evento; todas as ações exigem dono inclusive requisição direta. |
| H01 | A29 | F01 | local | C-F01-A29 | TEST-A29 | T-F01-04 | Gates rodam em projeto Compose distinto do ambiente de demonstração, sem remover volumes alheios; falha de bootstrap ou cleanup retorna não zero. |
| H03 | A29 | F01 | local | C-F01-A29 | TEST-A29 | T-F01-04 | Gates rodam em projeto Compose distinto do ambiente de demonstração, sem remover volumes alheios; falha de bootstrap ou cleanup retorna não zero. |
| R13 | A30 | F02 | local | C-F02-A30 | TEST-A30 | T-F02-03 | Cadastro ignora papel recebido; sessão é rotacionada no login e invalidada no logout; mutações web exigem CSRF e redirecionamento local seguro. |
| R01 | A31 | F03 | local | C-F03-A31 | TEST-A31 | T-F03-02 | Edição revalida a data no instante da escrita e não aceita frações de vaga, centavos fracionários ou valores fora dos limites documentados; nenhuma escrita parcial. |
| R03 | A31 | F03 | local | C-F03-A31 | TEST-A31 | T-F03-02 | Edição revalida a data no instante da escrita e não aceita frações de vaga, centavos fracionários ou valores fora dos limites documentados; nenhuma escrita parcial. |
| R06 | A32 | F04 | local | C-F04-A32 | TEST-A32 | T-F04-02 | Falha ao criar job reverte reserva; colisão de código usa savepoint e retry limitado; conflitos inesperados não viram sold_out. |
| R09 | A32 | F04 | local | C-F04-A32 | TEST-A32 | T-F04-02 | Falha ao criar job reverte reserva; colisão de código usa savepoint e retry limitado; conflitos inesperados não viram sold_out. |
| R07 | A33 | F04 | local | C-F04-A33 | TEST-A33 | T-F04-03 | Worker concorrente obedece event→ticket→job e revalida estado/vencimento; nenhuma espera de gateway ou lock global; transação abortada é retomável. |
| R08 | A33 | F04 | local | C-F04-A33 | TEST-A33 | T-F04-03 | Worker concorrente obedece event→ticket→job e revalida estado/vencimento; nenhuma espera de gateway ou lock global; transação abortada é retomável. |
| R11 | A33 | F04 | local | C-F04-A33 | TEST-A33 | T-F04-03 | Worker concorrente obedece event→ticket→job e revalida estado/vencimento; nenhuma espera de gateway ou lock global; transação abortada é retomável. |
| API | A34 | F06 | local | C-F06-A34 | TEST-A34 | T-F06-03 | Autorização antecede leitura/parse do corpo; JSON inválido, null, array, tipo errado, cartão Unicode e e-mail inválido respondem 422 após chave válida; precedência vale em eventos ausentes e esgotados. |
| R06 | A34 | F06 | local | C-F06-A34 | TEST-A34 | T-F06-03 | Autorização antecede leitura/parse do corpo; JSON inválido, null, array, tipo errado, cartão Unicode e e-mail inválido respondem 422 após chave válida; precedência vale em eventos ausentes e esgotados. |
| R07 | A34 | F06 | local | C-F06-A34 | TEST-A34 | T-F06-03 | Autorização antecede leitura/parse do corpo; JSON inválido, null, array, tipo errado, cartão Unicode e e-mail inválido respondem 422 após chave válida; precedência vale em eventos ausentes e esgotados. |
| R05 | A35 | F07 | local | C-F07-A35 | TEST-A35 | T-F07-03 | Leitura de gestão/painel usa snapshot único incluindo capacidade/status/owner e agregados; corridas de edição e cancelamento não produzem combinações impossíveis. |
| R11 | A35 | F07 | local | C-F07-A35 | TEST-A35 | T-F07-03 | Leitura de gestão/painel usa snapshot único incluindo capacidade/status/owner e agregados; corridas de edição e cancelamento não produzem combinações impossíveis. |
| R12 | A35 | F07 | local | C-F07-A35 | TEST-A35 | T-F07-03 | Leitura de gestão/painel usa snapshot único incluindo capacidade/status/owner e agregados; corridas de edição e cancelamento não produzem combinações impossíveis. |
| R07 | A36 | F07 | local | C-F07-A36 | TEST-A36 | T-F07-04 | Corridas reserva/cancelamento, gateway/cancelamento e check-in/cancelamento terminam em estado serial válido, sem 5xx ou entrada após cancelamento. |
| R10 | A36 | F07 | local | C-F07-A36 | TEST-A36 | T-F07-04 | Corridas reserva/cancelamento, gateway/cancelamento e check-in/cancelamento terminam em estado serial válido, sem 5xx ou entrada após cancelamento. |
| R11 | A36 | F07 | local | C-F07-A36 | TEST-A36 | T-F07-04 | Corridas reserva/cancelamento, gateway/cancelamento e check-in/cancelamento terminam em estado serial válido, sem 5xx ou entrada após cancelamento. |
| H03 | A37 | F01 | local | C-F01-A37 | TEST-A37 | T-F01-04 | Gate documental diferencia baseline, candidato local e release; relatório incompleto, falso PASS, arquivo alterado ou estado inconsistente causam falha na fase apropriada. |
| H01 | X01 | F02 | local | C-F02-X01 | TEST-X01 | T-F02-04 | Após up com seed, A/B/P autenticam; duas execuções da seed não duplicam contas. |
| H02 | X01 | F02 | local | C-F02-X01 | TEST-X01 | T-F02-04 | Após up com seed, A/B/P autenticam; duas execuções da seed não duplicam contas. |
| H01 | X02 | F03 | local | C-F03-X02 | TEST-X02 | T-F03-04 | Migração e clock da fundação permitem criação e rejeição de data vencida. |
| R01 | X02 | F03 | local | C-F03-X02 | TEST-X02 | T-F03-04 | Migração e clock da fundação permitem criação e rejeição de data vencida. |
| R04 | X03 | F03 | local | C-F03-X03 | TEST-X03 | T-F03-04 | URL de gestão e listagem usam dono da sessão; B não pode editar/publicar A. |
| R13 | X03 | F03 | local | C-F03-X03 | TEST-X03 | T-F03-04 | URL de gestão e listagem usam dono da sessão; B não pode editar/publicar A. |
| H01 | X04 | F04 | local | C-F04-X04 | TEST-X04 | T-F04-04 | Worker do Compose consome job persistido após reinício sem chave real. |
| R08 | X04 | F04 | local | C-F04-X04 | TEST-X04 | T-F04-04 | Worker do Compose consome job persistido após reinício sem chave real. |
| R02 | X05 | F04 | local | C-F04-X05 | TEST-X05 | T-F04-04 | Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação. |
| R03 | X05 | F04 | local | C-F04-X05 | TEST-X05 | T-F04-04 | Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação. |
| R05 | X05 | F04 | local | C-F04-X05 | TEST-X05 | T-F04-04 | Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação. |
| R07 | X05 | F04 | local | C-F04-X05 | TEST-X05 | T-F04-04 | Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação. |
| R09 | X06 | F05 | local | C-F05-X06 | TEST-X06 | T-F05-04 | Sessão define dono do ingresso; anônimo e outra conta não veem compra pessoal. |
| R13 | X06 | F05 | local | C-F05-X06 | TEST-X06 | T-F05-04 | Sessão define dono do ingresso; anônimo e outra conta não veem compra pessoal. |
| R02 | X07 | F05 | local | C-F05-X07 | TEST-X07 | T-F05-04 | A publicação e as vagas calculadas por F03 chegam à vitrine; draft/cancelled não são exibidos, inclusive fixture cancelada. A ação real de cancelar é validada em X14. |
| R05 | X07 | F05 | local | C-F05-X07 | TEST-X07 | T-F05-04 | A publicação e as vagas calculadas por F03 chegam à vitrine; draft/cancelled não são exibidos, inclusive fixture cancelada. A ação real de cancelar é validada em X14. |
| R06 | X08 | F05 | local | C-F05-X08 | TEST-X08 | T-F05-04 | Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine. |
| R08 | X08 | F05 | local | C-F05-X08 | TEST-X08 | T-F05-04 | Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine. |
| R09 | X08 | F05 | local | C-F05-X08 | TEST-X08 | T-F05-04 | Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine. |
| R02 | X09 | F06 | local | C-F06-X09 | TEST-X09 | T-F06-04 | A listagem de parceiros reflete publicação, preço e capacidade de F03; fixtures draft/cancelled ficam fora. Cancelamento real será validado em X15. |
| R03 | X09 | F06 | local | C-F06-X09 | TEST-X09 | T-F06-04 | A listagem de parceiros reflete publicação, preço e capacidade de F03; fixtures draft/cancelled ficam fora. Cancelamento real será validado em X15. |
| R05 | X09 | F06 | local | C-F06-X09 | TEST-X09 | T-F06-04 | A listagem de parceiros reflete publicação, preço e capacidade de F03; fixtures draft/cancelled ficam fora. Cancelamento real será validado em X15. |
| API | X09 | F06 | local | C-F06-X09 | TEST-X09 | T-F06-04 | A listagem de parceiros reflete publicação, preço e capacidade de F03; fixtures draft/cancelled ficam fora. Cancelamento real será validado em X15. |
| R06 | X10 | F06 | local | C-F06-X10 | TEST-X10 | T-F06-04 | API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture. |
| R07 | X10 | F06 | local | C-F06-X10 | TEST-X10 | T-F06-04 | API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture. |
| R09 | X10 | F06 | local | C-F06-X10 | TEST-X10 | T-F06-04 | API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture. |
| API | X10 | F06 | local | C-F06-X10 | TEST-X10 | T-F06-04 | API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture. |
| R05 | X16 | F06 | integrated | C-F06-X16 | TEST-X16 | T-W6-02 | Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web. |
| R07 | X16 | F06 | integrated | C-F06-X16 | TEST-X16 | T-W6-02 | Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web. |
| R09 | X16 | F06 | integrated | C-F06-X16 | TEST-X16 | T-W6-02 | Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web. |
| API | X16 | F06 | integrated | C-F06-X16 | TEST-X16 | T-W6-02 | Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web. |
| R13 | X11 | F07 | local | C-F07-X11 | TEST-X11 | T-F07-04 | Todas as ações operacionais respeitam guarda de dono. |
| R04 | X12 | F07 | local | C-F07-X12 | TEST-X12 | T-F07-04 | Cancelamento bloqueia publicação/edição e integra gestão em URL existente. |
| R11 | X12 | F07 | local | C-F07-X12 | TEST-X12 | T-F07-04 | Cancelamento bloqueia publicação/edição e integra gestão em URL existente. |
| R10 | X13 | F07 | local | C-F07-X13 | TEST-X13 | T-F07-04 | Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive. |
| R11 | X13 | F07 | local | C-F07-X13 | TEST-X13 | T-F07-04 | Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive. |
| R12 | X13 | F07 | local | C-F07-X13 | TEST-X13 | T-F07-04 | Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive. |
| R06 | X14 | F07 | integrated | C-F07-X14 | TEST-X14 | T-W6-02 | Com UI e operações integradas, uma compra web confirmada incrementa painel, permite check-in e, após cancelamento, some do catálogo e vira estornada em Meus ingressos. |
| R09 | X14 | F07 | integrated | C-F07-X14 | TEST-X14 | T-W6-02 | Com UI e operações integradas, uma compra web confirmada incrementa painel, permite check-in e, após cancelamento, some do catálogo e vira estornada em Meus ingressos. |
| R10 | X14 | F07 | integrated | C-F07-X14 | TEST-X14 | T-W6-02 | Com UI e operações integradas, uma compra web confirmada incrementa painel, permite check-in e, após cancelamento, some do catálogo e vira estornada em Meus ingressos. |
| R11 | X14 | F07 | integrated | C-F07-X14 | TEST-X14 | T-W6-02 | Com UI e operações integradas, uma compra web confirmada incrementa painel, permite check-in e, após cancelamento, some do catálogo e vira estornada em Meus ingressos. |
| R12 | X14 | F07 | integrated | C-F07-X14 | TEST-X14 | T-W6-02 | Com UI e operações integradas, uma compra web confirmada incrementa painel, permite check-in e, após cancelamento, some do catálogo e vira estornada em Meus ingressos. |
| R05 | X15 | F07 | integrated | C-F07-X15 | TEST-X15 | T-W6-02 | Com API e operações integradas, ingresso de parceiro conta na lotação e painel, permite check-in e consulta checkedIn; cancelar remove evento da lista, bloqueia POST, estorna e conserva consulta do ticket. |
| R07 | X15 | F07 | integrated | C-F07-X15 | TEST-X15 | T-W6-02 | Com API e operações integradas, ingresso de parceiro conta na lotação e painel, permite check-in e consulta checkedIn; cancelar remove evento da lista, bloqueia POST, estorna e conserva consulta do ticket. |
| R10 | X15 | F07 | integrated | C-F07-X15 | TEST-X15 | T-W6-02 | Com API e operações integradas, ingresso de parceiro conta na lotação e painel, permite check-in e consulta checkedIn; cancelar remove evento da lista, bloqueia POST, estorna e conserva consulta do ticket. |
| R11 | X15 | F07 | integrated | C-F07-X15 | TEST-X15 | T-W6-02 | Com API e operações integradas, ingresso de parceiro conta na lotação e painel, permite check-in e consulta checkedIn; cancelar remove evento da lista, bloqueia POST, estorna e conserva consulta do ticket. |
| R12 | X15 | F07 | integrated | C-F07-X15 | TEST-X15 | T-W6-02 | Com API e operações integradas, ingresso de parceiro conta na lotação e painel, permite check-in e consulta checkedIn; cancelar remove evento da lista, bloqueia POST, estorna e conserva consulta do ticket. |
| API | X15 | F07 | integrated | C-F07-X15 | TEST-X15 | T-W6-02 | Com API e operações integradas, ingresso de parceiro conta na lotação e painel, permite check-in e consulta checkedIn; cancelar remove evento da lista, bloqueia POST, estorna e conserva consulta do ticket. |
| SDD | P01 | RELEASE | release | C-RELEASE-P01 | TEST-P01 | T-W6-03 | PRD >=5 features, fornece/consome, DAG e waves; todas R01–R13 citadas, cada aresta coberta. |
| SDD | P02 | RELEASE | release | C-RELEASE-P02 | TEST-P02 | T-W6-03 | Spec, plano e contrato por feature, todos os critérios e cross-feature mapeados. |
| EVAL | P03 | RELEASE | release | C-RELEASE-P03 | TEST-P03 | T-W6-03 | Para cada feature há relatório novo e imutável, com data UTC, SHA completo, ferramenta, modelo, identidade de sessão e evidência por item; último relatório integrado aprova tudo aplicável. |
| STATE | P04 | RELEASE | release | C-RELEASE-P04 | TEST-P04 | T-W6-03 | Estado final aponta ao último relatório aprovado, commit implementado e PR de cada feature; nenhum concluído sem integração verificada. |
| PAR | P05 | RELEASE | release | C-RELEASE-P05 | TEST-P05 | T-W6-03 | Pelo menos uma wave paralela via PRs mergeados; primeiro commit de cada PR anterior ao último de todos os demais. |
| DELIVERY | P06 | RELEASE | release | C-RELEASE-P06 | TEST-P06 | T-W6-03 | Repo público único, main com README completo; fluxo externo 1–18 aprovado em clone limpo. |

## Governança
Alterações começam no brief/PRD, com aprovação do coordenador, atualização do JSON, matriz, contratos e catálogo; não reduzir cobertura. Cada teste deve ter evidência real no relatório. A37 testa a própria rastreabilidade.
