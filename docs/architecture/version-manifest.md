# Manifesto de versões W0

Status: **candidato para aprovação; W1 ainda deve materializar lockfile e imagens**.

Resolução verificada em 2026-11-26/27. Não usar tags `latest`.

## Plataforma e runtime

| Componente | Pin | linux/amd64 | linux/arm64 |
| --- | --- | --- | --- |
| Python image | `python:3.12.16-slim-bookworm` | manifest `sha256:1475c4f5b6bcb7d35e57661d6f5d7429ec4041275633c15f2b49350ac898276d` | manifest `sha256:209c477b2d5268b578d813ae5a4668682b55252a5b32ad1148dd49e937119101` |
| PostgreSQL image | `postgres:17.12-bookworm` | manifest `sha256:c7a16500f728a9c09731e772f228ee7a29615585e8019772f05b620522f62d03` | manifest `sha256:f3f92abad8b8105cb7e2bb5d76433640025be3221ce9758ba0ebcf0e115a73a9` |
| Playwright image | `mcr.microsoft.com/playwright/python:v1.65.2-noble` | manifest `sha256:cbd0a36dc6f6b8e8bb23703cf6cbe19ebe29e5a1ba43271a11a6c8e53c8b65d0` | manifest `sha256:ef91d1740c114a119450f11e8edb1af4f6d49e641c04207985f0c65a4aaa34a0` |
| Mermaid CLI | `ghcr.io/mermaid-js/mermaid-cli/mermaid-cli:11.12.0` | manifest `sha256:e8edd23a12b7939cabdb7fd9d2c6cbe7d7b8c37f68d62c782fd8e405b61529d6` | manifest `sha256:8380c215a0d611465c3062c4c8c294183ca6aac264d479c3b38364272e4ed4a0` |

Índices multi-arch verificados:

- Python: `sha256:44cf1793efa7c7a476bb0f2cff81443f4a072c90c1cb127e2924933daa3e8c64`.
- PostgreSQL: `sha256:1eff563f6c868b9b433566e9f3cf6e5c79fbd3b95bf70ec7277d376cdbfc50d7`.
- Playwright: `sha256:38dd67fc654b56b3cba611e4c8eb71cd33750e1cd29eea2a5dc00b484817a75f`.
- Mermaid CLI: `sha256:bad64c9d9ad917c8dfbe9d9e9c162b96f6615ff019b37058638d16eb27ce7783`.

## Dependências diretas Python

| Pacote | Pin | SHA-256 linux/amd64 | SHA-256 linux/arm64 |
| --- | --- | --- | --- |
| Django LTS | `5.2.19` | `5965d974a5218a2b68a11dd1276434707f23886525c23f0598eccedaf4f4ca00` | wheel universal |
| psycopg | `3.3.9` | `d2d7d04a1ce6dab4f5b27316bea3b52585cafa2f2d631e5b09dd69823f5c26f6` | wheel universal |
| psycopg-binary | `3.3.9` / CPython 3.12 | `a99f0b9a19ed7a56bf5d6776456b8f15f5364db8853b0f5d184db394a45c391d` | `b081348d8992af26e9b252f04876c286428418a6b7845d8d4caae2044b259668` |
| Gunicorn | `27.0.1` | `378b26b9a38adcf4592f28828233c1716acc55e833ea06bf48719782efaa0d10` | wheel universal |
| Ruff | `0.17.6` | `aa3b08254a732acba246891089a152c47c5733dc36b8ecb76ce8602f8326e5e4` | `435241c61af5909a022f76219d3d1bf24730dc1bf0acabb5ddf4b569ab3cbb30` |
| Playwright Python | `1.65.2` | `58932d35f56767ab7ebcdd3d4a733bfb3e62a1a5bc43c08e28b9fa9b3e61cf33` | `dd3e54b6a926fc6510f272797eec0707dc34ae04d564e74a7056c4a813e53270` |
| openapi-spec-validator | `0.7.2` | `4bbdc0894ec85f1d1bea1d6d9c8b2c3c8d7ccaa13577ef40da9c006c9fd0eb60` | wheel universal |

W1 deve resolver e hashear todas as dependências transitivas. A escolha é
`psycopg[binary]==3.3.9` para o harness local reproduzível; não pressupõe uso em
produção externa.

## Convenções congeladas pelo candidato

- DB e domínio em UTC; UI `America/Sao_Paulo`; API ISO 8601 com offset ou `Z`.
- BRL em centavos inteiros, `1..9007199254740991`; nenhum float.
- Gateway padrão em escala 1: 3 s para fast e 34 s para slow.
- Runtime web/worker usa role DML; bootstrap/migration usa role DDL separada.
- W1 comprova resolução transitiva, arquitetura efetiva, smoke de imagens e clone
  limpo antes de declarar o manifesto materializado.

## Proveniência

Versões de pacotes e wheels foram resolvidas nos índices oficiais do PyPI; versões
e manifests de imagens foram inspecionados nos registries oficiais. A evidência de
OpenAPI/Mermaid e os comandos executados para este candidato ficam no run aditivo
`docs/validation/w0-audit/runs/20261127T0245-0300-amendment/`; o run de
`20261126T2114-0300` é histórico e não prova o SHA atual.
