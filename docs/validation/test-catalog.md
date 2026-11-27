# Catálogo de testes e evidências

Cada seção é um teste ou grupo parametrizado obrigatório, a implementar no runner indicado. Os cenários não são resultados executados. IDs estáveis devem constar nos nomes/tags dos testes e no relatório. A execução de processo é manual/automatizada conforme o item; nenhuma fixture substitui o fluxo público.

## TEST-A01 | A01

- **Nível / fase:** e2e / local.
- **Preparar:** Clone de SHA limpo; Docker/Compose; sem .env; sem imagem local obrigatória.
- **Executar:** Executar bash bin/up; GET readiness pelo host; inspect serviços; autenticar seed quando F02 disponível.
- **Oráculo:** Exit 0; DB, web e worker prontos; migração/seed one-shot concluídas; nenhuma chave real; antes de F02 comprovar linhas e hashes da seed.
- **Evidência mínima:** Clonar SHA em pasta temporária; executar up; verificar HTTP e compose ps. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F01-A01 · T-F01-03 · H01.

## TEST-A02 | A02

- **Nível / fase:** e2e / local.
- **Preparar:** Stack da demo com usuário e evento sentinela.
- **Executar:** Executar down; verificar ausência de containers e listener; subir novamente; seed outra vez; comparar IDs e quantidade.
- **Oráculo:** Nenhum serviço do projeto ativo; dados persistem e seed permanece com 2 organizadores + 1 participante seed, sem duplicação.
- **Evidência mínima:** Executar up, seed duas vezes, down, provar porta fechada e ps vazio, up novamente; comparar IDs e autenticação após F02. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F01-A02 · T-F01-03 · H02.

## TEST-A03 | A03

- **Nível / fase:** integration / local.
- **Preparar:** Ambiente de teste exclusivo e teste propositalmente falho em cópia.
- **Executar:** Rodar gates íntegro; repetir com asserção false e depois restaurar; verificar código de saída e cleanup.
- **Oráculo:** Suíte íntegra exit 0; versão quebrada exit diferente de 0; relatório lista testes realmente executados.
- **Evidência mínima:** Executar gates e injetar falha em cópia descartável; capturar códigos de saída. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F01-A03 · T-F01-01 · H03.

## TEST-A04 | A04

- **Nível / fase:** e2e / local.
- **Preparar:** README e AGENTS no candidato.
- **Executar:** Seguir comandos e verificar nomes, porta, chave local, mapa e defaults.
- **Oráculo:** Comandos reproduzíveis; sem setup manual; links internos existentes; endereços corretos.
- **Evidência mínima:** Inspeção dos arquivos, ambiente sem .env e sem credenciais externas. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F01-A04 · T-F01-03 · H04.

## TEST-A05 | A05

- **Nível / fase:** integration / local.
- **Preparar:** Banco PostgreSQL migrado em volume vazio.
- **Executar:** Forçar duplicata de código, FK inexistente, status inválido, preço 0, capacidade 0, buyer misto, dois jobs por ticket; migrar de novo.
- **Oráculo:** Todas as escritas inválidas falham; dados válidos persistem; sem migração pendente.
- **Evidência mínima:** Aplicar migração em DB vazio e reexecutar; tentar inserir status inválido, código duplicado, capacidade zero e FK órfã; todas rejeitadas. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F01-A05 · T-F01-02 · R05, R09.

## TEST-A06 | A06

- **Nível / fase:** integration / local.
- **Preparar:** Browser sem sessão e contas seed.
- **Executar:** Cadastrar, repetir e-mail com caixa distinta, login incorreto/correto, logout; consultar hash sem registrá-lo.
- **Oráculo:** Participante único; senha não em claro; sessão só após sucesso; logout invalida cookie anterior.
- **Evidência mínima:** Browser: cadastro/login/logout; POST com role=organizer; consulta DB somente para verificar hash e papel. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F02-A06 · T-F02-01 · R13.

## TEST-A07 | A07

- **Nível / fase:** integration / local.
- **Preparar:** Fixtures de eventos A/B e atores anônimo/P/A/B.
- **Executar:** Exercitar guardas com IDs de A e B; forjar proprietário no payload; comparar resultados e dados.
- **Oráculo:** Anônimo redirecionado no GET, participante 403, B recebe 404 genérico ao acessar A; nenhuma mutação.
- **Evidência mínima:** Sessões independentes A/B/P/anônima; fixture de evento A; assert HTTP 404 para B, ausência de nome/dados e nenhuma mutação; 403 ou redirect para demais. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F02-A07 · T-F02-02 · R13.

## TEST-A08 | A08

- **Nível / fase:** integration / local.
- **Preparar:** Dois participantes com e-mails distintos e credencial de parceiro.
- **Executar:** Forjar ID de participante no request/contexto, tentar autenticar por chave; validar identidade retornada.
- **Oráculo:** ID da sessão é autoridade exclusiva; chave não cria sessão; login por e-mail continua conta distinta.
- **Evidência mínima:** Testar guarda de participante com duas contas e recurso fixture; tentar usar X-Api-Key em rota web; negar. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F02-A08 · T-F02-02 · R09, R13.

## TEST-A09 | A09

- **Nível / fase:** integration / local.
- **Preparar:** A autenticado; formulário de criação e edição.
- **Executar:** Enviar campos vazios, preço 0, capacidade 0, data ontem, depois data futura válida.
- **Oráculo:** 422 ou formulário com erros; nenhum evento inválido; sucesso cria draft com valores normalizados.
- **Evidência mínima:** Tabela de casos com agora, passado, futuro, 0, -1, 1.5, preço zero e campos vazios; checar persistência. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F03-A09 · T-F03-01 · R01.

## TEST-A10 | A10

- **Nível / fase:** integration / local.
- **Preparar:** Dois organizadores, E1 draft e E2 de B.
- **Executar:** Abrir gestão E1, listar A, consultar catálogo, publicar e recarregar.
- **Oráculo:** URL estável, apenas eventos de A na gestão, E1 fora antes e visível depois.
- **Evidência mínima:** Criar E1, consultar catálogo antes/depois e abrir URL de gestão com dono. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F03-A10 · T-F03-03 · R02, R04.

## TEST-A11 | A11

- **Nível / fase:** integration / local.
- **Preparar:** E1 com pending e confirmed, ocupação 2; preço 10000.
- **Executar:** Editar para cap 1, 2 e 3; trocar preço para 15000; comparar snapshot de tickets.
- **Oráculo:** Cap 1 nega sem mudança; 2 e 3 aceitam; ingressos anteriores continuam 10000.
- **Evidência mínima:** Fixtures de dois ingressos ocupando; reduzir para 1 rejeita, 2/3 aceitam; snapshot histórico inalterado. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F03-A11 · T-F03-02 · R03, R05.

## TEST-A12 | A12

- **Nível / fase:** integration / local.
- **Preparar:** Evento fixture cancelled, publicado e draft.
- **Executar:** Tentar editar e publicar cancelado, consultar lista pública.
- **Oráculo:** Cancelado ausente e imutável; somente publicado elegível.
- **Evidência mínima:** Fixture de estado cancelled; POST edição/publicação e leitura pública; negar sem mutação. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F03-A12 · T-F03-02 · R11.

## TEST-A13 | A13

- **Nível / fase:** integration / local.
- **Preparar:** E publicado cap 2 sem tickets; relógio de teste e worker pausado para conferir commit.
- **Executar:** Reservar web e parceiro; capturar DTO imediato, recontar tickets e jobs; comparar preço/código.
- **Oráculo:** Um ticket pending e um job por chamada; código distinto; 0 vagas após duas; não aguarda pagamento.
- **Evidência mínima:** Invocar reserve e consultar DB; medir tempo <2s em ambiente local estável; rollback injetado não deixa ticket/job; colisão de código tratada. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F04-A13 · T-F04-02 · R05, R06, R09.

## TEST-A14 | A14

- **Nível / fase:** integration / local.
- **Preparar:** PostgreSQL real, 10 eventos novos cap 5 e 30 clientes em conexões distintas.
- **Executar:** Barreira de início, usar cartões de aprovação; conferir resultados e contagem DB; rodar também cap 1 com 2 concorrentes.
- **Oráculo:** Exatamente 5/25 em todas as rodadas, 1/1 no limite; nenhuma exceção inesperada nem job órfão.
- **Evidência mínima:** TransactionTestCase com barreira de threads/conexões distintas e PostgreSQL real; consultar ocupação, jobs e erros; repetir 10 vezes como robustez. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F04-A14 · T-F04-02 · R07.

## TEST-A15 | A15

- **Nível / fase:** integration / local.
- **Preparar:** 5 eventos ou vagas independentes; worker padrão ativo; relógio monotônico + timestamps DB.
- **Executar:** Comprar cada final 0001/0002/0003/0004/9999; consultar pending e resultado até deadline; medir intervalo created→resolved, recarregar vagas.
- **Oráculo:** Aprovação/recusa corretas; 2–5 s e 30–40 s; recusa libera exatamente uma vaga; nenhum terminal antecipado.
- **Evidência mínima:** Testes unitários de mapeamento e integração com relógio real: polling, timestamps, ocupação; não acelerar teste de prazo. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F04-A15 · T-F04-03 · R08.

## TEST-A16 | A16

- **Nível / fase:** integration / local.
- **Preparar:** Ticket slow e fixtures terminais; dois preços sucessivos.
- **Executar:** Comprar antes/depois da edição; reiniciar worker antes de due; executar resolução novamente; tentar aplicar a fixture terminal.
- **Oráculo:** Preço histórico intacto; job recuperado; só uma transição; terminal nunca muda.
- **Evidência mínima:** Testar preço antes/depois, aplicar resultado duas vezes e fixtures cancelled/refunded; parar/reiniciar worker com job pendente e verificar efeito único. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F04-A16 · T-F04-03 · R03, R11.

## TEST-A17 | A17

- **Nível / fase:** integration / local.
- **Preparar:** E publicado com vaga; DB e captura sanitizada de log.
- **Executar:** Enviar cartão com 15/17 dígitos, letras, Unicode, espaços, tipo numérico; e-mail inválido; procurar número de teste em DB/logs.
- **Oráculo:** Sem ticket/job para entradas inválidas; PAN não salvo nem refletido.
- **Evidência mínima:** Casos 15/17 dígitos, letras, Unicode, espaços, e-mail inválido; assert contagem zero e inspeção DB/logs. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F04-A17 · T-F04-01 · R06.

## TEST-A18 | A18

- **Nível / fase:** e2e / local.
- **Preparar:** E1 draft, E2 publicado com vaga, E3 publicado lotado, E4 cancelado fixture.
- **Executar:** Visitar vitrine anonimamente e detalhe E3; forjar POST quando vaga termina.
- **Oráculo:** Só E2/E3 listados; mensagem Ingressos esgotados no detalhe ou tentativa; sem venda adicional.
- **Evidência mínima:** Browser: draft/publicado/cancelled, capacidade 1 pendente e tentativa direta sem vaga. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F05-A18 · T-F05-01 · R02, R05, R07.

## TEST-A19 | A19

- **Nível / fase:** e2e / local.
- **Preparar:** Browser participante novo e evento publicado disponível.
- **Executar:** Cadastrar, comprar 0001, abrir Meus ingressos imediatamente e recarregar até 5s.
- **Oráculo:** Evento e código visíveis, pendente inicialmente, confirmado até deadline; sem esperar gateway no POST.
- **Evidência mínima:** Playwright: cadastro, login, compra, tela pending e polling/reload até confirmed; conferir código em DB ou via F06 após integração. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F05-A19 · T-F05-02 · R06, R08, R09.

## TEST-A20 | A20

- **Nível / fase:** e2e / local.
- **Preparar:** Fixtures de cinco status para P, ticket de outro participante e parceiro com mesmo e-mail.
- **Executar:** Abrir Meus ingressos, trocar sessão, tentar URL/ID forjado e compra anônima.
- **Oráculo:** Só tickets do ID da sessão; cinco rótulos exatos; parceiro não aparece; visitante não compra.
- **Evidência mínima:** Fixtures dos cinco estados; duas contas; ingresso partner com mesmo e-mail não aparece; POST anônimo sem efeito. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F05-A20 · T-F05-02 · R09, R13.

## TEST-A21 | A21

- **Nível / fase:** e2e / local.
- **Preparar:** Eventos draft, published, lotado e cancelled; chave válida.
- **Executar:** GET /api/partner/events; verificar set de campos, tipos, timestamps e vagas.
- **Oráculo:** 200 array; publicados inclusive esgotados; sem dados de owner/PII; disponibilidade derivada.
- **Evidência mínima:** HTTP GET com fixtures dos estados; comparar shape e valores; esgotado permanece com 0. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F06-A21 · T-F06-02 · API, R02, R05.

## TEST-A22 | A22

- **Nível / fase:** e2e / local.
- **Preparar:** E disponível, draft, inexistente, esgotado, cancelado fixture.
- **Executar:** POST válido; em seguida combinar erro de chave, payload inválido, evento indisponível e falta de vaga.
- **Oráculo:** 202 pending exato; 401→422→404→409 na precedência; erros sem efeitos.
- **Evidência mínima:** Tabela HTTP: JSON inválido e evento inexistente ->422; inválido e esgotado ->422; válido draft/cancelled/inexistente ->404; lotado ->409; válido ->202. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F06-A22 · T-F06-02 · API, R06, R07.

## TEST-A23 | A23

- **Nível / fase:** e2e / local.
- **Preparar:** Ticket web fixture e parceiro; ID inexistente; chaves válidas e inválidas.
- **Executar:** GET ambos os tickets e ID ausente; executar as três rotas sem chave e com chave inválida.
- **Oráculo:** 200 exatamente ticketId/code/eventId/status/checkedIn booleano; 404 ticket_not_found; 401 unauthorized em 6 combinações.
- **Evidência mínima:** HTTP em três rotas × sem/errada e com payload inválido; consulta fixtures web/partner e inexistente; checar JSON exato. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F06-A23 · T-F06-02 · API, R09, R13.

## TEST-A24 | A24

- **Nível / fase:** e2e / local.
- **Preparar:** Dois eventos novos, cap 5, preço 1000, gateway padrão, web concorrente.
- **Executar:** Disparar 30 POSTs com final 0001 por evento usando barreira; verificar payloads, cinco IDs/códigos únicos, disponibilidade e confirmações até 10s.
- **Oráculo:** Por rodada 5×202, 25×409 sold_out, nenhum outro status; cinco confirmed e 0 vagas.
- **Evidência mínima:** Runner HTTP com barreira, 30 conexões, validar corpo e IDs únicos, consultar cada aceito e availableSeats=0; usar novo evento por rodada. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F06-A24 · T-F06-03 · R07, API.

## TEST-A25 | A25

- **Nível / fase:** integration / local.
- **Preparar:** Ingresso de outro evento, código inexistente, pending, declined, confirmed livre/usado, cancelado.
- **Executar:** Executar tabela de decisão e 10 POSTs concorrentes para código livre; em cancelado testar POST com inválido e próprio.
- **Oráculo:** Mensagens R10 em ordem; exatamente uma entrada liberada; nenhum efeito nos demais; timestamp original preservado.
- **Evidência mínima:** Fixtures código inválido/outro evento, cancelado, pending/declined/refunded, confirmado já usado e novo; corrida com duas sessões do dono. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F07-A25 · T-F07-01 · R10.

## TEST-A26 | A26

- **Nível / fase:** integration / local.
- **Preparar:** Evento publicado, ticket confirmado e slow pending + declined; relógio real.
- **Executar:** Cancelar antes de 30s; consultar estados em até 10s, novamente após 45s; forjar edição/republicação; tentar cancelar draft e repetir cancelamento.
- **Oráculo:** Evento terminal; confirmed refunded, pending cancelled, declined intacto; nenhum ingresso reativado; ações inválidas negadas.
- **Evidência mínima:** Criar slow 0003 + fast 0001, cancelar antes de 30s; medir <=10s, aguardar >=45s, repetir cancelamento e testar ações; corrida cancelamento/reserva/finalização. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F07-A26 · T-F07-02 · R11.

## TEST-A27 | A27

- **Nível / fase:** integration / local.
- **Preparar:** Ingressos mistos de dois canais com preço 10000,10000,15000 confirmados e um declined; um já utilizado.
- **Executar:** Abrir painel, comparar ao oráculo; cancelar; recarregar.
- **Oráculo:** Antes 3/0/1/0/35000/0 (cap 3), depois 0/0/0/0/0/3; soma por preço congelado.
- **Evidência mínima:** Fixture 10000+10000+15000 confirmados, 1 check-in, recusado e estornado; conferir receita 35000 e todas as contagens; após cancelar comparar zeros e estornos. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F07-A27 · T-F07-03 · R05, R12.

## TEST-A28 | A28

- **Nível / fase:** integration / local.
- **Preparar:** A, B, P, anônimo; E de A com ticket.
- **Executar:** Acessar URL e enviar check-in/cancelamento em cada sessão; conferir HTML e banco.
- **Oráculo:** A tem gestão completa; B, P, anônimo não leem nem alteram; resposta sem dados de A.
- **Evidência mínima:** Browser A/B/P/visitante, POST forjado de B, verificar nenhum dado nem alteração; abrir gestão de A e executar ações. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F07-A28 · T-F07-03 · R04, R13.

## TEST-A29 | A29

- **Nível / fase:** integration / local.
- **Preparar:** Demo sentinela em projeto/volume próprio; gate em outro projeto.
- **Executar:** Rodar gate positivo e com falha de setup; interromper execução; conferir ps e listener, estado demo.
- **Oráculo:** Cleanup isolado; nenhum volume demo removido; falha/cleanup não zero; demo responde.
- **Evidência mínima:** Criar ambiente sentinela, induzir falha em gate isolado, verificar código e containers/volume do sentinela. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F01-A29 · T-F01-04 · H01, H03.

## TEST-A30 | A30

- **Nível / fase:** integration / local.
- **Preparar:** Sessão anônima, formulários públicos e protegidos.
- **Executar:** Enviar role=organizer, token CSRF ausente, next=//host e variações, reutilizar cookie após logout.
- **Oráculo:** Conta participante, mutação proibida sem CSRF, apenas redirect interno, sessão anterior inválida.
- **Evidência mínima:** POST forjado, role=organizer, cookies antes/depois, token ausente e next externo; comparar banco. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F02-A30 · T-F02-03 · R13.

## TEST-A31 | A31

- **Nível / fase:** integration / local.
- **Preparar:** Clock injetável e A dono de evento.
- **Executar:** Executar limites numéricos, data igual a now, inválida e futura; atrasar lock até data vencer; editar parcialmente inválido.
- **Oráculo:** Validação estrita dentro da escrita; sem alteração parcial; moeda decimal exata.
- **Evidência mínima:** Tabela de limites: ontem/agora/futuro, 0/1/1.5, 0/0.01/1.001, campos vazios, limite numérico. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F03-A31 · T-F03-02 · R01, R03.

## TEST-A32 | A32

- **Nível / fase:** integration / local.
- **Preparar:** Code generator injetável e DB transacional; evento com vagas.
- **Executar:** Forçar colisão uma vez e permanente; injetar falha ao criar job; verificar tickets/jobs antes/depois.
- **Oráculo:** Colisão transitória resolve com novo código; permanente/falha reverte tudo, não retorna sold_out.
- **Evidência mínima:** Forçar colisões e exceção entre INSERTs; contar tickets/jobs, inspecionar status HTTP em teste integrado. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F04-A32 · T-F04-02 · R06, R09.

## TEST-A33 | A33

- **Nível / fase:** integration / local.
- **Preparar:** Job vencido, dois workers independentes; lock de evento controlado.
- **Executar:** Ambos descobrem o mesmo ID; um rollback; outro conclui; repetir job terminal; testar evento diferente.
- **Oráculo:** Um efeito, sem deadlock; retry só de transação abortada; eventos independentes não bloqueiam entre si.
- **Evidência mínima:** Duas conexões/processos, job selecionado duas vezes, lock hold/release, abortar uma execução, confirmar efeito único. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F04-A33 · T-F04-03 · R07, R08, R11.

## TEST-A34 | A34

- **Nível / fase:** e2e / local.
- **Preparar:** Chave válida/errada, evento ausente e esgotado.
- **Executar:** Enviar JSON truncado, null, array, e-mail ruim, cartão Unicode e numérico, content-type incorreto, corpo com chave ausente.
- **Oráculo:** 401 antes de parse; 422 para payload inválido autenticado mesmo com evento inexistente/lotado; sem redirect/500.
- **Evidência mínima:** HTTP bruto com corpo malformado, chave ausente/errada/válida; conferir resposta exata e ausência de efeitos. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F06-A34 · T-F06-03 · API, R06, R07.

## TEST-A35 | A35

- **Nível / fase:** integration / local.
- **Preparar:** Dois estados válidos de evento/tickets em transações; consultas simultâneas.
- **Executar:** Usar barreira para alterar capacity e status durante leituras; comparar cada resultado a snapshots completos.
- **Oráculo:** Sem mistura de dados de commits distintos, sem clamp escondendo ocupação inválida; painel sempre deriva do mesmo snapshot.
- **Evidência mínima:** Forçar alternância de snapshots e comparar cada resultado a estados completos permitidos; verificar ausência de clamp de contagem negativa. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F07-A35 · T-F07-03 · R05, R11, R12.

## TEST-A36 | A36

- **Nível / fase:** integration / local.
- **Preparar:** Evento publicado cap 1 ou 2; conexões separadas; ticket pending/confirmed.
- **Executar:** Forçar as duas ordens de lock em cada par: reserva×cancelar, finalize×cancelar, checkin×cancelar.
- **Oráculo:** Somente resultados serializáveis; no final 0 pending/confirmed, nenhum check-in liberado se cancelar ganhou; sem deadlock/5xx.
- **Evidência mínima:** Barreiras e locks controlados em ambas as ordens; comparar sequência de commits e estado terminal. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F07-A36 · T-F07-04 · R07, R10, R11.

## TEST-A37 | A37

- **Nível / fase:** integration / local.
- **Preparar:** Baseline e fixture Git local sem credenciais.
- **Executar:** Executar verificador; alterar item, remover mapeamento, simular relatório faltante, editar relatório commitado.
- **Oráculo:** Falha estrutural ou de histórico detectada; baseline sem relatórios é válida, release incompleto falha.
- **Evidência mínima:** Executar verificador sobre fixture Git descartável e mutações negativas. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F01-A37 · T-F01-04 · H03.

## TEST-X01 | X01

- **Nível / fase:** integration / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** Subir ambiente limpo, login das três contas, comparar IDs após reseed.
- **Oráculo:** Após up com seed, A/B/P autenticam; duas execuções da seed não duplicam contas.
- **Evidência mínima:** Subir ambiente limpo, login das três contas, comparar IDs após reseed. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F02-X01 · T-F02-04 · H01, H02.

## TEST-X02 | X02

- **Nível / fase:** integration / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** DB limpo migrado; criar evento futuro e rejeitar ontem.
- **Oráculo:** Migração e clock da fundação permitem criação e rejeição de data vencida.
- **Evidência mínima:** DB limpo migrado; criar evento futuro e rejeitar ontem. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F03-X02 · T-F03-04 · H01, R01.

## TEST-X03 | X03

- **Nível / fase:** integration / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** Browser e POST direto B contra E1 de A; ausência de dados, estado intacto.
- **Oráculo:** URL de gestão e listagem usam dono da sessão; B não pode editar/publicar A.
- **Evidência mínima:** Browser e POST direto B contra E1 de A; ausência de dados, estado intacto. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F03-X03 · T-F03-04 · R04, R13.

## TEST-X04 | X04

- **Nível / fase:** integration / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** Comprar slow, reiniciar worker antes de due; obter status final uma vez.
- **Oráculo:** Worker do Compose consome job persistido após reinício sem chave real.
- **Evidência mínima:** Comprar slow, reiniciar worker antes de due; obter status final uma vez. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F04-X04 · T-F04-04 · H01, R08.

## TEST-X05 | X05

- **Nível / fase:** integration / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** Corrida compra × redução e compra × preço; conferir invariantes e snapshots.
- **Oráculo:** Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação.
- **Evidência mínima:** Corrida compra × redução e compra × preço; conferir invariantes e snapshots. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F04-X05 · T-F04-04 · R02, R03, R05, R07.

## TEST-X06 | X06

- **Nível / fase:** e2e / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** Dois browsers com sessões distintas; compra e acesso cruzado.
- **Oráculo:** Sessão define dono do ingresso; anônimo e outra conta não veem compra pessoal.
- **Evidência mínima:** Dois browsers com sessões distintas; compra e acesso cruzado. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F05-X06 · T-F05-04 · R09, R13.

## TEST-X07 | X07

- **Nível / fase:** e2e / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** Criar draft, publicar, reservar até lotar, cancelar fixture; recarregar catálogo.
- **Oráculo:** A publicação e as vagas calculadas por F03 chegam à vitrine; draft/cancelled não são exibidos, inclusive fixture cancelada. A ação real de cancelar é validada em X14.
- **Evidência mínima:** Criar draft, publicar, reservar até lotar, cancelar fixture; recarregar catálogo. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F05-X07 · T-F05-04 · R02, R05.

## TEST-X08 | X08

- **Nível / fase:** e2e / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** Comprar 0004, observar lotação, após 45s ver declined e vaga.
- **Oráculo:** Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine.
- **Evidência mínima:** Comprar 0004, observar lotação, após 45s ver declined e vaga. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F05-X08 · T-F05-04 · R06, R08, R09.

## TEST-X09 | X09

- **Nível / fase:** e2e / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** GET antes/depois publicação, edição e cancelamento fixture.
- **Oráculo:** A listagem de parceiros reflete publicação, preço e capacidade de F03; fixtures draft/cancelled ficam fora. Cancelamento real será validado em X15.
- **Evidência mínima:** GET antes/depois publicação, edição e cancelamento fixture. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F06-X09 · T-F06-04 · R02, R03, R05, API.

## TEST-X10 | X10

- **Nível / fase:** e2e / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** POST simultâneo e GET ticket, comparar dados de ledger.
- **Oráculo:** API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture.
- **Evidência mínima:** POST simultâneo e GET ticket, comparar dados de ledger. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F06-X10 · T-F06-04 · R06, R07, R09, API.

## TEST-X16 | X16

- **Nível / fase:** e2e / integrated.
- **Preparar:** Checkout integrado contendo ambas as features; realizar ações reais via UI/API, sem editar DB.
- **Executar:** Corrida web e API com capacidade 1; um sucesso, outro esgotado; testar isolamento pelo e-mail.
- **Oráculo:** Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web.
- **Evidência mínima:** Corrida web e API com capacidade 1; um sucesso, outro esgotado; testar isolamento pelo e-mail. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F06-X16 · T-W6-02 · R05, R07, R09, API.

## TEST-X11 | X11

- **Nível / fase:** e2e / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** B tenta check-in e cancelamento de A, sem efeito e sem informação.
- **Oráculo:** Todas as ações operacionais respeitam guarda de dono.
- **Evidência mínima:** B tenta check-in e cancelamento de A, sem efeito e sem informação. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F07-X11 · T-F07-04 · R13.

## TEST-X12 | X12

- **Nível / fase:** e2e / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** Cancelar publicado e tentar editar e republicar via POST; consultar catálogo.
- **Oráculo:** Cancelamento bloqueia publicação/edição e integra gestão em URL existente.
- **Evidência mínima:** Cancelar publicado e tentar editar e republicar via POST; consultar catálogo. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F07-X12 · T-F07-04 · R04, R11.

## TEST-X13 | X13

- **Nível / fase:** integration / local.
- **Preparar:** Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.
- **Executar:** Combinar slow, fast, check-in, cancelar e esperar resultado tardio.
- **Oráculo:** Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive.
- **Evidência mínima:** Combinar slow, fast, check-in, cancelar e esperar resultado tardio. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F07-X13 · T-F07-04 · R10, R11, R12.

## TEST-X14 | X14

- **Nível / fase:** e2e / integrated.
- **Preparar:** Checkout integrado contendo ambas as features; realizar ações reais via UI/API, sem editar DB.
- **Executar:** Fluxo browser: comprar, confirmar, validar código, cancelar, recarregar ambos.
- **Oráculo:** Com UI e operações integradas, uma compra web confirmada incrementa painel, permite check-in e, após cancelamento, some do catálogo e vira estornada em Meus ingressos.
- **Evidência mínima:** Fluxo browser: comprar, confirmar, validar código, cancelar, recarregar ambos. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F07-X14 · T-W6-02 · R06, R09, R10, R11, R12.

## TEST-X15 | X15

- **Nível / fase:** e2e / integrated.
- **Preparar:** Checkout integrado contendo ambas as features; realizar ações reais via UI/API, sem editar DB.
- **Executar:** HTTP+browser: compra, consultar checkedIn, cancelar, verificar 404 e estorno.
- **Oráculo:** Com API e operações integradas, ingresso de parceiro conta na lotação e painel, permite check-in e consulta checkedIn; cancelar remove evento da lista, bloqueia POST, estorna e conserva consulta do ticket.
- **Evidência mínima:** HTTP+browser: compra, consultar checkedIn, cancelar, verificar 404 e estorno. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-F07-X15 · T-W6-02 · R05, R07, R10, R11, R12, API.

## TEST-P01 | P01

- **Nível / fase:** process / release.
- **Preparar:** main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.
- **Executar:** Executar validate_docs e revisar DAG, regras, escopo e cada critério.
- **Oráculo:** PRD >=5 features, fornece/consome, DAG e waves; todas R01–R13 citadas, cada aresta coberta.
- **Evidência mínima:** Inspeção dos artefatos e do histórico Git; registrar evidência verificável. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-RELEASE-P01 · T-W6-03 · SDD.

## TEST-P02 | P02

- **Nível / fase:** process / release.
- **Preparar:** main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.
- **Executar:** Inspecionar todos os FDD, planos, contratos e mapeamentos; validar existência dos testes.
- **Oráculo:** Spec, plano e contrato por feature, todos os critérios e cross-feature mapeados.
- **Evidência mínima:** Inspeção dos artefatos e do histórico Git; registrar evidência verificável. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-RELEASE-P02 · T-W6-03 · SDD.

## TEST-P03 | P03

- **Nível / fase:** process / release.
- **Preparar:** main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.
- **Executar:** Rodar validate_evidence --release e conferir evidência original, SHA, sessão, modelo e imutabilidade.
- **Oráculo:** Para cada feature há relatório novo e imutável, com data UTC, SHA completo, ferramenta, modelo, identidade de sessão e evidência por item; último relatório integrado aprova tudo aplicável.
- **Evidência mínima:** Inspeção dos artefatos e do histórico Git; registrar evidência verificável. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-RELEASE-P03 · T-W6-03 · EVAL.

## TEST-P04 | P04

- **Nível / fase:** process / release.
- **Preparar:** main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.
- **Executar:** Cruzar state, relatórios mais recentes, SHAs e PRs; confirmar todos os status.
- **Oráculo:** Estado final aponta ao último relatório aprovado, commit implementado e PR de cada feature; nenhum concluído sem integração verificada.
- **Evidência mínima:** Inspeção dos artefatos e do histórico Git; registrar evidência verificável. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-RELEASE-P04 · T-W6-03 · STATE.

## TEST-P05 | P05

- **Nível / fase:** process / release.
- **Preparar:** main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.
- **Executar:** Abrir PRs da wave, conferir merge e lista de commits; testar sobreposição estrita para cada par.
- **Oráculo:** Pelo menos uma wave paralela via PRs mergeados; primeiro commit de cada PR anterior ao último de todos os demais.
- **Evidência mínima:** Inspeção dos artefatos e do histórico Git; registrar evidência verificável. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-RELEASE-P05 · T-W6-03 · PAR.

## TEST-P06 | P06

- **Nível / fase:** process / release.
- **Preparar:** main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.
- **Executar:** Clonar main em pasta vazia, rodar os 18 passos, conferir README e repo público.
- **Oráculo:** Repo público único, main com README completo; fluxo externo 1–18 aprovado em clone limpo.
- **Evidência mínima:** Inspeção dos artefatos e do histórico Git; registrar evidência verificável. Salvar comando, resultado, SHA e identificadores sintéticos; falha ou ausência de evidência bloqueia aprovação.
- **Vínculos:** C-RELEASE-P06 · T-W6-03 · DELIVERY.
