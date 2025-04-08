import sys

def read_file(file_path):
    """Read text from a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def process_text(text):
    """Process the text (count words, convert to uppercase)."""
    if not text:
        return None
    word_count = len(text.split())
    uppercase_text = text.upper()
    return {"original_text": text, "word_count": word_count, "uppercase_text": uppercase_text}

def write_results(results, output_file):
    """Write the processed results to a file."""
    if not results:
        return False
    try:
        with open(output_file, 'w') as file:
            file.write(f"Original Text:\n{results['original_text']}\n\n")
            file.write(f"Word Count: {results['word_count']}\n\n")
            file.write(f"Uppercase Text:\n{results['uppercase_text']}\n")
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False

def interactive_mode():
    """Interactive mode to process user input or view text."""
    print("Welcome to the Interactive Text Processor!")
    print("Options:")
    print("1. View text in input.txt")
    print("2. Process text from input.txt")
    print("3. Enter new text to process")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            text = read_file("input.txt")
            if text is None:
                print("No input.txt found.")
            else:
                print("\nCurrent text in input.txt:")
                print(text)

        elif choice == "2":
            text = read_file("input.txt")
            if text is None:
                print("No input.txt found. Please create one or enter text manually.")
                continue
            results = process_text(text)
            if results and write_results(results, "output.txt"):
                print(f"Processing complete. Results written to output.txt")
            else:
                print("Processing failed.")
        elif choice == "3":
            text = input("Enter your text: ")
            results = process_text(text)
            if results:
                save = input("Would you like to save this to input.txt? (y/n): ").lower()
                if save == 'y':
                    with open("input.txt", 'w') as f:
                        f.write(text)
                    print("Text saved to input.txt")
                if write_results(results, "output.txt"):
                    print(f"Processing complete. Results written to output.txt")
                else:
                    print("Processing failed.")
            else:
                print("Processing failed.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

def main(input_file="input.txt", output_file="output.txt"):
    """Main function to process text file or launch interactive mode based on user input."""
    if sys.stdin.isatty():
        print("Do you want to run in interactive mode? (y/n): ")
        choice = input().lower()
    else:
        choice = 'n'  # Default to non-interactive in non-terminal environments

    if choice == 'y':
        interactive_mode()
    elif choice == 'n':
        text = read_file(input_file)
        if text:
            results = process_text(text)
            if results:
                success = write_results(results, output_file)
                if success:
                    print(f"Processing complete. Results written to {output_file}")
                    print(f"Content is {results}")
                    return True
        print("Processing failed.")
        return False
    else:
        print("Invalid choice. Please enter 'y' or 'n' next time.")
        return False

if __name__ == "__main__":
    main()