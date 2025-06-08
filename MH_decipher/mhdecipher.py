import numpy as np
import pandas as pd
import random
import math

alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")

def prolom_substitute(text: str, TM_ref: pd.DataFrame, iter: int, start_key: str):

    """
    Decoding ciphertext by replacing key values for dictionary values
    
    Args:
    text (str) text for decoding
    TM_ref (list) list of common bigrams from language to be decoded
    iter (int) number of iterations
    start_key (list[str]) random decoding key

    Returns:
        tuple:
            current_key (list[str]) last key which function tried to decrypt text
            best_decrypted_text (str) best decrypted text
            p_current (float) Plausibility score of the best decrypted text.
    
    """
    
    current_key = start_key

    decrypted_current = substitute_decrypt(text, "".join(current_key))
    p_current = plausibility(decrypted_current, TM_ref)

    for i in range(iter):
        candidate_key = current_key.copy()
        indices = random.sample(alphabet, 2)
        
        indice1 = candidate_key.index(indices[0])
        indice2 = candidate_key.index(indices[1])
        candidate_key[indice1], candidate_key[indice2] = candidate_key[indice2], candidate_key[indice1]
        
        decrypted_candidate = substitute_decrypt(text, "".join(candidate_key))
        p_candidate = plausibility(decrypted_candidate, TM_ref)
        q = p_candidate / p_current

        if q > 1:
            current_key = candidate_key
            p_current = p_candidate
        elif random.uniform(0, 1) < 0.01:
            current_key = candidate_key
            p_current = p_candidate
        elif (i % 50) == 0:
            print("Iteration", i, "log plausibility:", p_current)

    best_decrypted_text = substitute_decrypt(text, "".join(current_key))
    
    return (current_key, best_decrypted_text, p_current)

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

    TM = TM.div(TM.sum(axis=1).replace(0, 1), axis=0)
    
    row_sums = TM.sum(axis=1)
	print("Maximum deviation from 1:", abs(row_sums - 1).max())

    return TM

def plausibility(text: str, TM_ref: pd.DataFrame) -> float:
    """
    Calculates the log-likelihood (plausibility) of a text based on a reference transition matrix.

    Args:
        text (str): The decrypted text to evaluate.
        TM_ref (pd.DataFrame): Reference transition matrix (relative frequencies of bigrams).

    Returns:
        float: The log-likelihood score based on how well the text matches the reference matrix.
    """
    import math

    bigrams_obs = get_bigrams(text)
    TM_obs = transition_matrix(bigrams_obs)

    likelihood = 0.0
    for i in alphabet:
        for j in alphabet:
            likelihood += math.log(TM_ref.loc[i, j]) * TM_obs.loc[i, j]

    return likelihood


def substitute_encrypt(plaintext: str, key: str) -> str:
    """Encrypts the plaintext using a substitution cipher.
    
    Args:
        plaintext (str): Text to be encrypted.
        key (str): Substitution key.

    Returns:
        str: Resulting ciphertext.
    
    Raises:
        ValueError: If the key length does not match the alphabet length.
        ValueError: If there is duplicity of characters in the key.
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
        ValueError: If the key length does not match the alphabet length.
        ValueError: If there is duplicity of characters in the key.
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
