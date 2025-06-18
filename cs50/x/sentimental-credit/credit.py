def removeDigits(number, digits):
    return int((number - (number % (10**digits))) / (10**digits))


def numberI():
    n = input("Number: ")
    try:
        n = int(n)
    except:
        return numberI()
    else:
        return n


number = numberI()
if (removeDigits(number, 13) != 34 and removeDigits(number, 13) != 37 and removeDigits(number, 14) != 51 and removeDigits(number, 14) != 52 and removeDigits(number, 14) != 53 and removeDigits(number, 14) != 54 and removeDigits(number, 14) != 55 and removeDigits(number, 12) != 4 and removeDigits(number, 15) != 4):
    print("INVALID")
    quit()
sumOfProductsDigits = 0
for a in range(9):
    for b in range(2):
        sumOfProductsDigits += removeDigits((removeDigits(number, 2 * a + 1) % 10) * 2, b) % 10
for c in range(9):
    sumOfProductsDigits += removeDigits(number, 2 * c) % 10
if sumOfProductsDigits % 10 != 0:
    print("INVALID")
    quit()
if (removeDigits(number, 13) == 34 or removeDigits(number, 13) == 37):
    print("AMEX")
    quit()
if (removeDigits(number, 14) == 51 or removeDigits(number, 14) == 52 or removeDigits(number, 14) == 53 or removeDigits(number, 14) == 54 or removeDigits(number, 14) == 55):
    print("MASTERCARD")
    quit()
if (removeDigits(number, 12) == 4 or removeDigits(number, 15) == 4):
    print("VISA")
    quit()