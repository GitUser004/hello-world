def read_letter(letters,already_letter):
    while letters:
        current_letter = letters.pop()

        #模拟读取字母的过程
        print("Printing letter:" + current_letter)
        already_letter.append(current_letter)
def show_already_letter(already_letter):
    print("\nThe follwing letters has been read:")
    for letter in already_letter:
        print(letter)

def aaa(list):
    list[0]="123"


letters = ['A','B','C','D']
already_letter=[]

read_letter(letters,already_letter)
show_already_letter(already_letter)

aaa(already_letter)
show_already_letter(already_letter)