"""Package source plus built artifacts, excluding machine credentials and data."""
from pathlib import Path
import hashlib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parent / '知序人事-完整交付包.zip'
JAR = 'zhixu-server/target/zhixu-server-1.0.0.jar'
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.idea', '.vscode', '.claude', '.codegraph', 'hrm-files', 'uploads', 'logs', 'artifacts', '.worktrees'}


def include(path):
    relative = path.relative_to(ROOT)
    name = relative.as_posix()
    if any(part in SKIP_DIRS for part in relative.parts):
        return False
    if 'target' in relative.parts and name != JAR:
        return False
    if path.name.startswith('.env') and not path.name.endswith('.example'):
        return False
    if path.suffix.lower() in {'.log', '.pyc', '.rdb', '.pem', '.key', '.p12', '.pfx', '.jks', '.zip'}:
        return False
    return True


def main():
    required = {JAR, 'zhixu-admin/dist/index.html', 'start.bat', 'start.ps1', 'LICENSE', 'README.md', '使用说明.md', '交付验证报告.md', 'compose.delivery.yaml', 'delivery/vendor/minio-source.tar.gz', 'delivery/演示员工手册.md'}
    files = sorted(path for path in ROOT.rglob('*') if path.is_file() and include(path))
    names = {path.relative_to(ROOT).as_posix() for path in files}
    missing = required - names
    if missing:
        raise RuntimeError(f'Missing required delivery files: {sorted(missing)}')
    with zipfile.ZipFile(OUTPUT, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in files:
            archive.write(path, 'zhixu-hrm/' + path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(OUTPUT) as archive:
        corrupt = archive.testzip()
        if corrupt:
            raise RuntimeError(f'ZIP integrity failed: {corrupt}')
        assert not any('/.env' in name and not name.endswith('.example') for name in archive.namelist())
    checksum = hashlib.file_digest(OUTPUT.open('rb'), 'sha256').hexdigest()
    OUTPUT.with_suffix('.zip.sha256').write_text(checksum + '  ' + OUTPUT.name + '\n', encoding='utf-8')
    print(f'PASS {len(files)} files; required artifacts and ZIP integrity verified')
    print(f'{OUTPUT} ({OUTPUT.stat().st_size / 1024 / 1024:.1f} MiB)')
    print(f'SHA256 {checksum}')


if __name__ == '__main__':
    main()
