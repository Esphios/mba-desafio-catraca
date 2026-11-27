# F05 | Plano de implementação

Entrada: baseline W0 aprovada, dependências F02, F03, F04 integradas e aprovadas, branch exclusiva. Skills: secure-boundaries, browser-validation, feature-implementation.

## T-F05-01

**Entrega:** Implementar catálogo público e detalhe com estados vazio/lotado.

**Validação:** lint, checks do framework e testes já implementados; fase 1 não exige endpoints futuros.
- `TEST-A18` (A18): Visitar vitrine anonimamente e detalhe E3; forjar POST quando vaga termina. Resultado: Só E2/E3 listados; mensagem Ingressos esgotados no detalhe ou tentativa; sem venda adicional.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F05-02

**Entrega:** Implementar compra, mapeamento de erros e Meus ingressos por identidade.

**Validação:** lint, checks do framework e testes já implementados; fase 2 não exige endpoints futuros.
- `TEST-A19` (A19): Cadastrar, comprar 0001, abrir Meus ingressos imediatamente e recarregar até 5s. Resultado: Evento e código visíveis, pendente inicialmente, confirmado até deadline; sem esperar gateway no POST.
- `TEST-A20` (A20): Abrir Meus ingressos, trocar sessão, tentar URL/ID forjado e compra anônima. Resultado: Só tickets do ID da sessão; cinco rótulos exatos; parceiro não aparece; visitante não compra.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F05-03

**Entrega:** Testar fluxo browser, negativos, titularidade, CSRF e status.

**Validação:** lint, checks do framework e testes já implementados; fase 3 não exige endpoints futuros.
- Criar teste unitário ou de integração para a entrega desta etapa; provar caminho negativo e resultado observado antes da próxima etapa.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F05-04

**Entrega:** Avaliar dependências anteriores; entregar handoff sem modificar F06/F07.

**Validação:** lint, checks do framework e testes já implementados; fase 4 não exige endpoints futuros.
- `TEST-A18` (A18): Visitar vitrine anonimamente e detalhe E3; forjar POST quando vaga termina. Resultado: Só E2/E3 listados; mensagem Ingressos esgotados no detalhe ou tentativa; sem venda adicional.
- `TEST-A19` (A19): Cadastrar, comprar 0001, abrir Meus ingressos imediatamente e recarregar até 5s. Resultado: Evento e código visíveis, pendente inicialmente, confirmado até deadline; sem esperar gateway no POST.
- `TEST-A20` (A20): Abrir Meus ingressos, trocar sessão, tentar URL/ID forjado e compra anônima. Resultado: Só tickets do ID da sessão; cinco rótulos exatos; parceiro não aparece; visitante não compra.
- `TEST-X06` (X06): Dois browsers com sessões distintas; compra e acesso cruzado. Resultado: Sessão define dono do ingresso; anônimo e outra conta não veem compra pessoal.
- `TEST-X07` (X07): Criar draft, publicar, reservar até lotar, cancelar fixture; recarregar catálogo. Resultado: A publicação e as vagas calculadas por F03 chegam à vitrine; draft/cancelled não são exibidos, inclusive fixture cancelada. A ação real de cancelar é validada em X14.
- `TEST-X08` (X08): Comprar 0004, observar lotação, após 45s ver declined e vaga. Resultado: Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## Integração posterior
Não há item exclusivo de integração atribuído a esta feature; regressão global é obrigatória.

## Handoff
Entregar SHA limpo, base SHA, interfaces, comandos, logs redigidos e desvios. Avaliador novo, sem histórico de conversa, julga apenas contrato e evidência. Coordenador integra após local PASS; relatório final da feature exige também itens integrados, se houver.
