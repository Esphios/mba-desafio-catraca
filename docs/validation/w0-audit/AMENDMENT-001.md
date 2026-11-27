# AMENDMENT-001 | Ratificação controlada da baseline W0

Status: **ratificado por produto e arquitetura em 2026-11-27**.

Autorização de preparação: proprietário solicitou prosseguir com a opção recomendada
de ratificação controlada em 2026-11-27. Após as revisões independentes e correções,
o proprietário aprovou explicitamente `AMENDMENT-001` em 2026-11-27. A autorização
de W1 continua condicionada ao G0 limpo e ao commit separado de estado.

## Motivo

O brief original e o commit de importação citado pela auditoria histórica não são
recuperáveis. A busca local, no remoto e no workspace está registrada em
`runs/20261127T0018-0300-recovery-search.md`. A trava existente também nunca
correspondeu ao PRD e ao traceability commitados. Regenerar hashes sem amendment
ocultaria o problema.

## Autoridade ratificada

Após aprovação final deste amendment, PRD, OpenAPI e traceability tornam-se as três
fontes primárias protegidas por hash. Matriz, contracts, test catalog, HLD/ADRs e
interfaces são refinamentos normativos derivados: `validate_docs.py` verifica seus
IDs e mapeamentos, e qualquer mudança sem novo amendment/revisão continua proibida,
embora não sejam byte-locked. R01–R13, as três rotas fixas e os critérios A/X/P não
são reduzidos.

## Decisões ratificadas

1. `normalize_email` continua sendo fornecido por F01. F04 aplica a rotina no
   `PartnerBuyer` antes do lock; F06 valida envelope/transporte e não importa F01.
   O DAG permanece sem uma dependência oculta F01→F06.
2. F02 fornece `Actor`, guards de papel e predicado genérico de ownership. F03 é o
   único dono de lookup/lock de Event por meio de `event_guard`.
3. Os nomes estáveis do catálogo são `public_catalog` e `public_detail`. Clock,
   fixture factory, worker command, transição de ticket e DTO básico de gestão são
   portas explícitas no registro interno.
4. O limite único de preço é `1..9007199254740991` centavos (inteiro JSON seguro),
   ainda armazenado em `bigint`; capacidade é `1..2147483647`.
5. IDs públicos são UUID; código de ingresso tem exatamente 12 caracteres
   alfanuméricos maiúsculos. A05/A13/A21/A23 provam schema, geração, serialização e
   UUID malformado; o OpenAPI não altera paths, campos, status ou precedência.
6. E-mail canônico tem até 254 caracteres; o OpenAPI não impõe esse máximo ao valor
   bruto antes de strip/casefold. Na API, chave ausente/duplicada/inválida falha
   antes da leitura; body autenticado aceita até 16.384 bytes, e 16.385 retorna
   `422 invalid_request`. A17/A34 exercitam os limites e a borda inclusiva.
7. A FK única de PaymentJob garante zero ou um job por Ticket no schema; o serviço
   `reserve` garante exatamente um no mesmo commit. O CHECK exige queued/null ou
   done|ignored/non-null para `processed_at`.
8. Toda mutação de agregado já existente usa event→ticket→job. `create_event` é uma
   transação atômica sem row lock porque ainda não existe linha Event.
9. F01 precria hooks settings-driven de gestão; F03 possui shell/default básico e
   F07 possui provider/partial/URLconf finais. O gate local usa overrides reais sem
   editar wiring; após merge, o coordenador troca defaults e repete A28 antes dos
   integrados. O seletor `purchase-submit` integra o contrato web.
10. O manifesto de versões aprovado está em
    `docs/architecture/version-manifest.md`; W1 materializa imagens e lockfile.

## Hashes do conteúdo ratificado

Estes são os hashes aprovados e gravados na trava pelo commit explícito de
ratificação.

| Artefato | SHA-256 ratificado |
| --- | --- |
| `docs/prd/PRD.md` | `5f2764b10fab3da8027d1d423aa1b9abba270bf96812b86a16bb4c89ee0d9fec` |
| `docs/interfaces/partner.openapi.json` | `141992b6ba262e96b55bdba8dc7bb541110b6a7174a7b448a9a6d778720e0a00` |
| `docs/validation/traceability.json` | `42a0c0233a29f29fccaee5a793c70c035c5bb1fb86ddfbc3a7b5c4eabe50d7ad` |

## Situação da revisão independente

Quatro revisores novos avaliaram o primeiro candidato em produto, arquitetura,
contratos e governança. Todos bloquearam a ratificação e produziram correções:
cobertura UUID/código/body cap, digests por arquitetura, wiring F07 e proveniência.
As correções foram incorporadas em `eff1b20`; os quatro revisores reavaliaram o
delta e emitiram PASS para apresentação. O proprietário aprovou explicitamente o
pacote e o manifesto em 2026-11-27. A evidência está no run aditivo
`runs/20261127T0245-0300-amendment/`.

## Sequência de aceitação

1. Aplicar as decisões coordenadamente nos documentos e verificadores, sem editar a
   trava para esconder drift.
2. Revisar o diff normativo e executar G0; durante a preparação, o drift esperado
   deve continuar fail-closed.
3. Obter revisão em contextos independentes e aprovação explícita do candidato e do
   manifesto.
4. Atualizar `normative-lock.json` em commit explícito de ratificação e reproduzir G0
   no SHA limpo.
5. Registrar esse SHA como `baselineCommit`, `baseline=approved` e `currentWave=1`
   em commit de estado separado. Somente então despachar F01.

## Não decisões

- Nenhuma feature está implementada ou aprovada.
- Nenhum PASS documental prova concorrência, segurança ou runtime do produto.
- Relatórios históricos permanecem imutáveis.
- ADRs estão `accepted` pela ratificação final do pacote.

## Registro da ratificação

- Conteúdo candidato aprovado: `eff1b20cb50ae73313e8245d11a6a068fbda9bd5`.
- Evidência aditiva revisada: `d1704f61312630fcae4f1f3eec79e7fec5c793e4`.
- Aprovação humana explícita: proprietário, 2026-11-27, mensagem
  `Aprovo o AMENDMENT-001`.
- Próxima condição: G0 integral no commit de ratificação e atualização separada de
  `state/project-state.json` antes de despachar F01.
