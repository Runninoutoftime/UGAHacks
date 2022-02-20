import database
from PIL import Image as pimg

print("test")
print(database.color)

x = 0
for elem in database.color:

    R = elem[0]
    G = elem[1]
    B = elem[2]
    
    i = 0

    pants = ["Jeans", "Pants"]
    if database.name[x] in pants:
        for pant in database.wardrobePantColor:
            if (
                pant[0] >= R - 10 and pant[0] <= R + 10 and
                pant[1] >= G - 10 and pant[1] <= G + 10 and
                pant[2] >= B - 10 and pant[2] <= B + 10
                ):

                pimg.show(database.wardrobePantPath[i])
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

                pimg.show(database.wardrobeShirtPath)

    i = 0

    feet = ["Shoe", "Footwear"]
    for shoe in database.wardrobeShoeColor:
        if (
            shoe[0] >= R - 10 and shoe[0] <= R + 10 and
            shoe[1] >= G - 10 and shoe[1] <= G + 10 and
            shoe[2] >= B - 10 and shoe[2] <= B + 10
            ):

            pimg.show(database.wardrobeShoePath)    

    x = x + 1

