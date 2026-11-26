# Engineering Guidelines | Python/Django

## Organização e dependências

Estrutura planejada: `config/` configurações e raiz de URLs, `catraca_platform/` modelos e clock, `identity/`, `catalog/`, `ledger/`, `storefront/`, `partner/`, `operations/`, `templates/`, `tests/`, `bin/`, `docs/`, `state/`. Módulos de domínio não importam requests/views. Views adaptam HTTP e chamam casos de uso; templates não calculam vaga ou receita. Config fica em um único ponto; usar env somente no limite. Migrations iniciais F01. Sem import cíclico. Nomes internos em inglês snake_case, interface em português e DTO externo camelCase fixo. Uma responsabilidade por serviço; funções tipadas, dataclasses frozen para DTOs, enums TextChoices nos modelos. Não replicar constantes entre módulos.

## Convenções e qualidade

Python 3.12; usar annotations, `Decimal` em parsing financeiro, `int` cents, `datetime` aware, timezone UTC; renderizar data/hora em America/Sao_Paulo. Ruff format/check; código novo sem lint warnings. Fixar dependências em arquivo reproduzível com hashes/versões (incluindo transitivas); mudanças de dependência justifique, revise licença e segurança; não atualizar globalmente sem motivo. Não introduzir metaprogramação ou abstrações genéricas para duas chamadas simples. Docstrings para API pública e invariantes, comentários explicam porquê e não cada linha. Sem catch amplo que mascara exceção; worker pode capturar erro por job, registrar e continuar com backoff, não marcar done sem commit. Nunca transformar falha inesperada em sold_out; somente regra real retorna 409. Views não retornam stack trace.

## Persistência e concorrência

Ver protocolo transacional. `transaction.atomic()` explícito no serviço, não envolver todo request com ATOMIC_REQUESTS; acquire `select_for_update()` em queryset avaliado dentro da transação, sem lazy evaluation pós-commit. Nunca usar `select_related` que bloqueie tabelas desnecessárias; lock somente evento. Count separado. Ordenar locks quando múltiplos recursos. Não aguardar gateway no HTTP. Retries limitados e específicos para colisão de código/deadlock se necessário, nunca duplicar transação cujo commit é incerto. SQL bruto somente se ORM insuficiente e parâmetros bindados. Sem criação de ticket fora de reserve (exceto fixtures declaradas). Reusar status e dinheiro canônicos; migração idempotente por mecanismo Django, sem alterações destrutivas em dados reais.

## Web, API e segurança

Métodos GET não mutam domínio. POST web com CSRF; use PRG quando apropriado. Validação backend independente do HTML. Mensagens R07/R10 exatas; status em português. API responde JSON e status fixo, chave antes de parser, sem redirect ou trailing slash imposto. Não serializar modelos inteiros. Cookies HttpOnly, SameSite, sessões server-side; hash de senha e guards framework. Owner conferido em todos os endpoints. Testar acesso negativo, injection/escaping, invalid payload e CSRF; chave não aparece em logs. Não usar dados reais em testes, nem copiar credenciais para relatórios fora de demo.

## Testes

Unitários determinísticos e rápidos para validação, moeda, classificação, estados; integração contra PostgreSQL de teste para FKs e transações; TransactionTestCase com conexões independentes para lock; HTTP real para contrato/paralelismo; browser real para fluxo e autorização. Testes parametrizados sem ordem implícita, fixtures novas, não depender de sleep fixo quando polling com deadline basta. Teste de timing no modo real sem configuração acelerada. Falha deve indicar esperado/observado, sem segredo. Testar a mesma regra nos dois canais e na integração. Meta proposta: cobertura de branches nos módulos de domínio >=85% (não substitui casos obrigatórios; se ferramenta não disponível, registrar decisão e não alegar cobertura). Sem mocks do banco para prova R07. Para teste de falha de gates, introduzir falha em cópia temporária e garantir limpeza.

## Logs e operação

Evento logado: operation, event_id/ticket_id, outcome, elapsed_ms e correlation_id opcional. Não logar request.body, cartão, senha, sessão ou chave. Worker heartbeat e erro de job sem PII, não criar dashboards externos. Readiness com DB e worker, liveness simples. Investigar via `docker compose logs`, sem executar comandos destrutivos na main ou banco da demo sem confirmação. Consultas de verificação em DB test somente.

## Git e revisão

Commits pequenos e descritivos `feat(F04): reserve ticket under event lock`; `test(F04): prove capacity under concurrent requests`; `docs(F04): add evaluation report`. Não fabricar histórico para paralelismo. PR informa feature, critérios, comandos, SHA e evidência, mudanças de interface, regressões e riscos. Coordenador verifica base e ownership, revisa diffs, merges serialmente. Relatório novo em cada avaliação, não alterar nem squash junto com mudanças posteriores que ocultem proveniência; PR GitHub preserva commits da wave mesmo se squash no merge. Preferir merge commit para relatórios/histórico auditável. Estado atualizado pelo coordenador depois da evidência. Se docs divergem de código, não corrigir silenciosamente: amendment aprovado, rastreabilidade revisada.

## Documentation as context

PRD responde o que/porquê; design HLD o como; FDD por feature; ADR preserva decisão; guidelines são onboarding; diagramas são derivados da arquitetura; plano e contrato operacionalizam; relatório é evidência histórica, não documentação viva editável. Novo agente começa lendo só o necessário e registra lacunas. Após implementação, auditoria de codebase compara HLD/FDD/ADRs com código real e corrige documentação viva sem apagar decisões anteriores. Evitar duplicação: link para fonte canônica. Não gerar LLD de classes especulativas nem documentação de produção inexistente.
