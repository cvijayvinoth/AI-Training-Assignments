def calculate_grade():
    try:
        # Prompt the user for input
        user_input = input("Enter a mark (0-100): ")
        
        # Convert input to a float to support both integers and decimals
        mark = float(user_input)

        # Check for out-of-bounds numbers
        if mark < 0 or mark > 100:
            print("Error: The mark must be between 0 and 100.")
            return

        # Determine the grade using top-down boundary checks
        if mark >= 90:
            grade = "A"
        elif mark >= 80:
            grade = "B"
        elif mark >= 70:
            grade = "C"
        elif mark >= 60:
            grade = "D"
        else:
            grade = "E"

        # Format the output to remove trailing '.0' for clean whole numbers
        formatted_mark = int(mark) if mark.is_integer() else mark
        print(f"\nMark entered: {formatted_mark}")
        print(f"Resulting Grade: {grade}")

    except ValueError:
        # Handle non-numeric input gracefully to prevent crashes
        print("Error: Invalid input. Please enter a numerical value.")

if __name__ == "__main__":
    calculate_grade()
