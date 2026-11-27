"""Adapter model và chế độ preview.

call_model trả text/model/tokens_in/tokens_out, giữ @model_call của starter.
Provider fake dùng quy tắc, token 0; provider thật đọc usage API, không ước lượng
và không thay lỗi API bằng dữ liệu giả. Key chỉ đọc từ môi trường/.env local."""
import json
import os
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        from tools import preview_classify
        message = json.loads(user)["message"]
        return {"text": json.dumps(preview_classify(message), ensure_ascii=False),
                "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if MODEL_PROVIDER not in ("openai", "openrouter"):
        raise RuntimeError("Provider chưa được hỗ trợ; chọn openai hoặc openrouter trong .env")
    if not API_KEY or not MODEL_NAME:
        raise RuntimeError("Chưa điền API_KEY và MODEL_NAME trong .env local")
    endpoint = {"openai": "https://api.openai.com/v1/chat/completions",
                "openrouter": "https://openrouter.ai/api/v1/chat/completions"}[MODEL_PROVIDER]
    body = {"model": MODEL_NAME, "temperature": 0,
            "max_tokens": min(800, max(64, int(os.environ.get("MAX_OUTPUT_TOKENS", "300")))),
            "response_format": {"type": "json_object"},
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    request = urllib.request.Request(endpoint, data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json", "Authorization": "Bearer " + API_KEY})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Model API HTTP {exc.code}; kiểm key, credit hoặc quota. Không chuyển lỗi thành kết quả giả.") from None
    except (urllib.error.URLError, TimeoutError):
        raise RuntimeError("Không kết nối được model API; kiểm mạng rồi chạy lại thành lượt mới.") from None
    usage = result.get("usage", {})
    if not all(isinstance(usage.get(k), int) for k in ("prompt_tokens", "completion_tokens")):
        raise RuntimeError("API không trả usage hợp lệ; không ước lượng token thay thế")
    return {"text": result["choices"][0]["message"]["content"],
            "model": result.get("model") or MODEL_NAME,
            "tokens_in": usage["prompt_tokens"], "tokens_out": usage["completion_tokens"]}
