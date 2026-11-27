"""Local-only demo server. Defaults to preview mode and never executes a transaction."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse
from ai import MODEL_PROVIDER
from agent import answer
import tracing

ROOT = Path(__file__).resolve().parents[1]


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body, content_type="application/json; charset=utf-8"):
        raw = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/":
            self.reply(200, (ROOT / "codebase/index.html").read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/bootstrap":
            orders = json.loads((ROOT / "data/orders.json").read_text(encoding="utf-8"))["orders"]
            policies = json.loads((ROOT / "data/policies.json").read_text(encoding="utf-8"))["policies"]
            count = json.loads((ROOT / "evidence/review-sources.json").read_text(encoding="utf-8"))["count"]
            self.reply(200, {"mode": "preview" if MODEL_PROVIDER == "fake" else "ai", "orders": orders,
                             "policies": policies, "review_count": count})
        else:
            self.reply(404, {"error": "Không có đường dẫn này"})

    def do_POST(self):
        if self.path != "/api/ask":
            self.reply(404, {"error": "Không có đường dẫn này"})
            return
        origin = self.headers.get("Origin")
        if origin and urlparse(origin).netloc != self.headers.get("Host"):
            self.reply(403, {"error": "Chỉ nhận thao tác từ giao diện local"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 12000:
                self.reply(413, {"error": "Nội dung quá lớn hoặc rỗng"})
                return
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict) or not isinstance(data.get("text"), str):
                raise ValueError("Nhập câu khiếu nại hợp lệ")
            tracing.begin("web-demo")
            try:
                result = json.loads(answer(data["text"])["output"])
            finally:
                summary, _ = tracing.end()
            self.reply(200, {"result": result, "usage": {"model_calls": summary["model_calls"],
                              "tokens_in": summary["tokens_in"], "tokens_out": summary["tokens_out"]}})
        except (ValueError, TypeError):
            self.reply(400, {"error": "Nhập nội dung từ 1 đến 2.000 ký tự và chọn đơn cần kiểm tra"})
        except Exception as exc:
            # Chỉ in loại lỗi và thông báo (không in nội dung khách nhập) để biết sai key, quota hay mạng.
            print("[lỗi /api/ask] %s: %s" % (type(exc).__name__, str(exc)[:200]), file=sys.stderr, flush=True)
            hint = str(exc)[:200].rstrip(". ") + "." if isinstance(exc, RuntimeError) else "Kiểm cấu hình/model hoặc thử lại."
            self.reply(503, {"error": "Chưa xử lý được yêu cầu. " + hint + " Không có hành động tài chính nào được thực hiện."})

    def log_message(self, format, *args):
        return  # Do not persist customer input or headers.


def main():
    port = int(os.environ.get("APP_PORT", "18115"))
    print(f"AI1 Support: http://127.0.0.1:{port} · {'PREVIEW — chưa gọi AI' if MODEL_PROVIDER == 'fake' else 'chế độ AI (' + MODEL_PROVIDER + ') — chưa kiểm kết nối'}", flush=True)
    server = HTTPServer(("127.0.0.1", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
