# kms_utils.py
import os
import boto3
from base64 import b64encode, b64decode

KMS_KEY_ID = os.environ.get("KMS_KEY_ID")  # set in env (e.g., arn:aws:kms:...:key/xxxx)

kms = boto3.client("kms", region_name=os.environ.get("AWS_REGION", "us-east-1"))

def encrypt_bytes(plaintext_bytes: bytes) -> str:
    """
    Returns base64-encoded ciphertext.
    """
    if not KMS_KEY_ID:
        raise RuntimeError("KMS_KEY_ID not set")
    resp = kms.encrypt(KeyId=KMS_KEY_ID, Plaintext=plaintext_bytes)
    ct = resp["CiphertextBlob"]
    return b64encode(ct).decode('utf-8')

def decrypt_bytes(ct_b64: str) -> bytes:
    ct = b64decode(ct_b64)
    resp = kms.decrypt(CiphertextBlob=ct)
    return resp["Plaintext"]
