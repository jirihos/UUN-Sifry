import numpy as np

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

def prolom_substitute(text: str, TM_ref: np.ndarray, iter: int, start_key: str):
    pass

def get_bigrams(text: str) -> list[str]:
    pass

def transition_matrix(bigrams: list[str]) -> np.ndarray:
    pass

def plausibility(text: str, TM_ref: np.ndarray):
    pass

def substitute_encrypt(plaintext: str, key: str) -> str:
    pass

def substitute_decrypt(ciphertext: str, key: str) -> str:
    pass