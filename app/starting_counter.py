def increment_counter():
    try:
        # Open the file in read mode to check the current count
        with open("count.txt", "r") as f:
            count = int(f.read() or 0)
    except FileNotFoundError:
        # If the file does not exist, start count at 0
        count = 0

    # Increment the count
    count += 1

    # Open the file in write mode to update the count
    with open("count.txt", "w") as f:
        f.write(str(count))
