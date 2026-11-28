#!/usr/bin/env python3
"""Behavioral tests for lifecycle and gate shell contracts.

The fake Docker executable exercises the real shell scripts while keeping these
fast contract tests independent from a daemon. Compose itself is exercised by
the integration gate.
"""

import os
import signal
import socket
import subprocess
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ShellHarnessTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.temp = Path(self.tempdir.name)
        self.log = self.temp / 'docker.log'
        docker = self.temp / 'docker'
        docker.write_text(
            textwrap.dedent(
                '''\
                #!/usr/bin/env bash
                set -u
                printf '%s\\n' "$*" >> "$FAKE_DOCKER_LOG"
                if [[ -n ${FAKE_DOCKER_SLEEP_MATCH:-} && "$*" == *"$FAKE_DOCKER_SLEEP_MATCH"* ]]; then
                  exec sleep 30
                fi
                if [[ -n ${FAKE_DOCKER_FAIL_MATCH:-} && "$*" == *"$FAKE_DOCKER_FAIL_MATCH"* ]]; then
                  exit "${FAKE_DOCKER_FAIL_CODE:-42}"
                fi
                if [[ "$*" == *" ps -q"* ]]; then
                  printf '%s' "${FAKE_DOCKER_PS_OUTPUT:-}"
                fi
                if [[ "$*" == *"ps -aq --filter label=com.docker.compose.project="* ]]; then
                  printf '%s' "${FAKE_PROJECT_CONTAINERS:-}"
                fi
                '''
            )
        )
        docker.chmod(0o755)
        self.env = os.environ | {
            'PATH': f'{self.temp}:{os.environ["PATH"]}',
            'FAKE_DOCKER_LOG': str(self.log),
        }

    def tearDown(self):
        self.tempdir.cleanup()

    def run_script(self, script, *args, env=None, timeout=15):
        return subprocess.run(
            ['bash', str(ROOT / 'bin' / script), *args],
            cwd='/tmp',
            env=self.env | (env or {}),
            text=True,
            capture_output=True,
            timeout=timeout,
        )

    def docker_calls(self):
        return self.log.read_text().splitlines() if self.log.exists() else []

    def test_TEST_A03_feature_gate_runs_real_suite_and_document_checks(self):
        result = self.run_script('gates', '--feature', 'F01')

        self.assertEqual(result.returncode, 0, result.stderr)
        calls = '\n'.join(self.docker_calls())
        self.assertIn('run --rm test', calls)
        self.assertIn('scripts/validate_docs.py', calls)
        self.assertIn('scripts/test_harness.py', calls)
        self.assertIn('scripts/test_baseline.py', calls)
        git_common = subprocess.run(
            ['git', '-C', str(ROOT), 'rev-parse', '--path-format=absolute', '--git-common-dir'],
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        self.assertIn(f'-v {git_common}:{git_common}:ro', calls)
        self.assertIn('GIT_CONFIG_KEY_0=safe.directory', calls)

    def test_TEST_A29_gate_uses_unique_project_and_never_targets_demo(self):
        first = self.run_script('gates')
        first_calls = self.docker_calls()
        self.log.unlink()
        second = self.run_script('gates')
        second_calls = self.docker_calls()

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        first_project_call = next(call for call in first_calls if '--project-name ' in call)
        second_project_call = next(call for call in second_calls if '--project-name ' in call)
        first_project = first_project_call.split('--project-name ', 1)[1].split()[0]
        second_project = second_project_call.split('--project-name ', 1)[1].split()[0]
        self.assertNotEqual(first_project, second_project)
        self.assertNotEqual(first_project, 'catraca-demo')
        self.assertNotEqual(second_project, 'catraca-demo')
        self.assertTrue(any('down --volumes --remove-orphans' in call for call in first_calls))

    def test_TEST_A29_setup_failure_is_preserved_and_cleanup_runs(self):
        result = self.run_script(
            'gates', env={'FAKE_DOCKER_FAIL_MATCH': 'build test', 'FAKE_DOCKER_FAIL_CODE': '42'}
        )

        self.assertEqual(result.returncode, 42, result.stderr)
        self.assertTrue(any('down --volumes --remove-orphans' in c for c in self.docker_calls()))

    def test_TEST_A29_bootstrap_failure_propagates_before_web_or_worker_start(self):
        result = self.run_script(
            'up',
            env={
                'CAT_PROJECT': 'catraca-bootstrap-contract',
                'CAT_PORT': '18123',
                'CAT_PROFILE': 'test',
                'FAKE_DOCKER_FAIL_MATCH': ' bootstrap',
                'FAKE_DOCKER_FAIL_CODE': '44',
            },
        )

        self.assertEqual(result.returncode, 44, result.stderr)
        calls = self.docker_calls()
        bootstrap_call = next(call for call in calls if ' up ' in call and ' bootstrap' in call)
        self.assertIn('--exit-code-from bootstrap', bootstrap_call)
        self.assertFalse(any(' up ' in call and ' web worker' in call for call in calls))

    def test_TEST_A29_host_readiness_timeout_diagnoses_and_cleans_up(self):
        bash_env = self.temp / 'bash-env'
        bash_env.write_text('sleep() { SECONDS=$((SECONDS + 30)); }\n')
        with socket.create_server(('127.0.0.1', 0)) as listener:
            result = self.run_script(
                'up',
                env={
                    'BASH_ENV': str(bash_env),
                    'CAT_PROJECT': 'catraca-timeout-contract',
                    'CAT_PORT': str(listener.getsockname()[1]),
                },
                timeout=5,
            )

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('Host readiness did not return HTTP 200', result.stderr)
        self.assertIn('Startup failed for project catraca-timeout-contract', result.stderr)
        self.assertTrue(any('down --remove-orphans' in call for call in self.docker_calls()))

    def test_TEST_A29_cleanup_failure_turns_success_into_failure(self):
        result = self.run_script(
            'gates',
            env={'FAKE_DOCKER_FAIL_MATCH': 'down --volumes', 'FAKE_DOCKER_FAIL_CODE': '43'},
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Cleanup failed', result.stderr)

    def test_TEST_A29_term_interrupt_is_nonzero_and_cleans_its_project(self):
        process = subprocess.Popen(
            ['bash', str(ROOT / 'bin/gates')],
            cwd='/tmp',
            env=self.env
            | {
                'FAKE_DOCKER_SLEEP_MATCH': 'run --rm test',
                'FAKE_PROJECT_CONTAINERS': 'fake-gate-container',
            },
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if self.log.exists() and 'run --rm test' in self.log.read_text():
                break
            time.sleep(0.05)
        else:
            process.kill()
            self.fail('gate never reached the test command')

        process.send_signal(signal.SIGTERM)
        _, stderr = process.communicate(timeout=10)

        self.assertNotEqual(process.returncode, 0, stderr)
        self.assertTrue(any('down --volumes --remove-orphans' in c for c in self.docker_calls()))
        self.assertTrue(any('rm --force fake-gate-container' in c for c in self.docker_calls()))

    def test_TEST_A37_release_runs_release_evidence_phase_and_propagates_failure(self):
        result = self.run_script(
            'gates',
            '--release',
            env={'FAKE_DOCKER_FAIL_MATCH': 'validate_evidence.py --release'},
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(
            any('validate_evidence.py --release' in call for call in self.docker_calls())
        )

    def test_TEST_A03_unknown_feature_and_malformed_arguments_fail_before_docker(self):
        for arguments in (('--feature', 'F99'), ('--feature',), ('--release', 'extra')):
            with self.subTest(arguments=arguments):
                result = self.run_script('gates', *arguments)
                self.assertEqual(result.returncode, 2)
        self.assertEqual(self.docker_calls(), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
