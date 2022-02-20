import database
from PIL import Image as pimg

print("test")
print(database.color)

# Using readlines()
file1 = open('namesTxt.txt', 'r')
Lines = file1.readlines()
 
count = 0
# Strips the newline character
for line in Lines:
    count += 1
    print("Line{}: {}".format(count, line.strip()))
    database.name.append(line.strip())

with open("wardrobePantColor.txt") as file2:
    R1, G1, B1 = [int(x) for x in next(file2).split()]
    database.wardrobePantColor.append((R1, G1, B1))


# for line in f2:
#     database.wardrobePantColor.append(line.strip())
    

print(database.wardrobePantColor)

file3 = open("wardrobePantPath.txt")
f3 = file3.readlines()

for line in f3:
    database.wardrobePantPath.append(line.strip())


for x in range(len(database.name)):

    with open("colorTxt.txt") as f:
        R, G, B = [int(x) for x in next(f).split()]
        
        print("RGB: ", R, G, B)
    i = 0

    pants = ["Jeans", "Pants"]
    if str(database.name[x]) in pants:
        print("b")
        for pant in database.wardrobePantColor:
            print("a")
            print("A: ", pant[0], pant[1], pant[2])
            if (
                int(pant[0]) >= R - 10 and int(pant[0]) <= R + 10 and
                int(pant[1]) >= G - 10 and int(pant[1]) <= G + 10 and
                int(pant[2]) >= B - 10 and int(pant[2]) <= B + 10
                ):

                print("tt")
                with pimg.open("".join(database.wardrobePantPath)) as im:
                    im.show()
            
            i = i + 1

    i = 0

    tops = ["Top", "Dress", "Outerwear", "Jacket"]
    if database.name[x] in tops:
        for shirt in database.wardrobeShirtColor:
            if (
                shirt[0] >= R - 10 and shirt[0] <= R + 10 and
                shirt[1] >= G - 10 and shirt[1] <= G + 10 and
                shirt[2] >= B - 10 and shirt[2] <= B + 10
                ):
                
                print("show shirt")


    i = 0

    feet = ["Shoe", "Footwear"]
    for shoe in database.wardrobeShoeColor:
        if (
            shoe[0] >= R - 10 and shoe[0] <= R + 10 and
            shoe[1] >= G - 10 and shoe[1] <= G + 10 and
            shoe[2] >= B - 10 and shoe[2] <= B + 10
            ):

            print("show shoe")

    x = x + 1

