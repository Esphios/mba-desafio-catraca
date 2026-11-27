"""W0 diagnostic only. Mutants are isolated and destroyed; no normative changes."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_docs import validate


def state_wave(text):
    data = json.loads(text)
    data['features'][0]['wave'] = 99
    return json.dumps(data)


def api_type(text):
    data = json.loads(text)
    data['paths']['/api/partner/events']['get']['responses']['200']['content']['application/json']['schema']['items']['properties']['priceCents']['type'] = 'string'
    return json.dumps(data)


CASES = [
    ('Markdown acceptance altered', 'requirements-matrix.md', lambda x: x.replace('Clone limpo: ./bin/up constrói', 'Clone limpo: ./bin/up NÃO constrói', 1)),
    ('State wave jumps', 'state/project-state.json', lambda x: x.replace('"currentWave": 0', '"currentWave": 5')),
    ('State feature wave diverges', 'state/project-state.json', state_wave),
    ('OpenAPI priceCents integer changed to string', 'docs/interfaces/partner.openapi.json', api_type),
    ('Contract oracle contradicted', 'docs/features/F01-fundacao/contract.md', lambda x: x.replace('Exit 0; DB, web e worker prontos', 'Exit 1; DB, web e worker prontos', 1)),
    ('Test catalog oracle contradicted', 'docs/validation/test-catalog.md', lambda x: x.replace('Exatamente 5/25 em todas as rodadas', 'Exatamente 6/24 em todas as rodadas', 1)),
    ('PRD acceptance contradicted', 'docs/prd/PRD.md', lambda x: x.replace('Não reduzir lotação abaixo de ocupação', 'Permitir reduzir lotação abaixo de ocupação', 1)),
]

if __name__ == '__main__':
    missed = 0
    with tempfile.TemporaryDirectory() as temp:
        copy = Path(temp) / 'project'
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        assert not validate(copy), 'Unmodified baseline does not pass'
        for label, file, mutation in CASES:
            path = copy / file
            original = path.read_text(encoding='utf-8')
            modified = mutation(original)
            assert original != modified, f'Mutation did not apply: {label}'
            path.write_text(modified, encoding='utf-8')
            try:
                errors = validate(copy)
                print(f'{label}: {"DETECTED" if errors else "UNDETECTED"}')
                missed += not bool(errors)
            finally:
                path.write_text(original, encoding='utf-8')
        assert not validate(copy), 'Restored baseline does not pass'
    print(f'{missed}/{len(CASES)} invalid mutants accepted by structural gate.')
    sys.exit(1 if missed else 0)
