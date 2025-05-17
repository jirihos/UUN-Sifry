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

plaintext = ("99_VOZEM_DO_NEHO_A_ZAS_MNE_BEZI_DO_CESTY__ZACHVELA_SE_TAK_KUDY_VPRAVO_NEBO_VLEVO_TEDY_JE_KONEC_PTAL_SE_TISE_POKYVLA_HLAVOU_TEDY_JE_KONEC_OTEVREL_DVIRKA_VYSKOCIL_Z_VOZU_A_POSTAVIL_SE_PRED_KOLA_JED_REKL_CHRAPTIVE_POJEDES_PRESE_MNE_UJELA_S_VOZEM_DVA_KROKY_ZPET_POJD_MUSIME_DAL_DOVEZU_TE_ASPON_BLIZ_K_HRANICIM_KAM_CHCES_ZPATKY_SKRIPEL_ZUBY_ZPATKY_S_TEBOU_SE_MNOU_NENI_ANI_DOPREDU_ANI_ZPATKY_COPAK_MI_NEROZUMIS_MUSIM_TO_UDELAT_ABYS_VIDEL_ABY_BYLO_JISTO_ZE_JSEM_TE_MELA_RADA_MYSLIS_ZE_BYCH_MOHLA_JESTE_JEDNOU_SLYSET_COS_MI_REKL_ZPATKY_NEMUZES_BUD_BYS_MUSEL_VYDAT_TO_CO_NECHCES_A_NESMIS_NEBO_BY_TE_ODVEZLI_A_JA__SPUSTILA_RUCE_DO_KLINA_VIDIS_I_NA_TO_JSEM_MYSLELA_ZE_BYCH_SLA_S_TEBOU_DOPREDU_DOVEDLA_BYCH_TO_DOVEDLA_BYCH_TO_JISTE_ALE__TY_JSI_TAM_NEKDE_ZASNOUBEN_JDI_K_NI_HLED_NIKDY_ME_NENAPADLO_PTAT_SE_TE_NA_TO_KDYZ_JE_CLOVEK_PRINCEZNA_MYSLI_SI_ZE_JE_NA_SVETE_SAM_MAS_JI_RAD_POHLEDL_NA_NI_UTRYZNENYMA_OCIMA_PRECE_JEN_NEDOVEDL_ZAPRIT__TAK_VIDIS_VYDECHLA_TY_NEUMIS_ANI_LHAT_TY_MILY_ALE_POCHOP_KDYZ_JSEM_SI_TO_PAK")
key = ("VLZODTQHUXWSERMCFKNYIBJGP_A")


print("výchozí: ",plaintext)
ciphertext = (substitute_encrypt(plaintext, key))
print("zakódováno: ",ciphertext)

plaintextX = (substitute_decrypt(ciphertext, key))
print("dekódováno: ",plaintextX)