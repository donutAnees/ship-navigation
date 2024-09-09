import sys
import pyfiglet

def display_banner():
    banner = pyfiglet.figlet_format("SHIP ROUTING", font="slant")
    print(banner)

def main():
    display_banner()
    print("Welcome to the Ship Routing CLI Tool!")
    print("Enter your start and end coordinates with a step count to begin routing.\n")

    try:
        start_x = float(input("Enter the start X coordinate: "))
        start_y = float(input("Enter the start Y coordinate: "))
        end_x = float(input("Enter the end X coordinate: "))
        end_y = float(input("Enter the end Y coordinate: "))
        steps = int(input("Enter the number of steps: "))

    except ValueError:
        print("Invalid input. Please enter the correct numeric values for coordinates and steps.")
        sys.exit(1)


if __name__ == "__main__":
    main()