# F03 | Contrato de avaliação

Versão 2 proposta. Ambiente: checkout limpo do SHA, Docker/Compose e Git; `bash bin/up` e `bash bin/gates --feature F03` após implementados. Banco PostgreSQL real, dados sintéticos, projeto/porta exclusivos, gateway padrão para itens de tempo. O avaliador cria relatório novo sem alterar código.

## Fase LOCAL (antes do merge)

### C-F03-A09 (A09)

Preparação: A autenticado; formulário de criação e edição.

Procedimento: Enviar campos vazios, preço 0, capacidade 0, data ontem, depois data futura válida.

PASS somente se: 422 ou formulário com erros; nenhum evento inválido; sucesso cria draft com valores normalizados.

Teste: `TEST-A09`. Evidência: Tabela de casos com agora, passado, futuro, 0, -1, 1.5, preço zero e campos vazios; checar persistência.

### C-F03-A10 (A10)

Preparação: Dois organizadores, E1 draft e E2 de B.

Procedimento: Abrir gestão E1, listar A, consultar catálogo, publicar e recarregar.

PASS somente se: URL estável, apenas eventos de A na gestão, E1 fora antes e visível depois.

Teste: `TEST-A10`. Evidência: Criar E1, consultar catálogo antes/depois e abrir URL de gestão com dono.

### C-F03-A11 (A11)

Preparação: E1 com pending e confirmed, ocupação 2; preço 10000.

Procedimento: Editar para cap 1, 2 e 3; trocar preço para 15000; comparar snapshot de tickets.

PASS somente se: Cap 1 nega sem mudança; 2 e 3 aceitam; ingressos anteriores continuam 10000.

Teste: `TEST-A11`. Evidência: Fixtures de dois ingressos ocupando; reduzir para 1 rejeita, 2/3 aceitam; snapshot histórico inalterado.

### C-F03-A12 (A12)

Preparação: Evento fixture cancelled, publicado e draft.

Procedimento: Tentar editar e publicar cancelado, consultar lista pública.

PASS somente se: Cancelado ausente e imutável; somente publicado elegível.

Teste: `TEST-A12`. Evidência: Fixture de estado cancelled; POST edição/publicação e leitura pública; negar sem mutação.

### C-F03-A31 (A31)

Preparação: Clock injetável e A dono de evento.

Procedimento: Executar limites numéricos, data igual a now, inválida e futura; atrasar lock até data vencer; editar parcialmente inválido.

PASS somente se: Validação estrita dentro da escrita; sem alteração parcial; moeda decimal exata.

Teste: `TEST-A31`. Evidência: Tabela de limites: ontem/agora/futuro, 0/1/1.5, 0/0.01/1.001, campos vazios, limite numérico.

### C-F03-X02 (X02)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: DB limpo migrado; criar evento futuro e rejeitar ontem.

PASS somente se: Migração e clock da fundação permitem criação e rejeição de data vencida.

Teste: `TEST-X02`. Evidência: DB limpo migrado; criar evento futuro e rejeitar ontem.

### C-F03-X03 (X03)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: Browser e POST direto B contra E1 de A; ausência de dados, estado intacto.

PASS somente se: URL de gestão e listagem usam dono da sessão; B não pode editar/publicar A.

Teste: `TEST-X03`. Evidência: Browser e POST direto B contra E1 de A; ausência de dados, estado intacto.

## Fase INTEGRATED (após merge da wave)

Itens desta fase são explicitamente PENDING_INTEGRATION no relatório local; não contar como PASS e não exigir feature irmã no checkout isolado. Relatório integrado deve incluir todos os itens anteriores e os seguintes, sem pendências.

Nenhum item exclusivo desta fase; o último relatório local permanece válido se nenhum comportamento foi alterado, sem dispensar regressão de release.

## Mapeamento explícito

| Critério | Item      | Teste    | Fase  |
| -------- | --------- | -------- | ----- |
| A09      | C-F03-A09 | TEST-A09 | local |
| A10      | C-F03-A10 | TEST-A10 | local |
| A11      | C-F03-A11 | TEST-A11 | local |
| A12      | C-F03-A12 | TEST-A12 | local |
| A31      | C-F03-A31 | TEST-A31 | local |
| X02      | C-F03-X02 | TEST-X02 | local |
| X03      | C-F03-X03 | TEST-X03 | local |

Qualquer item aplicável sem evidência = FAIL. Fixture deve ser declarada; não usar fixture para substituir efeito real no integrado.
