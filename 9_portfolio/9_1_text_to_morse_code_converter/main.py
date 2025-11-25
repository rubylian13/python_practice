"""
A text-based Python program to convert Strings into Morse Code.
"""
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',

    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',

    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
    ' ': '/'
}

def text_to_morse(user_input):
    morse_code = " "
    text = user_input.upper()
    for char in text:
        if char in MORSE_CODE_DICT:
            morse_code += MORSE_CODE_DICT[char]
        else:
            morse_code += MORSE_CODE_DICT[' ']
    return morse_code.strip()

user_input = input("Please enter your text convert to Morse Code: ")
morse_output = text_to_morse(user_input)

print(f"Your text is {user_input}")
print(f"Converting to Morse Code is {morse_output}")