# W0 | atestações individuais dos revisores do amendment

Cada arquivo foi criado pela própria sessão canônica indicada em seu cabeçalho,
após o avaliador final apontar que o run anterior preservava apenas o resumo dos
pareceres. As sessões escreveram somente seu arquivo, não tocaram no Git index e
observaram `0af40390f83b92cad1efe6fd748f603e9dd27186` durante o registro.

| Papel | Sessão canônica | Arquivo | SHA-256 |
| --- | --- | --- | --- |
| Produto/rastreabilidade | `/root/w0_amend_product` | `product.md` | `50a1ad932e122eafcc09281640ddf25088d17b3e4bf30a7ea809458c73fd95e6` |
| Arquitetura/schema/transações | `/root/w0_amend_arch` | `architecture.md` | `47d26ecbb3e81db14b215790802fd1bb8301cdbb00962e2c5ca981fb5d13443a` |
| Contratos/interfaces | `/root/w0_amend_contracts` | `contracts.md` | `39a90c4b35410ae8a2b772c958bce28f02911c490f1231d88dabf12c974490d6` |
| Governança/harness | `/root/w0_amend_governance` | `governance.md` | `2cce538fae13850fcaa7b4567e123d328f9129ff6f227cf67fdea03eb3fc5cd6` |

## Limite declarado

As quatro sessões foram agentes separados e não atuaram como implementadores, mas
compartilharam o worktree principal e não conseguem comprovar, por metadado interno,
o modo exato de fork ou isolamento técnico forte. Esse limite foi preservado nas
atestações, não reinterpretado como independência absoluta.

Para cumprir o item 6 do checklist de forma demonstrável, este registro será seguido
por duas avaliações novas com `fork_turns=none`, cada uma em worktree read-only
separado, com identidade, caminho, SHA, acessos, comandos e handoff registrados.
