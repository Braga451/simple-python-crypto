import random, sys

def generateCipher(times_to_roll : int = 1) -> dict:
    cipher = [x for x in range(1, 27)]
    letters = [chr(letter) for letter in range(97, 123)]
    dict_crypt = {}
    rolls_remains = times_to_roll
    while(rolls_remains > 0):
        for index in range(len(cipher)):
            cipher[index] += 1
            if(cipher[index] > 26):
                cipher[index] = 1
        rolls_remains -= 1            
    for index in range(len(letters)):
        dict_crypt[letters[index]] = cipher[index]
    return dict_crypt

def numericSymbolicString() -> str:
    symbols_num = [] # Imagine the follow sequence for every crypto: !, @, #, $, %, &, *
    num = random.randint(1, 26)
    while(len(symbols_num) != 7):
        while(num in symbols_num):
            num = random.randint(1, 26)
        symbols_num.append(num)
    return ''.join(str(symbols_num)).replace("[", "").replace("]", "").replace(" ", "")

def symbolicStringToList(string : str = ""):
    return string.replace(" ", "").split(",")

def stringToNumberArray(string :str = "", cipher : dict = {}) -> list:
    ciphered_numbers = []
    letters = [chr(letter) for letter in range(97, 123)]
    if(len(cipher) != 26):
        raise ValueError("Use an valid cipher!")
    else:
        for x in range(len(string)):
            if(string[x] in letters):
                ciphered_numbers.append(str(cipher[string[x].lower()]))
            else:
                ciphered_numbers.append(str(string[x]))
    return ciphered_numbers

def numberArrayToSymbolic(num_array : list = [], symbolic_string : str = "") -> str:
    symbolic_list = symbolicStringToList(symbolic_string)
    symbols = ["!", "@", "#", "$", "%", "&", "*"]
    symbolic_dict = generateSymbolicDict(symbolic_list)
    crypted_array = num_array.copy()
    for key in symbolic_dict.keys():
        if key in crypted_array:
            index_positions = [index for index, x in enumerate(crypted_array) if x == key]
            for index in index_positions:
                crypted_array[index] = symbolic_dict[key]
    return crypted_array

def generateSymbolicDict(symbolic_list : list = []) -> dict:
    symbols = ["!", "@", "#", "$", "%", "&", "*"]
    symbolic_dict = {}
    for x in range(len(symbolic_list)):
        symbolic_dict[symbolic_list[x]] = symbols[x]
    return symbolic_dict

def generateEncrypted(password_to_encrypt : str = "", cipher_rolls : int = 0) -> None:
    cipher = generateCipher(cipher_rolls)
    symbolic_string = numericSymbolicString()
    number_array = stringToNumberArray(password_to_encrypt, cipher)
    encrypted_array = numberArrayToSymbolic(number_array, symbolic_string)
    print(f'''Cipher: {cipher} 
Symbolic string: {symbolic_string}
Numeric password array: {number_array}
Encrypted password array : {','.join(encrypted_array)}
Encrypted password: {''.join(encrypted_array)}
Size: {len(encrypted_array)}''')

def decrypt(cipher : dict = {}, symbolic_dict : dict = {}, password_to_decrypt : list = []) -> str:
    password_to_numeric = password_to_decrypt.copy()
    password_string = ""
    reversed_cipher = {value:key for(key,value) in cipher.items()}
    reversed_cipher_keys = [x for x in reversed_cipher.keys()]
    for keys in symbolic_dict.keys():
        index_positions_password = [index for index, x in enumerate(password_to_decrypt) if x == symbolic_dict[keys]]
        for index in index_positions_password:
            password_to_numeric[index] = keys
    for itens in password_to_numeric:
        if itens in str(reversed_cipher_keys):
            password_string += reversed_cipher[int(itens)]
        else:
            password_string += itens
    return password_string

def returnDecrypt(password_to_decrypt : str = "", cipher_rolls : int = 0, symbolic_string : str = "") -> None:
    symbolic_list = symbolicStringToList(symbolic_string)
    cipher = generateCipher(int(cipher_rolls))
    symbolic_dict = generateSymbolicDict(symbolic_list)
    password_to_decrypt_as_list = password_to_decrypt.replace(" ", "").split(",")
    clean_password = decrypt(cipher, symbolic_dict, password_to_decrypt_as_list)
    print(f'''Cipher: {cipher}
Symbolic dict: {symbolic_dict}
Password: {password_to_decrypt.replace(",", "")}
Clean password: {clean_password}''')

def usage() -> None:
    print('''To encrypt: main.py password_to_encrypt(str) cipher_rolls(int) 
To decrypt: main.py password_to_decrypt_array(str) cipher_rolls(int) "symbolic_string"(str)''')

def main(argv : list = []) -> None:
    if(len(argv) == 2):
        generateEncrypted(argv[0], int(argv[1]))
    elif(len(argv) == 3):
        returnDecrypt(argv[0], argv[1], argv[2])
    else:
        usage()
    
if __name__ == "__main__":
    main(sys.argv[1::])