"""Run the targeted tests against a selected main file and its released package."""
import argparse
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('entrypoint', type=Path)
    parser.add_argument('--embedded', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    entrypoint = args.entrypoint.resolve()
    with tempfile.TemporaryDirectory(prefix='clouds-evolution-release-') as temp:
        if args.embedded:
            destination = Path(temp) / entrypoint.name
            shutil.copy2(entrypoint, destination)
            entrypoint = destination
        sys.path.insert(0, str(entrypoint.parent))
        spec = importlib.util.spec_from_file_location('Clouds_Coder', entrypoint)
        module = importlib.util.module_from_spec(spec)
        sys.modules['Clouds_Coder'] = module
        spec.loader.exec_module(module)
        import liquid_kernel
        if args.embedded:
            assert Path(liquid_kernel.__file__).resolve().parent == (Path(temp) / 'liquid_kernel').resolve()
        print('Verified entrypoint:', args.entrypoint.name, 'package:', 'released embedded' if args.embedded else 'local', flush=True)
        import pytest
        result = pytest.main(['-q', *[str(root / 'tests' / name) for name in (
            'test_prompt_enhancement_recovery.py', 'test_portable_capabilities.py', 'test_split_distribution.py', 'test_outcome_scoring.py', 'test_candidate_retention.py', 'test_acceptance_portability.py', 'test_optimization_opportunities.py', 'test_admin_output_limits.py', 'test_native_output_recovery.py', 'test_proposal_schema_recovery.py', 'test_screenshot_regressions.py', 'test_cross_platform_runtime.py', 'test_admin_bootstrap_compatibility.py', 'test_evaluator_transport_defenses.py', 'test_evolution_policy_safety.py', 'test_pair_deployment_policy.py', 'test_optional_evolution_quotas.py', 'test_agentic_flow_compatibility.py', 'test_json_restart_defenses.py', 'test_evolution_progress.py', 'test_cache_runtime.py', 'test_shared_context_runtime.py', 'test_context_auto_compact.py', 'test_context_memory_recall.py', 'test_live_harness_repairs.py', 'test_agentic_evolution.py', 'test_evolution_integration.py', 'test_liquid_kernel.py', 'test_sqlite_connection_lifecycle.py',
            'test_model_configuration.py', 'test_admin_i18n.py', 'test_http_incomplete_read.py',
            'test_ide_v2.py::IDEWorkspaceServiceTests::test_remote_workspace_sandbox_blocks_outside_read_and_write',
        )]])
        raise SystemExit(result)


if __name__ == '__main__':
    main()
