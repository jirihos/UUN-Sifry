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

    """
    Coding plaintext by replacing dictionary values for key values
    
    Args:
    plaintext (str): Input string for coding
    key (str): key for coding 

    returns:
    string (encrypted_text)
    """

    mapping = {}
    encrypted_text = ""
    
    key = key.upper()
    plaintext = plaintext.upper() 

    if len(key) != len(alphabet): # error wrong key length compared to "alphabet" length
        raise ValueError("Wrong key length")

    for keyCharacter in key: # error if any duplicity in key (decoding with duplicity in "key" is not possible)
        if key.count(keyCharacter) > 1:
            raise ValueError("Duplicity in key, coding is not possible")

    for i in range(len(alphabet)): # map "key" values to "dictionary" 
        mapping[alphabet[i]] = key[i]

    for character in plaintext: # add character to "encrypted_text"
        if character in mapping: # if exist in "mapping"
            encrypted_text += mapping[character]
        else:
           encrypted_text += character

    return encrypted_text

def substitute_decrypt(ciphertext: str, key: str) -> str:

    """
    Decoding ciphertext by replacing key values for dictionary values
    
    Args:
    ciphertext (str): Input string for decoding
    key (str): key for decoding 

    returns:
    string (plaintext)
    """

    reverse_mapping = {}
    decrypted_text = ""
    
    key = key.upper()
    ciphertext = ciphertext.upper() 

    if len(key) != len(alphabet): # error wrong key length compared to "alphabet" length
        raise ValueError("Wrong key length")

    for keyCharacter in key: # error if any duplicity in key (decoding with duplicity in "key" is not possible)
        if key.count(keyCharacter) > 1:
            raise ValueError("Duplicity in key, decoding is not possible")

    for i in range(len(alphabet)): # map dictionary to key values
        reverse_mapping[key[i]] = alphabet[i]

    for character in ciphertext: # add character to "decrypted_text"
        if character in reverse_mapping: # if exist in "reverse_mapping"
            decrypted_text += reverse_mapping[character]
        else:
           decrypted_text += character

    return decrypted_text
