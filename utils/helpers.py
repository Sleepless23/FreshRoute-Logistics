from getpass import getpass

def select_from_list(prompt_options, exit_message="Exiting...", exit_option="Exit", head_text=""):
    if not prompt_options:
        print("No options provided!")
        return None

    print(f"\n{'=' * 50}") 
    if head_text:
        print(head_text)
    print("Please choose an option:")
    for i, option in enumerate(prompt_options, start=1):
        print(f"{i}. {option}")
    print(f"{len(prompt_options) + 1}. {exit_option}")
    print(f"{'=' * 50}") 

    while True:
        try:
            user_input = input("\nEnter your choice: ").strip()
            
            if not user_input:
                print("Input cannot be empty. Please try again.")
                continue

            if user_input.lower() == 'exit' or user_input == str(len(prompt_options) + 1):
                print(exit_message)
                return None

            value = int(user_input)
            if 1 <= value <= len(prompt_options):
                    return value
            else:
                print(f"Invalid choice! Please enter a number between 1 and {len(prompt_options) + 1}.")

        except ValueError:
            print("Invalid input! Please enter a valid number or 'exit'.")
        except (EOFError, KeyboardInterrupt):
            print("\nInput canceled by user.")
            return None

def input_string(prompt, exit_message="Exiting...", required_input=[], allow_pass=False, allow_empty=False):
    while True:
        try:
            user_input = input(prompt).strip() if not allow_pass else getpass(prompt).strip()
            
            if not user_input and not allow_empty:
                print("Input cannot be empty. Please try again.")
                continue

            if required_input and user_input.lower() not in required_input:
                print(f"Invalid input! Please enter one of the following: {', '.join(required_input)}")
                continue
            
            if user_input.lower() == 'exit':
                print(exit_message)
                return None
            
            return user_input
        
        except (EOFError, KeyboardInterrupt):
            print("\nInput canceled by user.")
            return None
