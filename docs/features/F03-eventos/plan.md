# F03 | Plano de implementação

Prerequisitos: baseline aprovada, dependências F01, F02 mergeadas; branch `feat/f03-eventos`; ler spec, contrato, guidelines, skills e estado.

## T-F03-01 | Etapa 1

- [ ] Implementar validação e formulários de evento, conversão monetária, serviços e consultas por dono.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A09`: Tabela de casos com agora, passado, futuro, 0, -1, 1.5, preço zero e campos vazios; checar persistência. Esperado: Nome/local não vazios; lotação inteira >=1; preço em centavos >0; início estritamente futuro em criar e editar, inclusive requisição direta.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Tabela de casos de data/lotação/preço, proprietário vem da sessão.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F03-02 | Etapa 2

- [ ] Implementar lock, consultas de ocupação, edição/publicação transacionais e DTO público.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A11`: Fixtures de dois ingressos ocupando; reduzir para 1 rejeita, 2/3 aceitam; snapshot histórico inalterado. Esperado: Editar sob lock do evento; capacidade abaixo de pending+confirmed é rejeitada; igual/acima aceita; preço novo não altera snapshot de ingressos.
  - `TEST-A12`: Fixture de estado cancelled; POST edição/publicação e leitura pública; negar sem mutação. Esperado: Evento cancelled não pode ser alterado/republicado; catálogo e disponibilidade pública o excluem.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Lock e contagem depois do lock; fixture de pending e confirmed; redução inválida e snapshot histórico.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F03-03 | Etapa 3

- [ ] Construir listagem e gestão do organizador e preparar ponto de extensão para operações.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A10`: Criar E1, consultar catálogo antes/depois e abrir URL de gestão com dono. Esperado: Evento nasce draft; publicar torna visível a consulta pública; gestão tem URL estável e lista apenas próprios eventos.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Criar, listar, publicar e abrir gestão; B tenta URL direta/POST; catálogo draft/publicado.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F03-04 | Etapa 4

- [ ] Executar testes de validação, estado, dono e lock; congelar DTO e interfaces para F04.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A09`: Tabela de casos com agora, passado, futuro, 0, -1, 1.5, preço zero e campos vazios; checar persistência. Esperado: Nome/local não vazios; lotação inteira >=1; preço em centavos >0; início estritamente futuro em criar e editar, inclusive requisição direta.
  - `TEST-A10`: Criar E1, consultar catálogo antes/depois e abrir URL de gestão com dono. Esperado: Evento nasce draft; publicar torna visível a consulta pública; gestão tem URL estável e lista apenas próprios eventos.
  - `TEST-A11`: Fixtures de dois ingressos ocupando; reduzir para 1 rejeita, 2/3 aceitam; snapshot histórico inalterado. Esperado: Editar sob lock do evento; capacidade abaixo de pending+confirmed é rejeitada; igual/acima aceita; preço novo não altera snapshot de ingressos.
  - `TEST-A12`: Fixture de estado cancelled; POST edição/publicação e leitura pública; negar sem mutação. Esperado: Evento cancelled não pode ser alterado/republicado; catálogo e disponibilidade pública o excluem.
  - `TEST-X02`: DB limpo migrado; criar evento futuro e rejeitar ontem. Esperado: Migração e clock da fundação permitem criação e rejeição de data vencida.
  - `TEST-X03`: Browser e POST direto B contra E1 de A; ausência de dados, estado intacto. Esperado: URL de gestão e listagem usam dono da sessão; B não pode editar/publicar A.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## Handoff

- [ ] Testes unitários, integração e contratos locais verdes no SHA indicado.
- [ ] Nada fora da ownership; atualizar docs e registrar dependências.
- [ ] Entregar SHA e comandos à sessão nova de avaliação; não entregar veredito pronto.
- [ ] Após aprovação independente e PR mergeado, coordenador atualiza estado.
