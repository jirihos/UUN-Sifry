"""
Substitution Cipher Module

Provides basic functions for encryption and decryption using a substitution cipher
based on a fixed alphabet (A–Z and underscore).
"""

ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")

def substitute_encrypt(plaintext: str, key: list[str]) -> str:
    """
    Encrypts the input text using a substitution cipher.

    Args:
        plaintext (str): Text to encrypt using only uppercase letters and underscores.
        key (list[str]): A permutation of the alphabet used as the encryption key.

    Returns:
        str: Encrypted ciphertext.
    """
    mapping = {ALPHABET[i]: key[i] for i in range(len(ALPHABET))}
    return ''.join(mapping.get(c, c) for c in plaintext)


def substitute_decrypt(ciphertext: str, key: list[str]) -> str:
    """
    Decrypts a ciphertext using the inverse of the substitution cipher.

    Args:
        ciphertext (str): Encrypted text to decrypt.
        key (list[str]): The same permutation key used for encryption.

    Returns:
        str: Decrypted original text.
    """
    reverse_mapping = {key[i]: ALPHABET[i] for i in range(len(ALPHABET))}
    return ''.join(reverse_mapping.get(c, c) for c in ciphertext)


if __name__ == "__main__":
    # Example usage (for demonstration only)
    test_key = list("DEFGHIJKLMNOPQRSTUVWXYZ_ABC")  # Shifted by 3
    sample_text = "BYL_POZDNI_VECER"
    
    encrypted = substitute_encrypt(sample_text, test_key)
    decrypted = substitute_decrypt(encrypted, test_key)

    print("Original:", sample_text)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
