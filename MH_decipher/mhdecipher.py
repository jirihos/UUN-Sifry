import numpy as np
import pandas as pd
import random

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

def prolom_substitute(text: str, TM_ref: pd.DataFrame, iter: int, start_key: str):
    """Attempts to decode the text using the Metropolis-Hastings (M-H) algorithm
    
    Args:
        text (str): Ciphertext for decoding.
        TM_ref (pd.DataFrame): Reference relative transition matrix.
        iter (int): The number of iterations.
        start_key (str): Initial key.

    Returns:
        A tuple (key, decrypted_text, p), where key is the best found key,
        decrypted_text is the text decrypted using the key, and p is
        the plausibility of the decrypted text.
    """
    
    current_key = start_key

    decrypted_current = substitute_decrypt(text, current_key)
    p_current = plausibility(decrypted_current, TM_ref)

    best_key = current_key
    p_best = p_current

    for i in range(iter):
        candidate_key = current_key

        # Swap 2 letters
        index1, index2 = random.sample(range(len(alphabet)), 2)
        candidate_key = list(candidate_key)
        candidate_key[index1], candidate_key[index2] = candidate_key[index2], candidate_key[index1]
        candidate_key = "".join(candidate_key)

        # Calculate the plausibility
        decrypted_candidate = substitute_decrypt(text, candidate_key)
        p_candidate = plausibility(decrypted_candidate, TM_ref)
        q = p_current / p_candidate

        if q > 1: # accept the candidate key, if its plausibility is higher than the plausibility of the current key
            current_key = candidate_key
            p_current = p_candidate
        elif random.uniform(0, 1) < 0.001: # small chance of accepting the candidate key even if its plausibility is lower
            current_key = candidate_key
            p_current = p_candidate

        # Remember the best key
        if p_current > p_best:
            best_key = current_key
            p_best = p_current

        # Log progress
        if (i % 50) == 0:
            print("Iteration", i, "log plausibility:", p_current)

    best_decrypted_text = substitute_decrypt(text, best_key)

    return (best_key, best_decrypted_text, p_best)


def get_bigrams(text: str) -> list[str]:
    """Generates a list of bigrams (two-character combinations) from the input string.

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
    """Constructs a relative transition matrix from a list of bigrams.

    The matrix counts normalized (relative) frequencies of transitions from one character
    to another based on the provided bigrams. If a character in a bigram is not found
    in the global `alphabet`, that bigram is ignored.

    Args:
        bigrams (list[str]): A list of bigrams (two-character strings) from which to build the transition matrix.

    Returns:
        pd.DataFrame: A square pandas DataFrame with rows and columns labeled by characters from `alphabet`.
                      Each cell (i, j) contains the relative frequency of transitions from character `alphabet[i]`
                      to `alphabet[j]`.
	"""

    n = len(alphabet)
    arr = np.zeros((n, n), dtype=int)

    # Build the absolute transition matrix
    for bigram in bigrams:
        c1 = bigram[0]
        c2 = bigram[1]
        if c1 in alphabet and c2 in alphabet:
            i = alphabet.index(c1)
            j = alphabet.index(c2)
            arr[i, j] += 1

    alphabet_list = list(alphabet)
    TM = pd.DataFrame(
        arr,
        index=alphabet_list,
        columns=alphabet_list
    )

    # Replace zeros with ones
    TM.replace(0, 1, inplace=True)

    # Convert to relative transition matrix
    TM = TM.div(TM.sum().sum())

    return TM


def plausibility(text: str, TM_ref: pd.DataFrame) -> float:
    """Calculates the likelihood (plausibility) of a text based on a reference transition matrix.

    Args:
        text (str): The text to evaluate.
        TM_ref (pd.DataFrame): Reference transition matrix.

    Returns:
        float: The likelihood score based on how well the text matches the reference matrix.
    """

    bigrams_obs = get_bigrams(text)
    TM_obs = transition_matrix(bigrams_obs)

    TM_ref = np.asarray(TM_ref)
    TM_obs = np.asarray(TM_obs)
    likelihood = np.sum(np.log(TM_ref) * TM_obs)

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

    if len(key) != len(alphabet):
        raise ValueError("Wrong key length")

    for keyCharacter in key: # error if any duplicity in key
        if key.count(keyCharacter) > 1:
            raise ValueError("Duplicity in key, coding is not possible")

    mapping = {}
    for i in range(len(alphabet)):
        mapping[alphabet[i]] = key[i]

    encrypted_text = ""
    for character in plaintext:
        if character in mapping:
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

    if len(key) != len(alphabet):
        raise ValueError("Wrong key length")

    for keyCharacter in key: # error if any duplicity in key
        if key.count(keyCharacter) > 1:
            raise ValueError("Duplicity in key, decoding is not possible")

    reverse_mapping = {}
    for i in range(len(alphabet)):
        reverse_mapping[key[i]] = alphabet[i]

    decrypted_text = ""
    for character in ciphertext:
        if character in reverse_mapping:
            decrypted_text += reverse_mapping[character]
        else:
            decrypted_text += character

    return decrypted_text
