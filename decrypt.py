from encrypt import encrypt


def decrypt(input_text: str, key: int) -> str:
    '''
    We can use the same function to decrypt, instead,
    we’ll modify the shift key value such that it = 26 - shift key.
    Here's the formula for it:
    -> Cipher(n) = De-cipher(26-n)
    '''
    encrypted_text = encrypt(input_text=input_text, key=26 - key)
    separator_char = 'n'
    if separator_char != encrypted_text[-1]:
        return "".join(encrypted_text.replace('n', ' '))
    else:
        # In case char "n" located at the end of the string
        return "n".join(encrypted_text.replace("n", ' ').rsplit(' ', 1))
