# W0 | evidência do candidato AMENDMENT-001

- Executado em: 2026-11-27, `America/Sao_Paulo`.
- Commit candidato testado: `eff1b20cb50ae73313e8245d11a6a068fbda9bd5`.
- Escopo: coerência documental, revisão independente e renderização do candidato,
  sem ratificar a baseline, alterar a trava ou autorizar W1.

## Resultado

O repositório real permaneceu fail-closed: `validate_docs.py` retornou 1 somente
pelos três hashes normativos ainda não ratificados. Em uma cópia efêmera do mesmo
tree, com os hashes candidatos aplicados apenas dentro do container, passaram:

- 2/2 testes focados do parser e da política LF;
- estrutura com 7 features, 37 critérios locais, 16 cruzados e 6 de processo;
- modelo abstrato com 4.290 estados e 36.558 transições;
- testes negativos da baseline e validação de evidência;
- 7/7 mutações inválidas detectadas.

`validate_evidence.py --release` falhou como esperado: F01–F07 estão incompletas,
sem merge/PR, e o estado de release está incompleto. Isso não é defeito do
candidato W0.

O OpenAPI passou em `openapi-spec-validator==0.7.2`. Os 10 fences Mermaid do
commit candidato foram renderizados em SVG e PNG com a imagem pinada do manifesto;
os 30 arquivos-fonte e artefatos estão em `mermaid/`, com digest em
`sha256sum.txt`. O ER alterado foi inspecionado visualmente e mostra
Ticket→PaymentJob como zero-ou-um no schema, coerente com a totalidade adicional
do serviço `reserve`.

## Revisão independente

Quatro avaliadores em contexto fresco — produto/rastreabilidade, arquitetura,
contratos e governança — bloquearam a primeira versão `93b5b1c` com achados
concretos. Os achados foram corrigidos em `eff1b20`; os mesmos quatro papéis
fizeram nova avaliação do delta e emitiram PASS para apresentação à aprovação
humana. Esses pareceres não equivalem à aprovação do proprietário nem ratificam a
baseline.

## Limites

- A trava normativa e `state/project-state.json` não foram modificados.
- Nenhum teste de produto, concorrência, browser ou release foi executado; não há
  implementação.
- A aprovação final explícita do candidato continua sendo pré-condição para o
  commit de ratificação e para G0.
