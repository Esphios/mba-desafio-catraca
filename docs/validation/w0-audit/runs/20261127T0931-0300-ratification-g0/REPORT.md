# W0 | G0 da baseline ratificada

- Executado em: 2026-11-27 09:31–09:37, `America/Sao_Paulo`.
- Commit ratificado e testado: `19059603b450981630477dac3732acfdc8fe9d1d`.
- Aprovação humana: proprietário, mensagem `Aprovo o AMENDMENT-001`.
- Escopo: ratificação e G0; nenhuma feature de produto foi implementada.

## Resultado do G0

Todos os gates exigidos para W0 passaram no worktree limpo:

- `validate_docs.py`: 7 features, 37 critérios locais, 16 cross-feature e 6 de
  processo;
- `verify_model.py`: 4.290 estados e 36.558 transições, negativo de oversell
  rejeitado;
- `test_baseline.py`: todos os negativos estruturais detectados;
- `validate_evidence.py`: estrutura e histórico válidos para a fase;
- `reproduce_mutations.py`: 7/7 mutações inválidas detectadas.

`validate_evidence.py --release` retornou 1, como obrigatório em W0, somente porque
F01–F07 não possuem implementação, merge/PR ou estado final. Nenhum resultado de
runtime, concorrência, segurança ou release foi inferido deste PASS documental.

## Ambiente e pins

- Host: Windows 11 Home 64-bit `10.0.26200`, WSL2 Linux x86_64
  `6.6.87.2-microsoft-standard-WSL2`.
- Python host: `3.12.10`; Git: `2.52.0.windows.1`.
- Docker client/server: `29.9.2`, engine Linux/amd64; Compose `5.6.1`.
- Imagem Python pinada: Python `3.12.16`.
- Imagem PostgreSQL pinada: PostgreSQL `17.12`.
- Imagem Playwright pinada: Python `3.12.3`; o pin da imagem foi resolvido pelo
  digest amd64 aprovado.
- Imagem Mermaid pinada: CLI `11.12.0`.
- OpenAPI: `openapi-spec-validator==0.7.2` retornou
  `docs/interfaces/partner.openapi.json: OK`.

## Mermaid

Os 10 fences atuais — 6 de arquitetura, 3 de design e 1 do PRD — foram comparados
com as 10 fontes rastreadas e coincidem exatamente. A imagem Mermaid pinada gerou
10 SVG e 10 PNG sem erro.

Dezesseis saídas foram byte-idênticas aos artefatos anteriores. `design-02` e
`design-03` diferiram em SVG/PNG porque o renderer de state diagram gera pontos de
controle aleatórios para curvas rough. O diff mostrou somente variação nesses
pontos; as quatro imagens foram inspecionadas lado a lado e são visualmente
equivalentes, legíveis e sem erro de renderização. A fonte Mermaid é idêntica.

## Limites e próxima transição

- `state/project-state.json` ainda permanece em `baseline=proposed`, wave 0.
- Este run não autoriza por si só uma feature; a mudança de estado deve ocorrer em
  commit separado apontando `baselineCommit` para o SHA ratificado acima.
- Um avaliador independente deve revisar a ratificação e este run antes do despacho
  de F01.
