"""Exercise the real local services; leaves an approved request and demo handbook.
Requires Docker CLI and the running delivery stack. Uses demo accounts only.
"""
import datetime
import hashlib
import http.cookiejar
import json
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://localhost:18080/api'
CHECKS = []


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)
    print('PASS ' + label, flush=True)


def docker(service, *args):
    return subprocess.check_output(['docker', 'compose', '-f', str(ROOT / 'compose.delivery.yaml'), 'exec', '-T', service, *args], cwd=ROOT).decode().strip()


class Client:
    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def raw(self, path, method='GET', data=None, headers=None):
        request = urllib.request.Request(BASE + path, data=data, method=method, headers=headers or {})
        with self.opener.open(request, timeout=90) as response:
            return response.read(), response.headers

    def api(self, path, method='GET', body=None):
        raw, _ = self.raw(path, method, json.dumps(body, ensure_ascii=False).encode() if body is not None else None, {'Content-Type': 'application/json'})
        result = json.loads(raw)
        if result.get('code') != 200:
            raise AssertionError(f'{method} {path}: {result}')
        return result.get('data')

    def login(self, account):
        raw, _ = self.raw('/validate/code')
        check(account + ' captcha JPEG', raw[:2] == b'\xff\xd8')
        code = json.loads(docker('redis', 'redis-cli', '--raw', 'get', 'validate:code'))
        staff = self.api('/login/' + str(code), 'POST', {'code': account, 'password': 'Zx@123456'})
        return staff


def upload_handbook(admin):
    path = ROOT / 'delivery' / '演示员工手册.md'
    content = path.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    info = admin.api('/docs/upload/init', 'POST', {'fileName': path.name, 'fileExt': 'md', 'fileSize': len(content), 'fileHash': digest, 'chunkSize': 5 * 1024 * 1024, 'ingest': True})
    if info.get('instantUpload'):
        document_id = info['id']
    else:
        upload_id = info['uploadId']
        boundary = 'zhixu-' + uuid.uuid4().hex
        fields = {'uploadId': upload_id, 'chunkIndex': '0', 'chunkHash': digest}
        body = b''
        for key, value in fields.items():
            body += f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode()
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="handbook.md"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode() + content + f'\r\n--{boundary}--\r\n'.encode()
        raw, _ = admin.raw('/docs/upload/chunks', 'POST', body, {'Content-Type': 'multipart/form-data; boundary=' + boundary})
        check('chunk upload to object storage', json.loads(raw)['code'] == 200)
        info = admin.api('/docs/upload/' + upload_id + '/complete?ingest=true', 'POST', {})
        document_id = info['documentId']
    for _ in range(40):
        doc = admin.api('/docs/' + str(document_id))
        if doc['kbStatus'] == 'READY':
            check('document parsing and vector indexing', doc.get('chunkCount', 0) > 0)
            return document_id
        if doc['kbStatus'] == 'FAILED':
            raise AssertionError(f'ingestion failed: {doc}')
        time.sleep(0.5)
    raise AssertionError('document indexing timed out')


def run():
    anonymous = Client()
    raw, _ = anonymous.raw('/actuator/health')
    check('backend health', json.loads(raw)['status'] == 'UP')
    try:
        raw, _ = anonymous.raw('/staff')
        check('anonymous access denied', json.loads(raw).get('code') in (401, 403, 1200, 1300))
    except urllib.error.HTTPError as exc:
        check('anonymous access denied', exc.code in (401, 403))
    admin = Client()
    admin.login('admin')
    check('product branding and demo mode', admin.api('/product/info')['name'] == '知序人事')
    cookie = next(c for c in admin.jar if c.name == 'refreshToken')
    check('refresh cookie proxy path', cookie.path == '/api/refresh')
    admin.api('/refresh', 'POST', {})
    check('refresh token round trip', True)
    check('home data', admin.api('/home/count') is not None)
    check('staff list', admin.api('/staff?current=1&size=10')['total'] > 0)
    check('salary list', admin.api('/salary?current=1&size=10') is not None)
    doc_id = upload_handbook(admin)
    raw, _ = admin.raw('/chat/chat', 'POST', json.dumps({'message': '报销需要哪些材料？'}, ensure_ascii=False).encode(), {'Content-Type': 'application/json'})
    stream = raw.decode()
    check('SSE completion and document citation', 'event:citations' in stream and 'event:meta' in stream and str(doc_id) in stream)
    tokens = []
    for event in stream.replace('\r\n', '\n').split('\n\n'):
        if event.startswith('event:token\n'):
            payload = event.split('data:', 1)[1]
            try:
                token = json.loads(payload)
            except json.JSONDecodeError:
                token = payload
            tokens.append(token)
    answer = ''.join(tokens)
    check('retrieved source text appears in answer', '发票' in answer and '本地演示' in answer)
    sessions = admin.api('/chat/conversations')
    check('conversation persisted', len(sessions) > 0)
    messages = admin.api('/chat/conversations/' + str(sessions[0]['id']) + '/messages')['records']
    check('question and answer persisted', len(messages) >= 2)
    employee = Client()
    staff = employee.login('staff_3')
    future = (datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))) + datetime.timedelta(days=7)).date()
    while future.weekday() >= 5:
        future += datetime.timedelta(days=1)
    existing = employee.api('/staff-leave/staff?id=' + str(staff['id']))['list']
    pending = [r['staffLeave'] for r in existing if r['staffLeave']['status'] == '待审核' and r['staffLeave']['remark'] == '知序端到端演示申请']
    if not pending:
        employee.api('/staff-leave/apply', 'POST', {'staffId': staff['id'], 'startDate': future.isoformat(), 'days': 1, 'typeNum': '事假', 'status': '待审核', 'remark': '知序端到端演示申请'})
    leave = employee.api('/staff-leave/staff?id=' + str(staff['id']))['list'][0]['staffLeave']
    leave_id = leave['id']
    check('leave application starts Flowable', leave['status'] == '待审核')
    for account, label in [('staff_9', 'HR approval'), ('staff_2', 'manager approval')]:
        approver = Client()
        approver.login(account)
        approver.api('/staff-leave/claim', 'POST', {'id': leave_id, 'status': '审核中'})
        approver.api('/staff-leave/complete', 'POST', {'id': leave_id, 'status': '审核通过', 'auditRemark': '演示通过'})
        check(label, True)
    leave = employee.api('/staff-leave/' + str(leave_id))
    check('leave approved state persisted', leave['status'] == '审核通过')
    future_leave = employee.api('/home/attendance?id=' + str(staff['id']) + '&month=' + future.strftime('%Y%m'))
    check('approved leave updates attendance', future_leave[future.day - 1]['message'] == '休假')
    report = {'checks': CHECKS, 'passed': len(CHECKS), 'documentId': doc_id, 'leaveId': leave_id, 'externalModelTested': False}
    (ROOT / 'delivery' / 'smoke-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'ALL {len(CHECKS)} CHECKS PASSED')


if __name__ == '__main__':
    run()
