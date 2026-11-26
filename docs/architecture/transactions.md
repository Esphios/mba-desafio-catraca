# Protocolo transacional e prova de invariantes

## Premissas

PostgreSQL 17, isolamento READ COMMITTED, todas as escritas do domínio via serviços. Bloqueio de linha por evento, não mutex em memória. Todas as mutações de lotação, preço, estado de evento, ticket e check-in passam pela mesma convenção. A aplicação usa papel sem permissão de alterações manuais fora do serviço em operação normal. A constraint de capacidade mínima não substitui a invariante agregada.

## Reserva (R03, R05–R09)

Pseudocódigo, a implementar em F04; operações SQL são conceituais.

```text
validate email/card/buyer BEFORE transaction
outcome, delay = classify(card suffix)  # 3s or 35s in default
BEGIN READ COMMITTED
  event = SELECT event WHERE id=? FOR UPDATE
  if missing or state != published: rollback EventNotAvailable
  occupied = SELECT COUNT(*) FROM ticket
             WHERE event_id=? AND status IN ('pending','confirmed')
  if occupied >= event.capacity: rollback SoldOut
  create ticket with event.price_cents, pending, unique code
  create payment_job in same transaction, due_at = clock.now() + delay
COMMIT
return immutable snapshot of just-created pending ticket
```

Não calcular count antes de adquirir lock nem numa query que combine o lock com snapshot antigo; aguardar commit anterior e executar count em outra instrução. Não liberar lock antes do INSERT. Retornar snapshot pending, não refazer query que possa refletir status após resposta. Falha ao inserir job desfaz ticket. Colisão de código: savepoint por tentativa, retry apenas da constraint de código, não de quaisquer integrity errors. Limitar retry; falha não vende. Qualquer outra tentativa de compra é uma compra nova (idempotência de POST não definida no brief; não retry automático do cliente em erro incerto).

## Edição e publicação (F03)

Dentro de atomic, carregar linha com lock; validar ator e estado atual; reavaliar data com clock; consultar ocupação e verificar capacity nova >= occupied; aplicar preço/capacity. Se comprar primeiro, redução observa nova ocupação; se editar primeiro, reserva observa nova capacity e preço. Publicar usa lock e estado draft. Não revalidar data passada em leitura pública; o brief só exige validação ao criar/editar.

## Worker de pagamento (F04)

Processo contínuo busca até 50 IDs queued com due_at <= now, por ordem due_at/ticket_id, consulta sem row lock. Para cada ID: obter event_id imutável pelo ticket sem lock; abrir atomic; lock do evento; reconsultar ticket/job, eventualmente lock por ordem event→ticket→job; checar job queued e vencido. Se ticket pending e event published, atualizar para confirmed/declined conforme outcome e status_changed_at. Caso contrário, job ignored; não mudar ticket terminal. Gravar done/ignored e completed_at na mesma transação. Dois workers podem selecionar o mesmo ID; segundo revalida job e não repete efeito. Não usar SKIP LOCKED no job antes do evento, pois inverte ordem. Sem espera ativa dentro de transação: polling de ~100 ms em idle, backoff curto em erro, log e retry do job. Não manter PAN; só resultado e data de vencimento.

| Final | Outcome | Delay padrão escolhido | Faixa exigida |
|---|---|---:|---|
| 0001 | approved | 3 s | 2–5 s |
| 0002 | declined | 3 s | 2–5 s |
| 0003 | approved | 35 s | 30–40 s |
| 0004 | declined | 35 s | 30–40 s |
| outros | declined | 3 s | 2–5 s |

Atraso contado a partir da criação; teste mede também latência observável da requisição. Configuração acelerada só em gates unitários/integração específicos, nunca no compose padrão/fluxo final. Teste de restart com job pendente e atraso real. Se worker cair depois de commit, job já done; se antes, permanece queued e é recuperável.

## Cancelamento (F07)

BEGIN; lock event; checar ator e published; atualizar evento cancelled e timestamp; UPDATE tickets confirmed→refunded; UPDATE tickets pending→cancelled; atualizar timestamps; manter declined e checked_in_at; commit. Jobs podem ficar queued para futura resposta ignorada (ou finalizar ignored na mesma ordem, escolha baseline: preservar queued até vencimento para exercitar a resposta tardia). A operação é imediata no commit, abaixo do limite de 10s a provar. Se gateway vence antes, confirmado é estornado; se cancelamento vence antes, pendente é cancelado e finalize não revive; se compra vence antes, é incluída; se depois, vê cancelled e falha. Check-in usa mesmo lock e não libera entrada após cancelamento. Nenhuma ação faz gateway dentro de lock.

## Prova de R07

Base: criação de evento tem zero tickets e capacity >=1. Hipótese: antes de cada transação serializada, 0 <= occupied <= capacity. Reserva só insere se occupied < capacity; incrementa exatamente 1. Aprovação troca pending por confirmed sem alterar ocupação; recusa reduz 1. Cancelamento reduz ocupação a zero e bloqueia novas reservas; edição só diminui capacity até occupied; check-in não altera ocupação. Rollback não altera estado. Com a ordem comum de lock por evento e snapshots novos após adquirir o lock, cada operação preserva a hipótese. Por indução, a invariante vale para todos os commits dessas operações. Limite da prova: escrita direta que não usa o protocolo viola a premissa; impedir caminhos alternativos e revisar código. A prova não substitui execução real.

## Consultas

Catálogo/painel devem agregar em uma única instrução SQL por leitura (LEFT JOIN com filtros ou subquery correlacionada), evitando combinar estado e ocupação de snapshots distintos. Lista pode ficar velha entre GET e POST, normal em HTTP; a compra revalida e retorna esgotado sem erro 500. Painel não usa preço atual para somar ticket. Sem N+1. Não armazenar métricas derivadas.

## Matriz de corridas

| A × B | Resultado permitido | Resultado proibido |
|---|---|---|
| 30 reservas × cap 5 | 5 aceitas, 25 esgotadas | 6+ aceitas ou 500 |
| reserva × diminuir capacidade | uma ordem serializável; capacidade >= ocupação | redução abaixo de ocupação |
| reserva × novo preço | ticket com preço de uma ordem consistente | preço sobrescrito depois |
| reserva × cancelar | venda antes vira cancelled/refunded ou compra 404 | ticket pending após cancelamento |
| finalize × cancelar | refunded se aprovação primeiro; cancelled se cancelamento primeiro | confirmed depois de cancelamento |
| check-in × check-in | uma entrada e uma já utilizada | duas entradas |
| check-in × cancelar | entrada antes ou cancelado; painel final 0 | entrada depois do cancelamento |
| worker × worker | um efeito terminal | dupla alteração |

Testar com conexões PostgreSQL distintas e barreira; medir timestamps de commit e distinguir resultados concorrentes válidos. Usar TransactionTestCase ou processo externo, nunca TestCase encapsulado como única evidência do lock. Repetir com eventos novos, ao menos duas rajadas HTTP e dez rodadas de stress do core.
