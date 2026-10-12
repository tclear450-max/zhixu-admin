import json
import http.client
import math
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from demo_model import Handler, answer, embedding


class DemoModelTests(unittest.TestCase):
    def test_vectors_are_normalized_stable_and_have_1024_dimensions(self):
        vec = embedding("请假流程")
        self.assertEqual(len(vec), 1024)
        self.assertEqual(vec, embedding("请假流程"))
        self.assertAlmostEqual(math.sqrt(sum(v * v for v in vec)), 1.0)

    def test_related_document_scores_above_unrelated_document(self):
        query = embedding("报销材料")
        related = embedding("报销材料需要发票和付款凭证")
        unrelated = embedding("服务器数据库备份")
        dot = lambda a, b: sum(x * y for x, y in zip(a, b))
        self.assertGreater(dot(query, related), dot(query, unrelated))

    def test_answer_preserves_evidence_and_marks_demo(self):
        messages = [{"role": "system", "content": "【参考知识库内容】\n【来源: 员工手册】\n报销需要发票和付款凭证。\n回答规则：不得编造"}, {"role": "user", "content": "报销需要什么？"}]
        result = answer(messages)
        self.assertIn("本地演示", result)
        self.assertIn("报销需要发票和付款凭证。", result)
        self.assertIn("来源：员工手册", result)

    def test_unrelated_evidence_does_not_fabricate_an_answer(self):
        result = answer([{"role": "system", "content": "【参考知识库内容】\n【来源: 手册】\n九点上班。\n回答规则："}, {"role": "user", "content": "报销材料"}])
        self.assertIn("未找到", result)

    def test_intent_contract(self):
        self.assertEqual(answer([{"role": "user", "content": "INTENT|\n当前用户输入：\n你好"}]), "INTENT|CHATTING|你好")
        self.assertEqual(answer([{"role": "user", "content": "INTENT|\n当前用户输入：\n报销材料"}]), "INTENT|KNOWLEDGE|报销材料")

    def test_http_supports_both_embedding_protocols(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f"http://127.0.0.1:{server.server_port}"
            def post(path, body):
                req = urllib.request.Request(base + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
                with urllib.request.urlopen(req) as response:
                    return json.load(response)
            native = post('/api/v1/services/embeddings/text-embedding/text-embedding', {"input": {"texts": ["请假", "报销"]}})
            openai = post('/compatible-mode/v1/embeddings', {"input": ["请假", "报销"]})
            self.assertEqual(native['output']['embeddings'][1]['embedding'], openai['data'][1]['embedding'])
            self.assertEqual(len(openai['data'][1]['embedding']), 1024)
            connection = http.client.HTTPConnection('127.0.0.1', server.server_port)
            payload = json.dumps({'messages': [{'role': 'user', 'content': '你好'}]}).encode()
            connection.request('POST', '/compatible-mode/v1/chat/completions', body=iter([payload[:10], payload[10:]]), headers={'Content-Type': 'application/json'}, encode_chunked=True)
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            self.assertIn('本地演示', json.load(response)['choices'][0]['message']['content'])
            connection.close()
        finally:
            server.shutdown()
            server.server_close()


if __name__ == '__main__':
    unittest.main()
