"""Start a real isolated server with a stalled optional JS download and verify restart readiness.

Only the temporary copy's downloader is fault-injected; supervisor, HTTP server,
nonce, PID verification, configuration and embedded package are production code.
"""
import argparse
import importlib.util
import json
import os
import shutil
import socket
import sys
import tempfile
import time
from pathlib import Path
from urllib.request import ProxyHandler, build_opener


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]/'Clouds_Coder.py'
    report = {'verification':'real isolated restart with 70s downloader fault', 'production_service_restarted':False}
    with tempfile.TemporaryDirectory(prefix='clouds-real-restart-') as directory:
        root = Path(directory)
        entry = root/'Clouds_Coder.py'
        shutil.copy2(source,entry)
        injection = '''\n# Test-only fault injection: optional download stalls, actual HTTP services still start.\ndef ensure_offline_js_libs(*args, **kwargs):\n    time.sleep(70)\n    return {"verification_fault": True}\n'''
        text = entry.read_text()
        text = text.replace('if __name__ == "__main__":\n    main()', injection+'\nif __name__ == "__main__":\n    main()')
        entry.write_text(text)
        sys.path.insert(0,str(root))
        spec = importlib.util.spec_from_file_location('restart_verification_entrypoint',entry)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name]=module
        spec.loader.exec_module(module)
        config = module._admin_factory_config()
        with socket.socket() as sock:
            sock.bind(('127.0.0.1',0))
            port = sock.getsockname()[1]
        config.update(host='127.0.0.1',port=port,skills_ui_enabled=False,rag_admin_enabled=False,code_admin_enabled=False,
                      mcp_service_enabled=False,ide_enabled=False,collaboration_enabled=False,download_js_lib='enabled',
                      liquid_kernel_mode='Off',liquid_kernel_startup_policy='inherit',web_search_enabled='disabled')
        nonce = 'verification-'+os.urandom(8).hex()
        before = time.monotonic()
        pid = None
        try:
            # A failed real test must not exec a fallback server in the verifier.
            original_exec = module.os.execve
            module.os.execve = lambda *a,**k: (_ for _ in ()).throw(RuntimeError('verification restart rolled back'))
            try:
                ready = module._admin_supervised_restart(config,config,restart_nonce=nonce,restart_from_boot_id='previous-test-boot',
                    error_path=root/'restart_error.json',timeout_seconds=20)
            finally:
                module.os.execve = original_exec
            opener = build_opener(ProxyHandler({}))
            url = module._admin_restart_probe_url(config,nonce,'previous-test-boot')
            with opener.open(url,timeout=3) as response:
                health = json.load(response)
            pid = health.get('pid')
            report.update(ready=ready,seconds=round(time.monotonic()-before,2),pid_verified=bool(pid),nonce_verified=health.get('restart_verified'),
                          downloader_delay_seconds=70)
            assert ready and health.get('restart_verified') and pid
            assert report['seconds'] < 20
            report['passed']=True
        except Exception as exc:
            report.update(passed=False,error=type(exc).__name__+': '+str(exc))
            if (root/'restart_error.json').exists():
                report['restart_error']=json.loads((root/'restart_error.json').read_text())
            if (root/'restart_startup.log').exists():
                report['startup_log_tail']=(root/'restart_startup.log').read_text()[-4000:]
        finally:
            if pid:
                try:
                    os.kill(int(pid),15)
                except ProcessLookupError:
                    pass
            args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
            print(json.dumps(report,ensure_ascii=False))
    return 0 if report.get('passed') else 1


if __name__=='__main__':
    raise SystemExit(main())
