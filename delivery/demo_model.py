"""Offline protocol adapter. Deterministic extraction, NOT a generative LLM.

Implements OpenAI chat/embedding and DashScope native embedding contracts so the
real Java ingestion, pgvector retrieval and SSE pipeline can run without a key.
"""
import hashlib
import json
import math
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DIMENSIONS = 1024


def features(text):
    text = re.sub(r"\s+", "", text.lower())
    return [text[i:i + n] for n in (1, 2, 3) for i in range(max(0, len(text) - n + 1))]


def embedding(text):
    vec = [0.0] * DIMENSIONS
    for term in features(text):
        digest = hashlib.sha256(term.encode()).digest()
        vec[int.from_bytes(digest[:4], "big") % DIMENSIONS] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def answer(messages):
    user = next((str(m.get("content", "")) for m in reversed(messages) if m.get("role") == "user"), "")
    if "当前用户输入：" in user and "INTENT|" in user:
        question = user.split("当前用户输入：")[-1].strip()
        kind = "CHATTING" if question in ("你好", "您好", "谢谢", "在吗", "你是谁") else "KNOWLEDGE"
        return f"INTENT|{kind}|{question}"
    system = "\n".join(str(m.get("content", "")) for m in messages if m.get("role") == "system")
    if "【参考知识库内容】" not in system:
        return "【本地演示 · 规则提取】您好，我是人事制度检索助手。请上传制度文档后，询问请假、考勤、报销等问题。此模式不调用生成式模型。"
    context = system.split("【参考知识库内容】", 1)[1].split("回答规则：", 1)[0]
    query_features = set(t for t in features(user) if len(t) >= 2)
    candidates = []
    source = "制度文档"
    for line in context.splitlines():
        if line.startswith("【来源: "):
            source = line.removeprefix("【来源: ").removesuffix("】")
        elif line.strip() and not line.strip().startswith("#"):
            score = len(query_features & set(features(line)))
            if score:
                candidates.append((score, source, line.strip()))
    candidates.sort(key=lambda c: c[0], reverse=True)
    selected = list(dict.fromkeys((src, line) for _, src, line in candidates))[:3]
    if not selected:
        return "【本地演示 · 规则提取】未找到与问题直接匹配的制度条款，请咨询 HR 或补充相关文档。"
    return "【本地演示 · 规则提取】检索到以下原文条款：\n\n" + "\n\n".join(f"{line}\n\n来源：{src}" for src, line in selected) + "\n\n此回答为文档原文提取；复杂理解与多轮推理需接入正式模型。"


class Handler(BaseHTTPRequestHandler):
    def send_json(self, payload, status=200):
        raw = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        self.send_json({"status": "UP", "mode": "deterministic-demo", "dimensions": DIMENSIONS})

    def do_POST(self):
        try:
            if self.headers.get('Transfer-Encoding', '').lower() == 'chunked':
                chunks = []
                total = 0
                while True:
                    size = int(self.rfile.readline(256).split(b';', 1)[0].strip(), 16)
                    total += size
                    if total > 2_000_000:
                        return self.send_json({"error": "request too large"}, 413)
                    if size == 0:
                        for _ in range(100):
                            if self.rfile.readline(1024) in (b'\r\n', b'\n', b''):
                                break
                        break
                    chunks.append(self.rfile.read(size))
                    if self.rfile.read(2) != b'\r\n':
                        raise ValueError('invalid chunk delimiter')
                raw = b''.join(chunks)
            else:
                size = int(self.headers.get("Content-Length", "0"))
                if size < 0 or size > 2_000_000:
                    return self.send_json({"error": "request too large"}, 413)
                raw = self.rfile.read(size)
            body = json.loads(raw)
            if self.path.endswith("/chat/completions"):
                result = answer(body.get("messages", []))
                return self.send_json({"id": "demo-chat", "object": "chat.completion", "created": int(time.time()), "model": body.get("model", "hrm-demo-extractive"), "choices": [{"index": 0, "message": {"role": "assistant", "content": result}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 0, "completion_tokens": len(result), "total_tokens": len(result)}})
            if self.path.endswith("/embeddings"):
                texts = body.get("input", [])
                if isinstance(texts, str):
                    texts = [texts]
                return self.send_json({"object": "list", "data": [{"object": "embedding", "index": i, "embedding": embedding(t)} for i, t in enumerate(texts)], "model": body.get("model"), "usage": {"prompt_tokens": 0, "total_tokens": 0}})
            if self.path.endswith("/text-embedding/text-embedding"):
                texts = body.get("input", {}).get("texts", [])
                return self.send_json({"output": {"embeddings": [{"text_index": i, "embedding": embedding(t)} for i, t in enumerate(texts)]}, "usage": {"total_tokens": 0}, "request_id": "local-demo"})
            self.send_json({"error": "unsupported endpoint"}, 404)
        except (ValueError, TypeError, KeyError) as exc:
            self.send_json({"error": str(exc)}, 400)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8090), Handler).serve_forever()
