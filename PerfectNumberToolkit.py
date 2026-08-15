import math
import re


# ==========================================
# PERFECT NUMBER TERMINAL
# Version 1.0
# ==========================================


# ------------------------------------------
# Perfect Number Check
# ------------------------------------------

def is_perfect_number(n):
    if n < 2:
        print("False")
        print("Previous perfect number: None")
        print("Next perfect number:", next_perfect_number(n))
        return False

    total = 1

    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            total += i

            if i != n // i:
                total += n // i

    if total == n:
        print("True")
        return True

    print("False")
    print("Previous perfect number:", prev_perfect_number(n))
    print("Next perfect number:", next_perfect_number(n))

    return False


# ------------------------------------------
# Next Perfect Number
# ------------------------------------------

def next_perfect_number(n):
    candidate = max(2, n + 1)

    while True:
        total = 1

        for i in range(2, math.isqrt(candidate) + 1):
            if candidate % i == 0:
                total += i

                if i != candidate // i:
                    total += candidate // i

        if total == candidate:
            return candidate

        candidate += 1


# ------------------------------------------
# Previous Perfect Number
# ------------------------------------------

def prev_perfect_number(n):
    candidate = n - 1

    while candidate >= 2:
        total = 1

        for i in range(2, math.isqrt(candidate) + 1):
            if candidate % i == 0:
                total += i

                if i != candidate // i:
                    total += candidate // i

        if total == candidate:
            return candidate

        candidate -= 1

    return None


# ------------------------------------------
# Perfect Numbers Up To
# ------------------------------------------

def perfect_numbers_upto(n):
    results = []

    for candidate in range(2, n + 1):
        total = 1

        for i in range(2, math.isqrt(candidate) + 1):
            if candidate % i == 0:
                total += i

                if i != candidate // i:
                    total += candidate // i

        if total == candidate:
            results.append(candidate)

    print(results)
    return results


# ------------------------------------------
# Perfect Numbers Between
# ------------------------------------------

def perfect_numbers_between(x, y):
    if x > y:
        x, y = y, x

    results = []

    for candidate in range(max(2, x), y + 1):
        total = 1

        for i in range(2, math.isqrt(candidate) + 1):
            if candidate % i == 0:
                total += i

                if i != candidate // i:
                    total += candidate // i

        if total == candidate:
            results.append(candidate)

    print(results)
    return results


# ------------------------------------------
# Nth Perfect Number
# ------------------------------------------

def nth_perfect_number(n):
    if n < 1:
        print("Error: n must be at least 1.")
        return None

    count = 0
    candidate = 1

    while count < n:
        candidate += 1

        total = 1

        for i in range(2, math.isqrt(candidate) + 1):
            if candidate % i == 0:
                total += i

                if i != candidate // i:
                    total += candidate // i

        if total == candidate:
            count += 1

    print(candidate)
    return candidate


# ------------------------------------------
# Count Perfect Numbers Up To
# ------------------------------------------

def count_perfect_numbers_upto(n):
    count = 0

    for candidate in range(2, n + 1):
        total = 1

        for i in range(2, math.isqrt(candidate) + 1):
            if candidate % i == 0:
                total += i

                if i != candidate // i:
                    total += candidate // i

        if total == candidate:
            count += 1

    print(count)
    return count


# ------------------------------------------
# Perfect Number Info
# ------------------------------------------

def perfect_number_info(n):
    if n < 2:
        print("Number:", n)
        print("Perfect:", False)
        print("Previous perfect number:", prev_perfect_number(n))
        print("Next perfect number:", next_perfect_number(n))
        return

    divisors = []

    for i in range(1, math.isqrt(n) + 1):
        if n % i == 0:
            divisors.append(i)

            if i != n // i:
                divisors.append(n // i)

    divisors.sort()

    proper_divisors = [d for d in divisors if d != n]
    divisor_sum = sum(proper_divisors)

    print("Number:", n)
    print("Perfect:", divisor_sum == n)
    print("Proper divisors:", proper_divisors)
    print("Sum of proper divisors:", divisor_sum)

    if divisor_sum == n:
        print("Status: Perfect Number")
    else:
        print("Status: Not a Perfect Number")
        print("Previous perfect number:", prev_perfect_number(n))
        print("Next perfect number:", next_perfect_number(n))


# ------------------------------------------
# Help
# ------------------------------------------

def show_help():
    print("""
==========================================
             COMMANDS
==========================================

is_perfect_number(n)
    Checks whether n is a perfect number.

next_perfect_number(n)
    Finds the next perfect number after n.

prev_perfect_number(n)
    Finds the previous perfect number before n.

perfect_numbers_upto(n)
    Shows all perfect numbers up to n.

perfect_numbers_between(x, y)
    Shows all perfect numbers between x and y.

nth_perfect_number(n)
    Shows the nth perfect number.

count_perfect_numbers_upto(n)
    Counts perfect numbers up to n.

perfect_number_info(n)
    Shows detailed information about n.

help
    Shows this help menu.

about
    Shows information about the program.

exit
    Exits the program.
""")


# ------------------------------------------
# About
# ------------------------------------------

def show_about():
    print("""
==========================================
        PERFECT NUMBER TERMINAL
==========================================

Version: 1.0
Language: Python

A terminal toolkit for finding,
checking, and analyzing perfect numbers.

==========================================
""")


# ------------------------------------------
# Command Parser
# ------------------------------------------

def execute_command(command):
    command = command.strip()

    if command.lower() == "help":
        show_help()
        return True

    if command.lower() == "about":
        show_about()
        return True

    if command.lower() == "exit":
        return False

    pattern = r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)$"
    match = re.match(pattern, command)

    if not match:
        print("Invalid command.")
        print("Type 'help' to see available commands.")
        return True

    function_name = match.group(1)
    arguments = match.group(2).strip()

    functions = {
        "is_perfect_number": (is_perfect_number, 1),
        "next_perfect_number": (next_perfect_number, 1),
        "prev_perfect_number": (prev_perfect_number, 1),
        "perfect_numbers_upto": (perfect_numbers_upto, 1),
        "perfect_numbers_between": (perfect_numbers_between, 2),
        "nth_perfect_number": (nth_perfect_number, 1),
        "count_perfect_numbers_upto": (count_perfect_numbers_upto, 1),
        "perfect_number_info": (perfect_number_info, 1),
    }

    if function_name not in functions:
        print(f"Unknown command: {function_name}")
        print("Type 'help' to see available commands.")
        return True

    function, argument_count = functions[function_name]

    try:
        parts = [part.strip() for part in arguments.split(",")]

        if len(parts) != argument_count:
            print(
                f"Error: {function_name}() requires "
                f"{argument_count} argument(s)."
            )
            return True

        numbers = [int(part) for part in parts]

        function(*numbers)

    except ValueError:
        print("Error: arguments must be integers.")

    except Exception as error:
        print("Error:", error)

    return True


# ------------------------------------------
# Main Program
# ------------------------------------------

def main():
    print("""
==========================================
       PERFECT NUMBER TERMINAL
==========================================

Type 'help' to see available commands.
Type 'exit' to quit.
""")

    while True:
        command = input(">>> ")

        should_continue = execute_command(command)

        if not should_continue:
            print("Goodbye!")
            break

        while True:
            choice = input("\nContinue? (y/n): ").strip().lower()

            if choice == "y":
                break

            if choice == "n":
                print("Goodbye!")
                return

            print("Please enter 'y' or 'n'.")


# ------------------------------------------
# Start Program
# ------------------------------------------

if __name__ == "__main__":
    main()
