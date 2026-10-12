"""Verify first-time MySQL initialization in a disposable container, no host ports."""
from pathlib import Path
import subprocess
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
name = 'zhixu-init-check-' + uuid.uuid4().hex[:12]
args = ['docker', 'run', '--rm', '-d', '--name', name, '-e', 'MYSQL_ROOT_PASSWORD=local-initialization-check']
for source, target in [(ROOT / 'delivery/00-databases.sql', '/docker-entrypoint-initdb.d/00-databases.sql'), (ROOT / 'db/mysql/hrm.sql', '/seed/hrm.sql'), (ROOT / 'delivery/demo.sql', '/seed/demo.sql')]:
    args.extend(['--mount', f'type=bind,source={source},target={target},readonly'])
args.append('mysql:8.1.0')
container_id = subprocess.check_output(args).decode().strip()
try:
    for _ in range(75):
        result = subprocess.run(['docker', 'exec', name, 'sh', '-c', 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql --default-character-set=utf8mb4 -uroot -N hrm -e "SELECT version FROM zhixu_delivery_meta WHERE id=1; SELECT name FROM sys_staff WHERE id=1; SELECT COUNT(*) FROM sal_salary;"'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            lines = result.stdout.strip().splitlines()
            assert lines[0] == '1.0.0' and lines[1] == '知序管理员' and int(lines[2]) > 0, result.stdout
            print('PASS fresh database schema, complete demo initialization marker, brand seed and current-month salaries')
            break
        time.sleep(1)
    else:
        raise RuntimeError(subprocess.check_output(['docker', 'logs', name]).decode())
finally:
    subprocess.run(['docker', 'stop', container_id], check=True, stdout=subprocess.DEVNULL)
