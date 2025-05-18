import numpy as np
import pandas as pd

alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")

def prolom_substitute(text: str, TM_ref: pd.DataFrame, iter: int, start_key: str):
    pass

def get_bigrams(text: str) -> list[str]:
    """
    Generates a list of bigrams (two-character combinations) from the input string.

    Args:
        text (str): The input string from which bigrams will be generated.

    Returns:
        list[str]: A list of bigrams extracted from the input string. Each bigram is a pair of consecutive characters.

    Example:
        >>> get_bigrams("hello")
        ['he', 'el', 'll', 'lo']
    """
    bigrams_list = []
    n = len(text)
    for i in range(1, n):
        bigram = text[i - 1] + text[i]
        bigrams_list.append(bigram)
    return bigrams_list


def transition_matrix(bigrams: list[str]) -> pd.DataFrame:
    """
    Constructs a relative transition matrix from a list of bigrams.

    The matrix counts normalized (relative) frequencies of transitions from one character
    to another based on the provided bigrams. If a character in a bigram is not found
    in the global `alphabet`, that bigram is ignored. Zeros are replaced by ones before
    normalization to avoid division by zero.

    Args:
        bigrams (list[str]): A list of bigrams (two-character strings) from which to build the transition matrix.

    Returns:
        pd.DataFrame: A square pandas DataFrame with rows and columns labeled by characters from `alphabet`.
                      Each cell (i, j) contains the relative frequency of transitions from character `alphabet[i]`
                      to `alphabet[j`]`, i.e. probabilities summing to 1 per row.

    Raises:
        NameError: If the global variable `alphabet` is not defined.

    Example:
        >>> alphabet = list("abc")
        >>> transition_matrix(['ab', 'bc', 'ca', 'ab'])
               a         b         c
        a  0.25      0.50      0.25
        b  0.25      0.25      0.50
        c  0.25      0.25      0.50
    """
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

    TM = TM.div(TM.sum(axis=1), axis=0)

    return TM

def plausibility(text: str, TM_ref: pd.DataFrame):
    pass

def substitute_encrypt(plaintext: str, key: str) -> str:
    """Encrypts the plaintext using a substitution cipher.
    
    Args:
        plaintext (str): Text to be encrypted.
        key (str): Substitution key.

    Returns:
        str: Resulting ciphertext.
    
    Raises:
        TODO
    """

    if len(key) != len(alphabet): # error wrong key length compared to "alphabet" length
        raise ValueError("Wrong key length")

    for keyCharacter in key: # error if any duplicity in key (decoding with duplicity in "key" is not possible)
        if key.count(keyCharacter) > 1:
            raise ValueError("Duplicity in key, coding is not possible")
    
    mapping = {}
    for i in range(len(alphabet)): # map "key" values to "dictionary" 
        mapping[alphabet[i]] = key[i]

    encrypted_text = ""
    for character in plaintext: # add character to "encrypted_text"
        if character in mapping: # if exist in "mapping"
            encrypted_text += mapping[character]
        else:
           encrypted_text += character

    return encrypted_text

def substitute_decrypt(ciphertext: str, key: str) -> str:
    """Decrypts the ciphertext using a substitution cipher.
    
    Args:
        ciphertext (str): Text to be decrypted.
        key (str): Substitution key.

    Returns:
        str: Resulting plaintext.
    
    Raises:
        TODO
    """

    if len(key) != len(alphabet): # error wrong key length compared to "alphabet" length
        raise ValueError("Wrong key length")

    for keyCharacter in key: # error if any duplicity in key (decoding with duplicity in "key" is not possible)
        if key.count(keyCharacter) > 1:
            raise ValueError("Duplicity in key, decoding is not possible")

    reverse_mapping = {}
    for i in range(len(alphabet)): # map dictionary to key values
        reverse_mapping[key[i]] = alphabet[i]

    decrypted_text = ""
    for character in ciphertext: # add character to "decrypted_text"
        if character in reverse_mapping: # if exist in "reverse_mapping"
            decrypted_text += reverse_mapping[character]
        else:
           decrypted_text += character

    return decrypted_text
