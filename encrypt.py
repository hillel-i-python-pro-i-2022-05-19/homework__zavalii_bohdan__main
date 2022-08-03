def encrypt(input_text: str, key: int) -> str:
    result = ""
    # Transverse the plain text
    input_text.split(" ")
    for i in range(len(input_text)):
        char = input_text[i]
        # Encrypt uppercase characters in plain text
        if char.isupper():
            result += chr((ord(char) + key - 65) % 26 + 65)
            # result.split("w")
        # Encrypt lowercase characters in plain text
        else:
            result += chr((ord(char) + key - 97) % 26 + 97)
    # return " ".join(result.split('w'))
    return result
