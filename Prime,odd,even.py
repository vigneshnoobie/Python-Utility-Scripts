def prime(n):

    if n <= 1:
        return False
    
    if n <= 3:
        return True
    
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    x = 5
    while x * x <= n:

        if n % x == 0 or n % (x + 2) == 0:

            return False
        
        x += 6

    return True

def Sort_n_save(start, end):
    
    odd_numbers = []
    even_numbers = []
    prime_numbers = []
    
    for n in range(start, end + 1):
        if n % 2 == 0:
            even_numbers.append(n)

        else:
            odd_numbers.append(n)
        
        if prime(n):
            prime_numbers.append(n)
    
   
    with open('File_Odd.txt', 'w') as file_odd:
        for n in odd_numbers:
            file_odd.write(str(n) + '\n')
    
  
    with open('File_Even.txt', 'w') as file_even:
        for n in even_numbers:
            file_even.write(str(n) + '\n')
    
    
    with open('File_Prime.txt', 'w') as file_prime:
        for n in prime_numbers:
            file_prime.write(str(n) + '\n')

def show_file_data():
    files = ['File_Odd.txt', 'File_Even.txt', 'File_Prime.txt']
    for file_name in files:
        print(f"Data in {file_name}:")
        try:
            with open(file_name, 'r') as file:
                print(file.read())
        except file_not_found_error:
            print("File not found")

def main():
    while True:
        try:
           
            start, end = map(int, input("Kindly enter the range of numbers: ").split('-'))
            if start < 0 or end < 0 or start > end:
                raise ValueError("Invalid input, it should not be negative and stating number should be less than ending number")
            break
        except ValueError as error:
            print(error)
    
   
    Sort_n_save(start, end)
    
    
    show_file_data()


if __name__ == "__main__":
    main()
