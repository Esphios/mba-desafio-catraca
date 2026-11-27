# F03 | Plano de implementação

Entrada: baseline W0 aprovada, dependências F01, F02 integradas e aprovadas, branch exclusiva. Skills: transaction-safety, secure-boundaries, feature-implementation.

## T-F03-01

**Entrega:** Implementar DTO, validação e persistência de draft, formulário de edição.

**Validação:** lint, checks do framework e testes já implementados; fase 1 não exige endpoints futuros.
- `TEST-A09` (A09): Enviar campos vazios, preço 0, capacidade 0, data ontem, depois data futura válida. Resultado: 422 ou formulário com erros; nenhum evento inválido; sucesso cria draft com valores normalizados.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F03-02

**Entrega:** Implementar lock, edição/publicação e consultas de ocupação; casos limite e estado terminal.

**Validação:** lint, checks do framework e testes já implementados; fase 2 não exige endpoints futuros.
- `TEST-A11` (A11): Editar para cap 1, 2 e 3; trocar preço para 15000; comparar snapshot de tickets. Resultado: Cap 1 nega sem mudança; 2 e 3 aceitam; ingressos anteriores continuam 10000.
- `TEST-A12` (A12): Tentar editar e publicar cancelado, consultar lista pública. Resultado: Cancelado ausente e imutável; somente publicado elegível.
- `TEST-A31` (A31): Executar limites numéricos, data igual a now, inválida e futura; atrasar lock até data vencer; editar parcialmente inválido. Resultado: Validação estrita dentro da escrita; sem alteração parcial; moeda decimal exata.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F03-03

**Entrega:** Implementar páginas de gestão e slot operacional; integração com identidade.

**Validação:** lint, checks do framework e testes já implementados; fase 3 não exige endpoints futuros.
- `TEST-A10` (A10): Abrir gestão E1, listar A, consultar catálogo, publicar e recarregar. Resultado: URL estável, apenas eventos de A na gestão, E1 fora antes e visível depois.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F03-04

**Entrega:** Executar testes de estado, data, dono e DB; fixar interface para F04/F05/F06/F07.

**Validação:** lint, checks do framework e testes já implementados; fase 4 não exige endpoints futuros.
- `TEST-A09` (A09): Enviar campos vazios, preço 0, capacidade 0, data ontem, depois data futura válida. Resultado: 422 ou formulário com erros; nenhum evento inválido; sucesso cria draft com valores normalizados.
- `TEST-A10` (A10): Abrir gestão E1, listar A, consultar catálogo, publicar e recarregar. Resultado: URL estável, apenas eventos de A na gestão, E1 fora antes e visível depois.
- `TEST-A11` (A11): Editar para cap 1, 2 e 3; trocar preço para 15000; comparar snapshot de tickets. Resultado: Cap 1 nega sem mudança; 2 e 3 aceitam; ingressos anteriores continuam 10000.
- `TEST-A12` (A12): Tentar editar e publicar cancelado, consultar lista pública. Resultado: Cancelado ausente e imutável; somente publicado elegível.
- `TEST-A31` (A31): Executar limites numéricos, data igual a now, inválida e futura; atrasar lock até data vencer; editar parcialmente inválido. Resultado: Validação estrita dentro da escrita; sem alteração parcial; moeda decimal exata.
- `TEST-X02` (X02): DB limpo migrado; criar evento futuro e rejeitar ontem. Resultado: Migração e clock da fundação permitem criação e rejeição de data vencida.
- `TEST-X03` (X03): Browser e POST direto B contra E1 de A; ausência de dados, estado intacto. Resultado: URL de gestão e listagem usam dono da sessão; B não pode editar/publicar A.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## Integração posterior
Não há item exclusivo de integração atribuído a esta feature; regressão global é obrigatória.

## Handoff
Entregar SHA limpo, base SHA, interfaces, comandos, logs redigidos e desvios. Avaliador novo, sem histórico de conversa, julga apenas contrato e evidência. Coordenador integra após local PASS; relatório final da feature exige também itens integrados, se houver.
