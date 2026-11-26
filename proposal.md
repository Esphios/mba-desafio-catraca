# Proposal | Catraca MVP

Status: proposta para aprovação; revisão 0.1 | 26/11/2026.

## Problema e oportunidade

Pequenos organizadores precisam publicar eventos, vender uma quantidade limitada de ingressos e operar a entrada com uma fonte de verdade comum. O risco principal não é uma tela isolada falhar: é venda, gateway, cancelamento e painel divergirem quando operações se sobrepõem. O projeto demonstrará especificação orientada a contratos e integração de trabalho agentic, não só uma aplicação de ingressos.

## Resultados e métricas de sucesso

| Resultado | Medida de aceite |
|---|---|
| Venda correta | 30 compras simultâneas em capacidade 5: exatamente 5 aceitas, 25 esgotadas, duas rodadas |
| Resposta assíncrona | Compra responde pending sem aguardar gateway; cartões rápidos 2–5 s e lentos 30–40 s |
| Cancelamento | Fora dos canais imediatamente; convergência dos ingressos <=10 s, sem ressurreição tardia |
| Operação | Cinco mensagens de check-in corretas, receita histórica e seis indicadores coerentes |
| Segurança | Nenhum acesso indevido a evento de outro dono; parceiro com contrato e chave |
| Reprodutibilidade | Clone limpo sobe em um comando; down e reseed funcionam; gates passam |
| Processo | 7 features com contratos, relatório independente por feature, wave paralela via PRs, estado consistente |

Não são metas de mercado ou SLAs de produção. Medir no ambiente local do avaliador.

## Escopo e entrega

Vitrine sem login, cadastro e sessão de participante, compra unitária, meus ingressos, gestão dos eventos próprios, check-in por código, cancelamento irrevogável e painel. API fixa para parceiro com chave. Seed de duas contas organizadoras e uma participante. Gateway exclusivamente simulado por padrão. Entregar código futuro num repositório público novo, com PRD, FDD/spec, planos, contratos, gates, histórico de avaliações e PRs. O pacote atual entrega apenas a baseline documental e verificadores auxiliares.

## Fora de escopo

Produção/cloud, pagamentos reais, dados de cartão persistidos, e-mail, notificações, app móvel, estética avançada, cadastro de organizador, carrinho/múltiplos ingressos, lugares numerados, transferência ou cancelamento individual, WebSocket, fuso complexo, multitenancy empresarial, observabilidade distribuída e arquitetura de microsserviços. Não exigir login para consultar vitrine. Não introduzir bloqueio de vendas pela data de início sem mudança aprovada (brief condiciona disponibilidade a publicado/não cancelado e lotação).

## Proposta técnica e alternativas

Monólito modular server-rendered com banco relacional e processo worker separado. Django reduz código de sessões, CSRF, formulários e ORM; PostgreSQL permite coordenação transacional entre processos. Um broker externo seria uma terceira dependência de dados e criaria janela de perda entre compra e enfileiramento; job no mesmo banco é suficiente. SQLite não será usado nem para validar concorrência, pois o mecanismo de lock é diferente. UI e API compartilham o mesmo caso de uso, sem regras reimplementadas por canal. Ver ADRs e pesquisa.

## Riscos e condições de aceite

| Risco | Contramedida |
|---|---|
| Oversell | Lock exclusivo por evento, contagem em consulta separada e testes reais com múltiplas conexões |
| Gateway após cancelamento | Transição condicional sob mesmo lock e job terminal durável |
| Receita incorreta | Snapshot em centavos, painel em uma leitura agregada |
| Agentes alterarem contrato após falha | Contrato versionado, relatório append-only, reavaliação independente |
| Conflitos entre branches | Schema e extensão de gestão preparados antes da wave, integração serial e regressão |
| Prazo de resposta worker | Polling curto, processos paralelos, teste de latência real e margem |
| Ambiente inconsistente | Versões fixadas, healthcheck, migrações/seed idempotentes, nomes Compose isolados |

## Questões resolvidas por design (não regras da fundadora)

IDs UUID, e-mail normalizado, UTC em persistência, UI em português, valores máximos de representação validados, chave única de parceiro local, cancelamento síncrono transacional, status de evento draft/published/cancelled, checkedIn derivado de timestamp preservado no estorno, mensagens de operações na mesma página, resposta a acesso de outro dono 404. Não é exigida expiração de sessão específica, mas será definida pela guideline. Aprovar essas escolhas no kickoff; se mudarem, atualizar matriz, ADR e contratos antes do código.

## Sequenciamento

W1 ambiente; W2 identidade; W3 eventos; W4 transações; W5 interfaces e operação em paralelo; W6 regressão e entrega. Estimativa de referência do brief: 8–12h somadas; não é compromisso de execução. Priorizar invariantes e fluxo obrigatório; melhorias opcionais não podem bloquear entrega.
