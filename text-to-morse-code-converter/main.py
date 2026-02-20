# Text to Morse Code Converter
# Author: Omkar Udawant

MC_CHART = "morse_code_chart.txt"


def load_chart():
    """
    Loads the Morse code chart from a text file
    and returns it as a dictionary.
    """
    try:
        with open(MC_CHART, "r", encoding="utf-8") as file:
            return {
                line.strip().split(" ")[0]: line.strip().split(" ")[1]
                for line in file
            }
    except FileNotFoundError:
        print("Error: morse_code_chart.txt file not found.")
        exit()


def get_user_input():
    """
    Prompts the user for input and ensures
    something valid is entered.
    """
    while True:
        text = input("Enter text to convert: ").lower().strip()
        if text:
            return text
        print("Please enter some valid text.")


def convert_to_morse(text, morse_dict):
    """
    Converts given text into Morse code.
    Unsupported characters are ignored.
    """
    converted = []

    for char in text:
        if char == " ":
            converted.append("/")  # word separator
        elif char in morse_dict:
            converted.append(morse_dict[char])

    return " ".join(converted)


def main():
    print("\n🔤 Welcome to the Text to Morse Code Converter 🔤\n")

    morse_dict = load_chart()

    while True:
        user_text = get_user_input()
        morse_output = convert_to_morse(user_text, morse_dict)

        if morse_output:
            print("\nMorse Code Output:")
            print(morse_output)
        else:
            print("No convertible characters found.")

        again = input("\nConvert another text? (y/n): ").lower().strip()
        if again != "y":
            break

    print("\nGoodbye! 👋")


if __name__ == "__main__":
    main()