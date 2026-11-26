# F01 | Plano de implementação

Prerequisitos: baseline aprovada, dependências nenhuma mergeadas; branch `feat/f01-fundacao`; ler spec, contrato, guidelines, skills e estado.

## T-F01-01 | Etapa 1

- [ ] Preparar repositório, fixar versões de containers e dependências, lint, runner e configuração; construir imagens para as arquiteturas suportadas.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A03`: Executar gates e injetar falha em cópia descartável; capturar códigos de saída. Esperado: ./bin/gates falha com teste quebrado, executa testes reais e lint, usa DB isolado e passa com testes válidos.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Build da imagem, `django check`, runner com teste mínimo que falha intencionalmente em cópia descartável e gate documental.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F01-02 | Etapa 2

- [ ] Definir schema de contas, eventos, ingressos e jobs, constraints, índices e migração inicial; usar PostgreSQL e estabelecer convenção de lock.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A05`: Aplicar migração em DB vazio e reexecutar; tentar inserir status inválido, código duplicado, capacidade zero e FK órfã; todas rejeitadas. Esperado: Schema possui FKs, unicidade de código, restrições de status, lotação e preço; migrações reexecutáveis.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Migração em DB limpo, constraints negativas, `makemigrations --check`.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F01-03 | Etapa 3

- [ ] Implementar seed, serviço one-shot de migração, heartbeat inicial do worker, readiness e scripts up/down/gates com ambiente de testes isolado.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A01`: Clonar SHA em pasta temporária; executar up; verificar HTTP e compose ps. Esperado: Clone limpo: ./bin/up constrói, migra, semeia e espera web/worker/DB prontos; /health/ready retorna 200 sem configuração manual.
  - `TEST-A02`: Executar up, seed duas vezes, down, provar porta fechada e ps vazio, up novamente; comparar IDs e autenticação após F02. Esperado: ./bin/down encerra todos os containers e portas iniciados; nova subida conserva dados e seed não duplica contas.
  - `TEST-A04`: Inspeção dos arquivos, ambiente sem .env e sem credenciais externas. Esperado: AGENTS.md e README contêm comandos, endereços, credenciais de seed, mapa; modo padrão não exige gateway real.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Readiness e seed, comparar IDs antes/depois, testar encerramento e reinício.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F01-04 | Etapa 4

- [ ] Comprovar clone limpo, seed repetível, down/up e gate negativo; registrar comandos e ambiente.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A01`: Clonar SHA em pasta temporária; executar up; verificar HTTP e compose ps. Esperado: Clone limpo: ./bin/up constrói, migra, semeia e espera web/worker/DB prontos; /health/ready retorna 200 sem configuração manual.
  - `TEST-A02`: Executar up, seed duas vezes, down, provar porta fechada e ps vazio, up novamente; comparar IDs e autenticação após F02. Esperado: ./bin/down encerra todos os containers e portas iniciados; nova subida conserva dados e seed não duplica contas.
  - `TEST-A03`: Executar gates e injetar falha em cópia descartável; capturar códigos de saída. Esperado: ./bin/gates falha com teste quebrado, executa testes reais e lint, usa DB isolado e passa com testes válidos.
  - `TEST-A04`: Inspeção dos arquivos, ambiente sem .env e sem credenciais externas. Esperado: AGENTS.md e README contêm comandos, endereços, credenciais de seed, mapa; modo padrão não exige gateway real.
  - `TEST-A05`: Aplicar migração em DB vazio e reexecutar; tentar inserir status inválido, código duplicado, capacidade zero e FK órfã; todas rejeitadas. Esperado: Schema possui FKs, unicidade de código, restrições de status, lotação e preço; migrações reexecutáveis.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## Handoff

- [ ] Testes unitários, integração e contratos locais verdes no SHA indicado.
- [ ] Nada fora da ownership; atualizar docs e registrar dependências.
- [ ] Entregar SHA e comandos à sessão nova de avaliação; não entregar veredito pronto.
- [ ] Após aprovação independente e PR mergeado, coordenador atualiza estado.
