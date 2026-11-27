# F01 | Contrato de avaliação

Versão 2 proposta. Ambiente: checkout limpo do SHA, Docker/Compose e Git; `bash bin/up` e `bash bin/gates --feature F01` após implementados. Banco PostgreSQL real, dados sintéticos, projeto/porta exclusivos, gateway padrão para itens de tempo. O avaliador cria relatório novo sem alterar código.

## Fase LOCAL (antes do merge)

### C-F01-A01 (A01)

Preparação: Clone de SHA limpo; Docker/Compose; sem .env; sem imagem local obrigatória.

Procedimento: Executar bash bin/up; GET readiness pelo host; inspect serviços; autenticar seed quando F02 disponível.

PASS somente se: Exit 0; DB, web e worker prontos; migração/seed one-shot concluídas; nenhuma chave real; antes de F02 comprovar linhas e hashes da seed.

Teste: `TEST-A01`. Evidência: Clonar SHA em pasta temporária; executar up; verificar HTTP e compose ps.

### C-F01-A02 (A02)

Preparação: Stack da demo com usuário e evento sentinela.

Procedimento: Executar down; verificar ausência de containers e listener; subir novamente; seed outra vez; comparar IDs e quantidade.

PASS somente se: Nenhum serviço do projeto ativo; dados persistem e seed permanece com 2 organizadores + 1 participante seed, sem duplicação.

Teste: `TEST-A02`. Evidência: Executar up, seed duas vezes, down, provar porta fechada e ps vazio, up novamente; comparar IDs e autenticação após F02.

### C-F01-A03 (A03)

Preparação: Ambiente de teste exclusivo e teste propositalmente falho em cópia.

Procedimento: Rodar gates íntegro; repetir com asserção false e depois restaurar; verificar código de saída e cleanup.

PASS somente se: Suíte íntegra exit 0; versão quebrada exit diferente de 0; relatório lista testes realmente executados.

Teste: `TEST-A03`. Evidência: Executar gates e injetar falha em cópia descartável; capturar códigos de saída.

### C-F01-A04 (A04)

Preparação: README e AGENTS no candidato.

Procedimento: Seguir comandos e verificar nomes, porta, chave local, mapa e defaults.

PASS somente se: Comandos reproduzíveis; sem setup manual; links internos existentes; endereços corretos.

Teste: `TEST-A04`. Evidência: Inspeção dos arquivos, ambiente sem .env e sem credenciais externas.

### C-F01-A05 (A05)

Preparação: Banco PostgreSQL migrado em volume vazio.

Procedimento: Forçar código duplicado, curto, longo, minúsculo ou não alfanumérico, FK inexistente, status inválido, preço 0/>2^53−1, capacidade 0/>2^31−1, buyer misto, dois jobs e queued/processado ou terminal/null; migrar de novo.

PASS somente se: Todas as escritas inválidas falham; DB permite ticket sem job apenas fora do serviço, enquanto reserve prova totalidade; dados válidos persistem; sem migração pendente.

Teste: `TEST-A05`. Evidência: Aplicar migração em DB vazio e reexecutar; tentar cada classe de código [A-Z0-9]{12} inválido, status/FK/limites inválidos, dois jobs e combinações state/processed_at inválidas; registrar constraints rejeitadas.

### C-F01-A29 (A29)

Preparação: Demo sentinela em projeto/volume próprio; gate em outro projeto.

Procedimento: Rodar gate positivo e com falha de setup; interromper execução; conferir ps e listener, estado demo.

PASS somente se: Cleanup isolado; nenhum volume demo removido; falha/cleanup não zero; demo responde.

Teste: `TEST-A29`. Evidência: Criar ambiente sentinela, induzir falha em gate isolado, verificar código e containers/volume do sentinela.

### C-F01-A37 (A37)

Preparação: Baseline e fixture Git local sem credenciais.

Procedimento: Executar verificador; alterar item, remover mapeamento, simular relatório faltante, editar relatório commitado.

PASS somente se: Falha estrutural ou de histórico detectada; baseline sem relatórios é válida, release incompleto falha.

Teste: `TEST-A37`. Evidência: Executar verificador sobre fixture Git descartável e mutações negativas.

## Fase INTEGRATED (após merge da wave)

Itens desta fase são explicitamente PENDING_INTEGRATION no relatório local; não contar como PASS e não exigir feature irmã no checkout isolado. Relatório integrado deve incluir todos os itens anteriores e os seguintes, sem pendências.

Nenhum item exclusivo desta fase; o último relatório local permanece válido se nenhum comportamento foi alterado, sem dispensar regressão de release.

## Mapeamento explícito

| Critério | Item      | Teste    | Fase  |
| -------- | --------- | -------- | ----- |
| A01      | C-F01-A01 | TEST-A01 | local |
| A02      | C-F01-A02 | TEST-A02 | local |
| A03      | C-F01-A03 | TEST-A03 | local |
| A04      | C-F01-A04 | TEST-A04 | local |
| A05      | C-F01-A05 | TEST-A05 | local |
| A29      | C-F01-A29 | TEST-A29 | local |
| A37      | C-F01-A37 | TEST-A37 | local |

Qualquer item aplicável sem evidência = FAIL. Fixture deve ser declarada; não usar fixture para substituir efeito real no integrado.
