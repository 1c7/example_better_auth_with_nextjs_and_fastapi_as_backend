import hashlib
import hmac
import base64
from urllib.parse import unquote

def verify_session_token(hmac_key: str, session_token: str) -> bool:
    """
    验证 session token 的签名

    Args:
        hmac_key: 用于签名的 HMAC 密钥。
        session_token: 待验证的 session token 字符串，格式为 "data.signature"。

    Returns:
        True 签名有效，False 签名无效。
    """
    try:
        parts = session_token.split('.')
        if len(parts) != 2:
            print("Error: Invalid session token format.")
            return False

        data_encoded = parts[0]
        signature_encoded = parts[1]

        # URL 解码 data 和 signature
        data = unquote(data_encoded)
        signature_expected_bytes = base64.urlsafe_b64decode(unquote(signature_encoded) + '=' * (4 - len(unquote(signature_encoded)) % 4))

        # 使用 HMAC-SHA256 计算 data 的签名
        hmac_obj = hmac.new(hmac_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256)
        signature_actual_bytes = hmac_obj.digest()

        # 对比计算出的签名和 token 中的签名
        return hmac.compare_digest(signature_actual_bytes, signature_expected_bytes)

    except Exception as e:
        print(f"An error occurred during verification: {e}")
        return False

def main():
    hmac_key = "LcWr9US2bCHDNckxuXKJRAXLOr0a2d6c"  # 请替换为你的实际密钥

    # 来自 Cookie 里的 `better-auth.session_token` 的值
    session_token = "6DLBcOCD6gxRQrKGHPZzShSNpXNyBPHX.BLH7eO3aRjS%2B3wWuoetnhkt6ix6jVQcn0A1aAYWcVTc%3D"

    is_valid = verify_session_token(hmac_key, session_token)

    if is_valid:
        print("Session token is valid.")
    else:
        print("Session token is invalid.")

if __name__ == "__main__":
    main()