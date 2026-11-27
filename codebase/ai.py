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


def _api_error_code(exc: urllib.error.HTTPError):
    try:
        payload = json.loads(exc.read().decode("utf-8"))
    except (AttributeError, UnicodeDecodeError, ValueError):
        return None
    detail = payload.get("error", {}) if isinstance(payload, dict) else {}
    if not isinstance(detail, dict):
        return None
    code = detail.get("code") or detail.get("type")
    return code if isinstance(code, str) and len(code) <= 80 else None


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        from tools import preview_classify
        payload = json.loads(user)
        return {"text": json.dumps(preview_classify(payload['message'], payload.get('order')), ensure_ascii=False),
                "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if MODEL_PROVIDER not in ("openai", "openrouter"):
        raise RuntimeError("Provider chưa được hỗ trợ; chọn openai hoặc openrouter trong .env")
    if not API_KEY or not MODEL_NAME:
        raise RuntimeError("Chưa điền API_KEY và MODEL_NAME trong .env local")
    endpoint = {"openai": "https://api.openai.com/v1/chat/completions",
                "openrouter": "https://openrouter.ai/api/v1/chat/completions"}[MODEL_PROVIDER]
    try:
        max_output_tokens = int(os.environ.get("MAX_OUTPUT_TOKENS", "300"))
    except ValueError:
        raise RuntimeError("MAX_OUTPUT_TOKENS phải là số nguyên") from None
    body = {"model": MODEL_NAME, "temperature": 0,
            "max_tokens": min(800, max(64, max_output_tokens)),
            "response_format": {"type": "json_object"},
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    request = urllib.request.Request(endpoint, data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json", "Authorization": "Bearer " + API_KEY})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        error_code = _api_error_code(exc)
        suffix = f" ({error_code})" if error_code else ""
        raise RuntimeError(f"Model API HTTP {exc.code}{suffix}; kiểm key, credit hoặc quota. Không chuyển lỗi thành kết quả giả.") from None
    except (urllib.error.URLError, TimeoutError):
        raise RuntimeError("Không kết nối được model API; kiểm mạng rồi chạy lại thành lượt mới.") from None
    if not isinstance(result, dict):
        raise RuntimeError("API trả về dữ liệu không hợp lệ; không tạo kết quả giả")
    usage = result.get("usage", {})
    if not all(isinstance(usage.get(k), int) for k in ("prompt_tokens", "completion_tokens")):
        raise RuntimeError("API không trả usage hợp lệ; không ước lượng token thay thế")
    choices = result.get("choices")
    if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
        raise RuntimeError("API không trả choices hợp lệ; không tạo kết quả giả")
    message = choices[0].get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise RuntimeError("API không trả nội dung hợp lệ; không tạo kết quả giả")
    return {"text": result["choices"][0]["message"]["content"],
            "model": result.get("model") or MODEL_NAME,
            "tokens_in": usage["prompt_tokens"], "tokens_out": usage["completion_tokens"]}
