# W0 | manifesto de sessões frescas

Registro do coordenador `/root`, criado a partir das chamadas reais de colaboração e
dos worktrees observados antes do despacho. Este manifesto não substitui os
pareceres autorais nem prova criptograficamente a plataforma; preserva os parâmetros
efetivamente enviados às sessões.

## Snapshot comum

- Despacho: 2026-11-27 09:45, `America/Sao_Paulo`.
- SHA: `b8db254568d6d359ae8261245814c365c97dbea6`.
- Ambos os worktrees estavam limpos, em detached HEAD, no mesmo SHA.
- Cada `spawn_agent` usou `fork_turns=none`; nenhuma transcrição do coordenador foi
  herdada pelo mecanismo de fork.
- O briefing continha apenas tarefa, paths, SHA, fontes obrigatórias, comandos e
  contrato de saída.
- As sessões não foram autorizadas a editar o checkout avaliado, Git index ou
  histórico, nem a despachar subagentes.

## Sessões e isolamento de filesystem

| Papel | Sessão canônica | Worktree exclusivo | Relatório autorizado |
| --- | --- | --- | --- |
| Produto/rastreabilidade | `/root/w0_fresh_product` | `C:\Users\eduar\AppData\Local\Temp\catraca-w0-product-32410078` | `product.md` |
| Arquitetura/governança | `/root/w0_fresh_architecture` | `C:\Users\eduar\AppData\Local\Temp\catraca-w0-architecture-32410078` | `architecture.md` |

Os relatórios são escritos aditivamente no repositório principal somente depois da
avaliação, em paths distintos deste diretório. O handoff ocorre pela resposta da
sessão ao coordenador e pelo próprio arquivo autoral. O coordenador verificará SHA,
status dos worktrees, hashes dos relatórios e ausência de outros paths antes de
commitar a evidência.
