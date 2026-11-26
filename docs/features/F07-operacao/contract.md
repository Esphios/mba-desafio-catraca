# F07 | Contrato de avaliação

Versão 0.1 proposta. Avaliar SHA exato em checkout limpo, Docker/Compose v2, Git, porta/projeto isolados; usar PostgreSQL real. Instalar nada no host além dos pré-requisitos do brief. Rodar `./bin/up`, `./bin/gates F07` quando implementados e executar verificações específicas abaixo. Se comando não existir ou efeito não puder ser reproduzido, FAIL/ BLOCKED, nunca PASS. Em F01, gates inicial não pressupõe features futuras. Fixtures de estados futuros são permitidas para dependências ainda não implementadas, somente em DB de teste e indicadas no relatório. Não substituir provas HTTP/UI finais por fixtures.

## Itens obrigatórios locais

| Item | Critério | Procedimento e evidência | Resultado esperado |
|---|---|---|---|
| C-F07-A25 | A25 (R10) | Fixtures código inválido/outro evento, cancelado, pending/declined/refunded, confirmado já usado e novo; corrida com duas sessões do dono. | Check-in aplica exatamente as cinco mensagens na ordem definida; só confirmed não utilizado recebe checkedIn=true; dois check-ins concorrentes liberam uma entrada. |
| C-F07-A26 | A26 (R11) | Criar slow 0003 + fast 0001, cancelar antes de 30s; medir <=10s, aguardar >=45s, repetir cancelamento e testar ações; corrida cancelamento/reserva/finalização. | Cancelar publicado é irreversível; na mesma transação confirmed→refunded e pending→cancelled, sem alteração de declined; gateway posterior não modifica; edit/publish/compra rejeitados. |
| C-F07-A27 | A27 (R05,R12) | Fixture 10000+10000+15000 confirmados, 1 check-in, recusado e estornado; conferir receita 35000 e todas as contagens; após cancelar comparar zeros e estornos. | Painel mostra seis métricas com snapshots de preço e ambos os canais; check-ins somente confirmed; cancelado tem receita/vagas/confirmados/pendentes/check-ins zero. |
| C-F07-A28 | A28 (R04,R13) | Browser A/B/P/visitante, POST forjado de B, verificar nenhum dado nem alteração; abrir gestão de A e executar ações. | Check-in, cancelar e painel ficam na URL de gestão de cada evento; todas as ações exigem dono inclusive requisição direta. |

## Cross-feature (dependências anteriores)

| Item | Critério | Procedimento e evidência | Esperado |
|---|---|---|---|
| C-F07-X11 | X11 (F02→F07) | B tenta check-in e cancelamento de A, sem efeito e sem informação. | Todas as ações operacionais respeitam guarda de dono. |
| C-F07-X12 | X12 (F03→F07) | Cancelar publicado e tentar editar e republicar via POST; consultar catálogo. | Cancelamento bloqueia publicação/edição e integra gestão em URL existente. |
| C-F07-X13 | X13 (F04→F07) | Combinar slow, fast, check-in, cancelar e esperar resultado tardio. | Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive. |

## Itens de integração pós-wave (W6)

Não bloquear aprovação isolada com itens ainda indisponíveis; estes são obrigatórios no gate de release integrado e avaliados novamente por sessão independente depois dos merges. Não registrar PASS antecipado.

| Item | Critério | Procedimento | Esperado |
|---|---|---|---|
| C-F07-X14 | X14 (F05→F07) | Fluxo browser: comprar, confirmar, validar código, cancelar, recarregar ambos. | Integração final (não dependência de implementação): compra web aparece no painel e permite check-in; cancelamento aparece em Meus ingressos. |
| C-F07-X15 | X15 (F06→F07) | HTTP+browser: compra, consultar checkedIn, cancelar, verificar 404 e estorno. | Integração final: compra partner soma painel, é validada no check-in e deixa API após cancelamento. |

## Veredito

PASS somente se todo item aplicável tem evidência real e satisfaz o resultado esperado. FAIL se divergente; BLOCKED se não reproduzível. Para itens W6, relatório isolado identifica explicitamente `not_applicable_until_integration`; o relatório mais recente após W6 cobre também esses itens. Guardar relatório em `reports/<UTC>-<shortSHA>.md` (novo arquivo; não alterar). Registrar data UTC, SHA completo, ferramenta/modelo, sessão independente, comandos, saída, artefatos, veredito individual e resumo. Usar template em docs/agents.
