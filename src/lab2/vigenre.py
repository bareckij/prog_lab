def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'  

    """
    ciphertext = ""
    keyword_repeated = (keyword * (len(plaintext) // len(keyword)) + keyword[:len(plaintext) % len(keyword)]).upper() 

    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            shift = ord(keyword_repeated[i]) - ord('A')
            is_upper = plaintext[i].isupper()
            ciphertext += chr((ord(plaintext[i]) - ord('A' if is_upper else 'a') + shift) % 26 + ord('A' if is_upper else 'a'))
        else:
            ciphertext += plaintext[i]
    return ciphertext

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'  

    """
    plaintext = ""
    keyword_repeated = (keyword * (len(ciphertext) // len(keyword)) + keyword[:len(ciphertext) % len(keyword)]).upper()  

    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            shift = ord(keyword_repeated[i]) - ord('A')
            is_upper = ciphertext[i].isupper()
            plaintext += chr((ord(ciphertext[i]) - ord('A' if is_upper else 'a') - shift + 26) % 26 + ord('A' if is_upper else 'a'))
        else:
            plaintext += ciphertext[i]
    return plaintext

print(decrypt_vigenere("python", "a"))
print(encrypt_vigenere("PYTHON", "A"))
print(encrypt_vigenere("python", "a"))
print(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"))
print(encrypt_vigenere("ATTACKATDAWN", "LEMON"))
print(encrypt_vigenere("attackatdawn", "lemon"))


