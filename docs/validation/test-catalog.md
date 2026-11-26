# Catálogo de testes | a implementar

IDs são contratos de teste, não resultados. Cada teste automatizado futuro deve incluir seu ID no nome, docstring ou metadado do runner, e registrar evidência no relatório. Testes de UI reais via Playwright em container; testes de domínio PostgreSQL com TransactionTestCase; API via HTTP e probes. `./bin/gates Fxx` e `./bin/gates` são interfaces planejadas.

## TEST-A01 | A01

Tarefa de implementação/validação: `T-F01-03`.

- Requisito: H01. Contrato: C-F01-A01.
- Setup e ação: Clonar SHA em pasta temporária; executar up; verificar HTTP e compose ps.
- Oráculo: Clone limpo: ./bin/up constrói, migra, semeia e espera web/worker/DB prontos; /health/ready retorna 200 sem configuração manual.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A02 | A02

Tarefa de implementação/validação: `T-F01-03`.

- Requisito: H02. Contrato: C-F01-A02.
- Setup e ação: Executar up, seed duas vezes, down, provar porta fechada e ps vazio, up novamente; comparar IDs e autenticação após F02.
- Oráculo: ./bin/down encerra todos os containers e portas iniciados; nova subida conserva dados e seed não duplica contas.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A03 | A03

Tarefa de implementação/validação: `T-F01-01`.

- Requisito: H03. Contrato: C-F01-A03.
- Setup e ação: Executar gates e injetar falha em cópia descartável; capturar códigos de saída.
- Oráculo: ./bin/gates falha com teste quebrado, executa testes reais e lint, usa DB isolado e passa com testes válidos.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A04 | A04

Tarefa de implementação/validação: `T-F01-03`.

- Requisito: H04. Contrato: C-F01-A04.
- Setup e ação: Inspeção dos arquivos, ambiente sem .env e sem credenciais externas.
- Oráculo: AGENTS.md e README contêm comandos, endereços, credenciais de seed, mapa; modo padrão não exige gateway real.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A05 | A05

Tarefa de implementação/validação: `T-F01-02`.

- Requisito: R05, R09. Contrato: C-F01-A05.
- Setup e ação: Aplicar migração em DB vazio e reexecutar; tentar inserir status inválido, código duplicado, capacidade zero e FK órfã; todas rejeitadas.
- Oráculo: Schema possui FKs, unicidade de código, restrições de status, lotação e preço; migrações reexecutáveis.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A06 | A06

Tarefa de implementação/validação: `T-F02-01`.

- Requisito: R13. Contrato: C-F02-A06.
- Setup e ação: Browser: cadastro/login/logout; POST com role=organizer; consulta DB somente para verificar hash e papel.
- Oráculo: Cadastro público cria somente participante, e-mail normalizado único; senha armazenada como hash; login válido e logout invalidam sessão; erro genérico em credenciais inválidas.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A07 | A07

Tarefa de implementação/validação: `T-F02-02`.

- Requisito: R13. Contrato: C-F02-A07.
- Setup e ação: Sessões independentes A/B/P/anônima; fixture de evento A; assert HTTP 404 para B, ausência de nome/dados e nenhuma mutação; 403 ou redirect para demais.
- Oráculo: Visitante e participante não acessam rotas de gestão; B não lê nem modifica eventos de A, incluindo URL direta e POST forjado.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A08 | A08

Tarefa de implementação/validação: `T-F02-02`.

- Requisito: R09, R13. Contrato: C-F02-A08.
- Setup e ação: Testar guarda de participante com duas contas e recurso fixture; tentar usar X-Api-Key em rota web; negar.
- Oráculo: Participante só tem acesso aos próprios recursos; parceiro não cria sessão web nem vincula conta pelo e-mail.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A09 | A09

Tarefa de implementação/validação: `T-F03-01`.

- Requisito: R01. Contrato: C-F03-A09.
- Setup e ação: Tabela de casos com agora, passado, futuro, 0, -1, 1.5, preço zero e campos vazios; checar persistência.
- Oráculo: Nome/local não vazios; lotação inteira >=1; preço em centavos >0; início estritamente futuro em criar e editar, inclusive requisição direta.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A10 | A10

Tarefa de implementação/validação: `T-F03-03`.

- Requisito: R02, R04. Contrato: C-F03-A10.
- Setup e ação: Criar E1, consultar catálogo antes/depois e abrir URL de gestão com dono.
- Oráculo: Evento nasce draft; publicar torna visível a consulta pública; gestão tem URL estável e lista apenas próprios eventos.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A11 | A11

Tarefa de implementação/validação: `T-F03-02`.

- Requisito: R03, R05. Contrato: C-F03-A11.
- Setup e ação: Fixtures de dois ingressos ocupando; reduzir para 1 rejeita, 2/3 aceitam; snapshot histórico inalterado.
- Oráculo: Editar sob lock do evento; capacidade abaixo de pending+confirmed é rejeitada; igual/acima aceita; preço novo não altera snapshot de ingressos.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A12 | A12

Tarefa de implementação/validação: `T-F03-02`.

- Requisito: R11. Contrato: C-F03-A12.
- Setup e ação: Fixture de estado cancelled; POST edição/publicação e leitura pública; negar sem mutação.
- Oráculo: Evento cancelled não pode ser alterado/republicado; catálogo e disponibilidade pública o excluem.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A13 | A13

Tarefa de implementação/validação: `T-F04-02`.

- Requisito: R05, R06, R09. Contrato: C-F04-A13.
- Setup e ação: Invocar reserve e consultar DB; medir tempo <2s em ambiente local estável; rollback injetado não deixa ticket/job; colisão de código tratada.
- Oráculo: Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A14 | A14

Tarefa de implementação/validação: `T-F04-02`.

- Requisito: R07. Contrato: C-F04-A14.
- Setup e ação: TransactionTestCase com barreira de threads/conexões distintas e PostgreSQL real; consultar ocupação, jobs e erros; repetir 10 vezes como robustez.
- Oráculo: Quando lotação esgota, não cria ingresso/job; 30 reservas concorrentes sobre capacidade 5 dão exatamente 5 sucessos/25 sold_out, em duas rodadas novas.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A15 | A15

Tarefa de implementação/validação: `T-F04-03`.

- Requisito: R08. Contrato: C-F04-A15.
- Setup e ação: Testes unitários de mapeamento e integração com relógio real: polling, timestamps, ocupação; não acelerar teste de prazo.
- Oráculo: Gateway padrão confirma 0001 e recusa 0002/outros em 2–5s; confirma 0003 e recusa 0004 em 30–40s; recusa libera uma vaga.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A16 | A16

Tarefa de implementação/validação: `T-F04-03`.

- Requisito: R03, R11. Contrato: C-F04-A16.
- Setup e ação: Testar preço antes/depois, aplicar resultado duas vezes e fixtures cancelled/refunded; parar/reiniciar worker com job pendente e verificar efeito único.
- Oráculo: Snapshot de preço é capturado sob lock; finalize só altera pending de evento publicado; resultado duplicado/tardio não revive terminal; job sobrevive reinício.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A17 | A17

Tarefa de implementação/validação: `T-F04-01`.

- Requisito: R06. Contrato: C-F04-A17.
- Setup e ação: Casos 15/17 dígitos, letras, Unicode, espaços, e-mail inválido; assert contagem zero e inspeção DB/logs.
- Oráculo: Cartão diferente de 16 dígitos ASCII falha antes de criar ingresso; e-mail malformado na compra de parceiro falha; PAN não persiste nem aparece em logs.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A18 | A18

Tarefa de implementação/validação: `T-F05-01`.

- Requisito: R02, R05, R07. Contrato: C-F05-A18.
- Setup e ação: Browser: draft/publicado/cancelled, capacidade 1 pendente e tentativa direta sem vaga.
- Oráculo: Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A19 | A19

Tarefa de implementação/validação: `T-F05-02`.

- Requisito: R06, R08, R09. Contrato: C-F05-A19.
- Setup e ação: Playwright: cadastro, login, compra, tela pending e polling/reload até confirmed; conferir código em DB ou via F06 após integração.
- Oráculo: Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A20 | A20

Tarefa de implementação/validação: `T-F05-02`.

- Requisito: R09, R13. Contrato: C-F05-A20.
- Setup e ação: Fixtures dos cinco estados; duas contas; ingresso partner com mesmo e-mail não aparece; POST anônimo sem efeito.
- Oráculo: Meus ingressos filtra por participant_id autenticado, não por e-mail, e mostra todos os cinco rótulos; visitante não compra.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A21 | A21

Tarefa de implementação/validação: `T-F06-02`.

- Requisito: API, R02, R05. Contrato: C-F06-A21.
- Setup e ação: HTTP GET com fixtures dos estados; comparar shape e valores; esgotado permanece com 0.
- Oráculo: GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A22 | A22

Tarefa de implementação/validação: `T-F06-02`.

- Requisito: API, R06, R07. Contrato: C-F06-A22.
- Setup e ação: Tabela HTTP: JSON inválido e evento inexistente ->422; inválido e esgotado ->422; válido draft/cancelled/inexistente ->404; lotado ->409; válido ->202.
- Oráculo: POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A23 | A23

Tarefa de implementação/validação: `T-F06-02`.

- Requisito: API, R09, R13. Contrato: C-F06-A23.
- Setup e ação: HTTP em três rotas × sem/errada e com payload inválido; consulta fixtures web/partner e inexistente; checar JSON exato.
- Oráculo: GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A24 | A24

Tarefa de implementação/validação: `T-F06-03`.

- Requisito: R07, API. Contrato: C-F06-A24.
- Setup e ação: Runner HTTP com barreira, 30 conexões, validar corpo e IDs únicos, consultar cada aceito e availableSeats=0; usar novo evento por rodada.
- Oráculo: Em duas rodadas HTTP reais, cada evento novo de capacidade 5 recebe 30 POST simultâneos com cartão 0001: 5×202 e 25×409, sem 5xx; depois 5 confirmados.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A25 | A25

Tarefa de implementação/validação: `T-F07-01`.

- Requisito: R10. Contrato: C-F07-A25.
- Setup e ação: Fixtures código inválido/outro evento, cancelado, pending/declined/refunded, confirmado já usado e novo; corrida com duas sessões do dono.
- Oráculo: Check-in aplica exatamente as cinco mensagens na ordem definida; só confirmed não utilizado recebe checkedIn=true; dois check-ins concorrentes liberam uma entrada.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A26 | A26

Tarefa de implementação/validação: `T-F07-02`.

- Requisito: R11. Contrato: C-F07-A26.
- Setup e ação: Criar slow 0003 + fast 0001, cancelar antes de 30s; medir <=10s, aguardar >=45s, repetir cancelamento e testar ações; corrida cancelamento/reserva/finalização.
- Oráculo: Cancelar publicado é irreversível; na mesma transação confirmed→refunded e pending→cancelled, sem alteração de declined; gateway posterior não modifica; edit/publish/compra rejeitados.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A27 | A27

Tarefa de implementação/validação: `T-F07-03`.

- Requisito: R05, R12. Contrato: C-F07-A27.
- Setup e ação: Fixture 10000+10000+15000 confirmados, 1 check-in, recusado e estornado; conferir receita 35000 e todas as contagens; após cancelar comparar zeros e estornos.
- Oráculo: Painel mostra seis métricas com snapshots de preço e ambos os canais; check-ins somente confirmed; cancelado tem receita/vagas/confirmados/pendentes/check-ins zero.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-A28 | A28

Tarefa de implementação/validação: `T-F07-03`.

- Requisito: R04, R13. Contrato: C-F07-A28.
- Setup e ação: Browser A/B/P/visitante, POST forjado de B, verificar nenhum dado nem alteração; abrir gestão de A e executar ações.
- Oráculo: Check-in, cancelar e painel ficam na URL de gestão de cada evento; todas as ações exigem dono inclusive requisição direta.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X01 | X01

Tarefa de implementação/validação: `T-F02-04`.

- Requisito: H01, H02. Contrato: C-F02-X01.
- Setup e ação: Subir ambiente limpo, login das três contas, comparar IDs após reseed.
- Oráculo: Após up com seed, A/B/P autenticam; duas execuções da seed não duplicam contas.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X02 | X02

Tarefa de implementação/validação: `T-F03-04`.

- Requisito: H01, R01. Contrato: C-F03-X02.
- Setup e ação: DB limpo migrado; criar evento futuro e rejeitar ontem.
- Oráculo: Migração e clock da fundação permitem criação e rejeição de data vencida.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X03 | X03

Tarefa de implementação/validação: `T-F03-04`.

- Requisito: R04, R13. Contrato: C-F03-X03.
- Setup e ação: Browser e POST direto B contra E1 de A; ausência de dados, estado intacto.
- Oráculo: URL de gestão e listagem usam dono da sessão; B não pode editar/publicar A.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X04 | X04

Tarefa de implementação/validação: `T-F04-04`.

- Requisito: H01, R08. Contrato: C-F04-X04.
- Setup e ação: Comprar slow, reiniciar worker antes de due; obter status final uma vez.
- Oráculo: Worker do Compose consome job persistido após reinício sem chave real.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X05 | X05

Tarefa de implementação/validação: `T-F04-04`.

- Requisito: R02, R03, R05, R07. Contrato: C-F04-X05.
- Setup e ação: Corrida compra × redução e compra × preço; conferir invariantes e snapshots.
- Oráculo: Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X06 | X06

Tarefa de implementação/validação: `T-F05-04`.

- Requisito: R09, R13. Contrato: C-F05-X06.
- Setup e ação: Dois browsers com sessões distintas; compra e acesso cruzado.
- Oráculo: Sessão define dono do ingresso; anônimo e outra conta não veem compra pessoal.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X07 | X07

Tarefa de implementação/validação: `T-F05-04`.

- Requisito: R02, R05. Contrato: C-F05-X07.
- Setup e ação: Criar draft, publicar, reservar até lotar, cancelar fixture; recarregar catálogo.
- Oráculo: Publicar/lotar/cancelar reflete na vitrine sem cache obsoleto.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X08 | X08

Tarefa de implementação/validação: `T-F05-04`.

- Requisito: R06, R08, R09. Contrato: C-F05-X08.
- Setup e ação: Comprar 0004, observar lotação, após 45s ver declined e vaga.
- Oráculo: Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X09 | X09

Tarefa de implementação/validação: `T-F06-04`.

- Requisito: R02, R03, R05, API. Contrato: C-F06-X09.
- Setup e ação: GET antes/depois publicação, edição e cancelamento fixture.
- Oráculo: API usa catálogo e centavos/ocupação canônicos; edição preço/capacidade reflete na listagem.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X10 | X10

Tarefa de implementação/validação: `T-F06-04`.

- Requisito: R06, R07, R09, API. Contrato: C-F06-X10.
- Setup e ação: POST simultâneo e GET ticket, comparar dados de ledger.
- Oráculo: API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X16 | X16

Tarefa de implementação/validação: `T-W6-02`.

- Requisito: R05, R07, R09, API. Contrato: C-F06-X16.
- Setup e ação: Corrida web e API com capacidade 1; um sucesso, outro esgotado; testar isolamento pelo e-mail.
- Oráculo: Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X11 | X11

Tarefa de implementação/validação: `T-F07-04`.

- Requisito: R13. Contrato: C-F07-X11.
- Setup e ação: B tenta check-in e cancelamento de A, sem efeito e sem informação.
- Oráculo: Todas as ações operacionais respeitam guarda de dono.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X12 | X12

Tarefa de implementação/validação: `T-F07-04`.

- Requisito: R04, R11. Contrato: C-F07-X12.
- Setup e ação: Cancelar publicado e tentar editar e republicar via POST; consultar catálogo.
- Oráculo: Cancelamento bloqueia publicação/edição e integra gestão em URL existente.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X13 | X13

Tarefa de implementação/validação: `T-F07-04`.

- Requisito: R10, R11, R12. Contrato: C-F07-X13.
- Setup e ação: Combinar slow, fast, check-in, cancelar e esperar resultado tardio.
- Oráculo: Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X14 | X14

Tarefa de implementação/validação: `T-W6-02`.

- Requisito: R06, R09, R10, R11, R12. Contrato: C-F07-X14.
- Setup e ação: Fluxo browser: comprar, confirmar, validar código, cancelar, recarregar ambos.
- Oráculo: Integração final (não dependência de implementação): compra web aparece no painel e permite check-in; cancelamento aparece em Meus ingressos.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-X15 | X15

Tarefa de implementação/validação: `T-W6-02`.

- Requisito: R05, R07, R10, R11, R12, API. Contrato: C-F07-X15.
- Setup e ação: HTTP+browser: compra, consultar checkedIn, cancelar, verificar 404 e estorno.
- Oráculo: Integração final: compra partner soma painel, é validada no check-in e deixa API após cancelamento.
- Evidência: saída do runner com asserções; HTTP status/body, screenshots ou SQL apenas quando aplicável; limpeza de fixture após execução. Não marcar PASS se houve skip.

## TEST-P01

Tarefa de implementação/validação: `T-W6-03`.

PRD >=5 features, fornece/consome, DAG e waves; todas R01–R13 citadas, cada aresta coberta. Inspecionar artefatos e histórico real, registrar comandos/URLs e veredito; contrato C-RELEASE-P01.

## TEST-P02

Tarefa de implementação/validação: `T-W6-03`.

Spec, plano e contrato por feature, todos os critérios e cross-feature mapeados. Inspecionar artefatos e histórico real, registrar comandos/URLs e veredito; contrato C-RELEASE-P02.

## TEST-P03

Tarefa de implementação/validação: `T-W6-03`.

Cada feature aprovada em avaliação independente; relatório imutável com data, SHA, ferramenta, modelo, evidência por item. Inspecionar artefatos e histórico real, registrar comandos/URLs e veredito; contrato C-RELEASE-P03.

## TEST-P04

Tarefa de implementação/validação: `T-W6-03`.

Estado final bate com relatórios existentes e mais recentes; sem status concluído sem aprovação. Inspecionar artefatos e histórico real, registrar comandos/URLs e veredito; contrato C-RELEASE-P04.

## TEST-P05

Tarefa de implementação/validação: `T-W6-03`.

Pelo menos uma wave paralela via PRs mergeados; primeiro commit de cada PR anterior ao último de todos os demais. Inspecionar artefatos e histórico real, registrar comandos/URLs e veredito; contrato C-RELEASE-P05.

## TEST-P06

Tarefa de implementação/validação: `T-W6-03`.

Repo público único, main com README completo; fluxo externo 1–18 aprovado em clone limpo. Inspecionar artefatos e histórico real, registrar comandos/URLs e veredito; contrato C-RELEASE-P06.
