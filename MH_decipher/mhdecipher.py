import numpy as np
import pandas as pd

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

def prolom_substitute(text: str, TM_ref: np.ndarray, iter: int, start_key: str):
    pass

def get_bigrams(text: str) -> list[str]:
    bigrams_list = []
    n = len(text)
    for i in range(1, n):
        bigram = text[i - 1] + text[i]
        bigrams_list.append(bigram)
    return bigrams_list

def transition_matrix(bigrams: list[str]) -> pd.DataFrame:
    n = len(alphabet)
    TM = pd.DataFrame(
        np.zeros((n, n), dtype=int),
        index=alphabet,
        columns=alphabet
    )

    for bigram in bigrams:
        c1 = bigram[0]
        c2 = bigram[1]
        if c1 in alphabet and c2 in alphabet:
            i = alphabet.index(c1)
            j = alphabet.index(c2)
            TM.iat[i, j] += 1

    TM.replace(0, 1, inplace=True)

    return TM

def plausibility(text: str, TM_ref: np.ndarray):
    pass

def substitute_encrypt(plaintext: str, key: str) -> str:
    pass

def substitute_decrypt(ciphertext: str, key: str) -> str:
    pass