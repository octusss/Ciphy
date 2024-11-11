import base64
import os
import random
import string
import platform
import time

# Function to clear the screen
def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

# Function to display the bot header
def display_header(title):
    print("\033[1;34m====================\033[0m")
    print(f"\033[1;35m    {title}\033[0m")
    print("\033[1;34m====================\033[0m")

# Function to read configuration from a file
def read_config(file_path):
    config = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                config[key] = value
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except ValueError:
        print(f"Error: Invalid format in configuration file '{file_path}'.")
    return config

# Function to generate a random key file or allow custom key generation
def generate_key_file(file_path, encoding_type):
    try:
        if encoding_type == 'easy':
            key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            shift = random.randint(1, 25)

        elif encoding_type == 'secure':
            key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            shift = random.randint(26, 50)

        elif encoding_type == 'hard':
            key = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=64))
            shift = random.randint(51, 100)

        elif encoding_type == 'custom':
            print("\n\033[1;36m--- Custom Key File Generation ---\033[0m")
            key = input("Enter custom XOR key (leave blank for random): ") or ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            shift = int(input("Enter Caesar shift value: "))

        else:
            print("Invalid encoding type.")
            time.sleep(1.5)
            clear_screen()
            return

        with open(file_path, 'w') as file:
            file.write(f"xor_key={key}\n")
            file.write(f"caesar_shift={shift}\n")
        
        print(f"\n\033[1;32mKey file '{file_path}' generated successfully.\033[0m\n")
        time.sleep(1.5)
        clear_screen()

    except Exception as e:
        print(f"\n\033[1;31mError...\033[0m")
        time.sleep(2)
        clear_screen()

# XOR Function
def xor_cipher(text, key):
    encoded_chars = []
    for i in range(len(text)):
        encoded_char = chr(ord(text[i]) ^ ord(key[i % len(key)]))
        encoded_chars.append(encoded_char)
    return ''.join(encoded_chars)

# Caesar Cipher
def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if 32 <= ord(char) <= 126:
            shifted = chr((ord(char) - 32 + shift) % 95 + 32)
            result += shifted
        else:
            result += char
    return result

# Convert string to Hexadecimal
def ascii_to_hex(text):
    return ''.join([hex(ord(c))[2:].zfill(2) for c in text])

# Convert Hex back to ASCII
def hex_to_ascii(hex_string):
    try:
        bytes_object = bytes.fromhex(hex_string)
        return bytes_object.decode('ascii')
    except ValueError:
        return ""

# Encoding function
def encode(text, xor_key, caesar_shift):
    try:
        text = base64.b64encode(text.encode('ascii')).decode('ascii')
        text = xor_cipher(text, xor_key)
        text = caesar_cipher(text, caesar_shift)
        text = ascii_to_hex(text)  # Add hex conversion
        return text
    except Exception as e:
        clear_screen()
        return ""

# Decoding function
def decode(encoded_text, xor_key, caesar_shift):
    try:
        text = hex_to_ascii(encoded_text)  # Convert hex back to ASCII
        text = caesar_cipher(text, -caesar_shift)
        text = xor_cipher(text, xor_key)
        text = base64.b64decode(text).decode('ascii')
        return text
    except Exception as e:
        clear_screen()
        return ""

# Main user interface
def main():
    clear_screen()  # Clear the screen at the start
    key_file_loaded = False  # Track if a key file has been loaded
    global xor_key, caesar_shift

    default_key_file = "default.key"  # Default key file name

    while True:
        display_header("Cipher System")
        print(" 1) Encode / Decode")
        print(" 2) Load custom key file")
        print(" 3) Generate key file")
        print(" q) Quit")
        print("\033[1;34m====================\033[0m")
        action = input("\033[1;37mChoose an action: \033[0m").strip().lower()

        if action == '1':
            clear_screen()  # Clear the screen for the next menu

            # Load the default key file when encoding/decoding is selected
            if not key_file_loaded:
                if os.path.exists(default_key_file):
                    config = read_config(default_key_file)
                    if config:  # Only proceed if the config is valid
                        xor_key = config.get('xor_key', '')
                        caesar_shift = int(config.get('caesar_shift', 0))
                        key_file_loaded = True  # Mark key file as loaded
                        print(f"\n\033[1;32mLoaded configuration from '{default_key_file}'.\033[0m\n")
                        time.sleep(1.5)
                        clear_screen()
                else:
                    print(f"\n\033[1;31mError: Key file '{default_key_file}' not found.\033[0m")
                    print("Please load a key file first.\n")
                    time.sleep(3)
                    clear_screen()
                    continue  # Go back to the main menu

            while True:
                display_header("Encode / Decode Menu")
                print(" 1) Encode")
                print(" 2) Decode")
                print(" b) Back")
                print("\033[1;34m====================\033[0m")

                sub_action = input("\033[1;37mChoose an action: \033[0m").lower()

                if sub_action == '1':  # Encode
                    text = input("\033[1;37mEnter text to encode: \033[0m")
                    encoded = encode(text, xor_key, caesar_shift)
                    if encoded:
                        print(f"\n\033[1;32mEncoded:\033[0m \x1b[35m{encoded}\033[0m\n")
                        input("Press enter key to continue...")  # Wait for user input
                        clear_screen()

                elif sub_action == '2':  # Decode
                    encoded_text = input("\033[1;37mEnter text to decode: \033[0m")
                    decoded = decode(encoded_text, xor_key, caesar_shift)
                    if decoded:
                        print(f"\n\033[1;32mDecoded:\033[0m \x1b[35m{decoded}\033[0m\n")
                        input("Press enter key to continue...")  # Wait for user input
                        clear_screen()

                elif sub_action == 'b':
                    clear_screen()  # Clear the screen before going back
                    break

                else:
                    print("\033[1;31mInvalid option. Please choose 1, 2, or b.\033[0m\n")
                    time.sleep(2)
                    clear_screen()

        elif action == '2':  # Load custom key file
            clear_screen()  # Clear the screen for the next menu
            display_header("Load Custom Key File")
            file_name = input("\033[1;37mKey File name: \033[0m")
            if os.path.exists(file_name):
                config = read_config(file_name)
                if config:  # Only proceed if the config is valid
                    xor_key = config.get('xor_key', '')
                    caesar_shift = int(config.get('caesar_shift', 0))
                    key_file_loaded = True  # Mark key file as loaded
                    print(f"\n\033[1;32mLoaded configuration from '{file_name}'.\033[0m\n")
                    time.sleep(1)
                    clear_screen()
                else:
                    print(f"\n\033[1;31mError loading valid configuration from '{file_name}'.\033[0m\n")
                    input("Press enter key to continue...")

            else:
                print(f"\n\033[1;31mFile '{file_name}' not found.\033[0m\n")
                time.sleep(2)
                clear_screen()

        elif action == '3':  # Generate key file
            clear_screen()  # Clear the screen for the next menu
            display_header("Generate Key File")
            file_name = input("\033[1;37mEnter key file name to generate (type nothing for default): \033[0m") or "default.key"
            print("\033[1;36m--- Choose encoding type ---\033[0m")
            print(" 1) Easy encoding")
            print(" 2) Secure encoding")
            print(" 3) Hard encoding")
            print(" 4) Custom encoding")
            encoding_choice = input("\033[1;37mOption: \033[0m").strip()
            encoding_types = {'1': 'easy', '2': 'secure', '3': 'hard', '4': 'custom'}
            
            if encoding_choice in encoding_types:
                generate_key_file(file_name, encoding_types[encoding_choice])
            else:
                print("\033[1;31mInvalid choice. Please select 1, 2, 3, or 4.\033[0m\n")
                time.sleep(2)
                clear_screen()

        elif action == 'q':
            print("\033[1;36mExiting...\033[0m")
            break
        
        else:
            print("\033[1;31mInvalid option. Please choose 1, 2, 3, or q.\033[0m\n")
            time.sleep(2)
            clear_screen()

if __name__ == "__main__":
    main()