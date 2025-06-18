def heightI():
    h = input("Height: ")
    try:
        h = int(h)
    except:
        return heightI()
    else:
        if h <= 8 and h >= 1:
            return h
        else:
            return heightI()


while True:
    height = heightI()
    if height <= 8 and height >= 1:
        break
for row in range(height):
    for column in range(2 * height + 2):
        if column < height - row - 1 or column == height or column == height + 1:
            print(" ", end="")
        elif (column >= height - row - 1 and column < height) or (column <= height + row + 2):
            print("#", end="")
    print()
