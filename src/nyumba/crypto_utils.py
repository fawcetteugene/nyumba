import os
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def get_or_create_key(passphrase: str = None) -> Fernet:
    key_dir = Path.home() / ".nyumba"
    key_dir.mkdir(exist_ok=True)
    key_file = key_dir / "key"

    if passphrase is None:
        passphrase = os.environ.get("NYUMBA_PASSPHRASE")
        if not passphrase:
            # No passphrase, use a random key (store it unencrypted)
            if key_file.exists():
                with open(key_file, "rb") as f:
                    key = f.read()
            else:
                key = Fernet.generate_key()
                with open(key_file, "wb") as f:
                    f.write(key)
            return Fernet(key)

    # Derive key from passphrase with salt
    salt_file = key_dir / "salt"
    if salt_file.exists():
        salt = salt_file.read_bytes()
    else:
        salt = os.urandom(16)
        salt_file.write_bytes(salt)

    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return Fernet(key)

def encrypt_text(text: str, fernet: Fernet) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt_text(encrypted: str, fernet: Fernet) -> str:
    return fernet.decrypt(encrypted.encode()).decode()
