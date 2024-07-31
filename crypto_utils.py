from ecdsa import SigningKey, VerifyingKey, SECP256k1

def generate_key_pair():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    return private_key.to_string().hex(), public_key.to_string().hex()

def sign_transaction(private_key_hex, transaction_details):
    private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    signature = private_key.sign(transaction_details.encode())
    return signature.hex()

def verify_signature(public_key_hex, signature_hex, transaction_details):
    public_key = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)
    signature = bytes.fromhex(signature_hex)
    return public_key.verify(signature, transaction_details.encode())
