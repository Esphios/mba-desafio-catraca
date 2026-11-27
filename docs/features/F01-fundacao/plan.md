# F01 | Plano de implementação

Entrada: baseline W0 aprovada, dependências nenhuma integradas e aprovadas, branch exclusiva. Skills: harness-engineering, schema-review, feature-implementation.

## T-F01-01

**Entrega:** Materializar os pins aprovados na W0 em runtime, Dockerfile, Compose, lockfile, estrutura de comandos e lint; implementar health inicial.

**Validação:** lint, checks do framework e testes já implementados; fase 1 não exige endpoints futuros.
- `TEST-A03` (A03): Rodar gates íntegro; repetir com asserção false e depois restaurar; verificar código de saída e cleanup. Resultado: Suíte íntegra exit 0; versão quebrada exit diferente de 0; relatório lista testes realmente executados.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F01-02

**Entrega:** Criar user custom e models/schema, constraints, índices e migrations; rodar testes de integridade.

**Validação:** lint, checks do framework e testes já implementados; fase 2 não exige endpoints futuros.
- `TEST-A05` (A05): Forçar duplicata de código, FK inexistente, status inválido, preço 0, capacidade 0, buyer misto, dois jobs por ticket; migrar de novo. Resultado: Todas as escritas inválidas falham; dados válidos persistem; sem migração pendente.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F01-03

**Entrega:** Implementar bootstrap, seed e scripts de subida/descida/gates; validar clone limpo.

**Validação:** lint, checks do framework e testes já implementados; fase 3 não exige endpoints futuros.
- `TEST-A01` (A01): Executar bash bin/up; GET readiness pelo host; inspect serviços; autenticar seed quando F02 disponível. Resultado: Exit 0; DB, web e worker prontos; migração/seed one-shot concluídas; nenhuma chave real; antes de F02 comprovar linhas e hashes da seed.
- `TEST-A02` (A02): Executar down; verificar ausência de containers e listener; subir novamente; seed outra vez; comparar IDs e quantidade. Resultado: Nenhum serviço do projeto ativo; dados persistem e seed permanece com 2 organizadores + 1 participante seed, sem duplicação.
- `TEST-A04` (A04): Seguir comandos e verificar nomes, porta, chave local, mapa e defaults. Resultado: Comandos reproduzíveis; sem setup manual; links internos existentes; endereços corretos.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F01-04

**Entrega:** Verificar fail-closed do harness, isolamento e documentação; fornecer interface e avaliação.

**Validação:** lint, checks do framework e testes já implementados; fase 4 não exige endpoints futuros.
- `TEST-A01` (A01): Executar bash bin/up; GET readiness pelo host; inspect serviços; autenticar seed quando F02 disponível. Resultado: Exit 0; DB, web e worker prontos; migração/seed one-shot concluídas; nenhuma chave real; antes de F02 comprovar linhas e hashes da seed.
- `TEST-A02` (A02): Executar down; verificar ausência de containers e listener; subir novamente; seed outra vez; comparar IDs e quantidade. Resultado: Nenhum serviço do projeto ativo; dados persistem e seed permanece com 2 organizadores + 1 participante seed, sem duplicação.
- `TEST-A03` (A03): Rodar gates íntegro; repetir com asserção false e depois restaurar; verificar código de saída e cleanup. Resultado: Suíte íntegra exit 0; versão quebrada exit diferente de 0; relatório lista testes realmente executados.
- `TEST-A04` (A04): Seguir comandos e verificar nomes, porta, chave local, mapa e defaults. Resultado: Comandos reproduzíveis; sem setup manual; links internos existentes; endereços corretos.
- `TEST-A05` (A05): Forçar duplicata de código, FK inexistente, status inválido, preço 0, capacidade 0, buyer misto, dois jobs por ticket; migrar de novo. Resultado: Todas as escritas inválidas falham; dados válidos persistem; sem migração pendente.
- `TEST-A29` (A29): Rodar gate positivo e com falha de setup; interromper execução; conferir ps e listener, estado demo. Resultado: Cleanup isolado; nenhum volume demo removido; falha/cleanup não zero; demo responde.
- `TEST-A37` (A37): Executar verificador; alterar item, remover mapeamento, simular relatório faltante, editar relatório commitado. Resultado: Falha estrutural ou de histórico detectada; baseline sem relatórios é válida, release incompleto falha.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## Integração posterior
Não há item exclusivo de integração atribuído a esta feature; regressão global é obrigatória.

## Handoff
Entregar SHA limpo, base SHA, interfaces, comandos, logs redigidos e desvios. Avaliador novo, sem histórico de conversa, julga apenas contrato e evidência. Coordenador integra após local PASS; relatório final da feature exige também itens integrados, se houver.
