# Pesquisa técnica | duas fases

## Fase 1: exploração

Pergunta: como impedir oversell e resposta tardia sem exigir infraestrutura adicional ao avaliador? Opções: mutex do processo (não cobre réplicas); isolamento serializable com retry (válido, mas exige tratar abortos e repetição); contador reservado com UPDATE condicional (rápido, mas exige manter agregado sincronizado); lock da linha de evento + count de tickets em READ COMMITTED (escolhido, simples para MVP). Para gateway, sleep no HTTP viola R06; tarefa somente em memória se perde no restart; broker externo com outbox é válido, mas desnecessário; job PostgreSQL transacional resolve a atomicidade da reserva e do agendamento.

## Fase 2: fundamentação e aplicação

- PostgreSQL 17, [Explicit Locking](https://www.postgresql.org/docs/17/explicit-locking.html): row locks bloqueiam escritores/locks conflitantes até fim da transação; ordem consistente reduz deadlock. Implicação: todos os serviços seguem event→ticket→job.
- PostgreSQL 17, [Data Consistency Checks at the Application Level](https://www.postgresql.org/docs/17/applevel-consistency.html) e [SET TRANSACTION](https://www.postgresql.org/docs/17/sql-set-transaction.html): READ COMMITTED adquire snapshot por comando; lock antes da consulta agregada. Implicação: nova contagem após lock, não antes.
- PostgreSQL 17, [Transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html): alterações agrupadas são visíveis em conjunto no commit. Implicação: ticket e job/cancelamento não podem ser parcialmente confirmados.
- Django 5.2, [Release notes](https://docs.djangoproject.com/en/5.2/releases/5.2/): compatibilidade com PostgreSQL 14+. [Testing tools](https://docs.djangoproject.com/en/5.2/topics/testing/tools/): TestCase encapsula transações; para observar commit e lock de verdade, usar TransactionTestCase. Implicação: gate usa PostgreSQL, conexões independentes.
- Django 5.2, [Instalação](https://docs.djangoproject.com/en/5.2/topics/install/): driver PostgreSQL necessário; instalar runtime em containers.

Fontes oficiais consultadas em 26/11/2026. Não houve benchmark nem teste de infraestrutura nesta fase. Hipóteses a medir: 32 threads HTTP suportam rajada sem 5xx; worker conclui em 5 s/40 s; consultas agregadas retornam em tempo adequado. Se falhar, coletar plano de execução, locks e latência antes de alterar design. ADRs registram escolhas; relatório de validação registra resultados reais.
