# Relatório de avaliação | TEMPLATE (não é evidência)

Não salvar este template como relatório real nem marcar PASS sem execução.

- Feature: <Fxx>
- Data/hora UTC: <ISO 8601>
- SHA completo avaliado: <40 hex>
- SHA base / branch: <real>
- Ferramenta e modelo: <real>
- Identificador de sessão: <novo contexto; separado do implementador>
- Contrato e revisão: <caminho + SHA>
- Ambiente: <OS, Docker, imagens, PostgreSQL, modo padrão/rápido>
- Independência: <como contexto separado e checkout limpo foram garantidos>

| Item do contrato | Teste | Comando/procedimento | Esperado | Observado/evidência | Veredito |
|---|---|---|---|---|---|
| <C-Fxx-Axx> | <TEST-Axx> | <comando exato> | <oráculo> | <stdout/HTTP/screenshot caminho> | PASS/FAIL/BLOCKED |

Para cada FAIL: passos de reprodução, expected/actual, impacto e links aos artefatos. Para integração futura, declarar not_applicable_until_integration apenas em X14–X16 antes W6. Nenhuma ocorrência no relatório final. Inserir todos os itens, inclusive erros e negativos. Evidências não podem conter senha/PAN/chave; redigir segredos sem ocultar resultados. Capturar códigos de saída, timestamps e contagens, não apenas texto "passou".

## Veredito global

<APPROVED somente se tudo aplicável PASS; caso contrário REJECTED/BLOCKED>.

## Encerramento

Rodar down do ambiente isolado. Registrar arquivo novo `reports/<UTC>-<shortSHA>.md`, commit sem editar relatórios anteriores. Enviar caminho ao coordenador. Se nova avaliação, novo arquivo.
