// Include libraries
#include <cs50.h>
#include <math.h>
#include <stdio.h>

// Function to remove digits
long removeDigits(long number, long digits)
{
    return ((number - (number % (long) pow(10, digits))) / (long) pow(10, digits));
}

int main(void)
{
    // Get credit card number
    long number = get_long("Number: ");

    // Check if starting is invalid and if the number is too long or short
    if (removeDigits(number, 13) != 34 &&
        removeDigits(number, 13) != 37 &&
        removeDigits(number, 14) != 51 &&
        removeDigits(number, 14) != 52 &&
        removeDigits(number, 14) != 53 &&
        removeDigits(number, 14) != 54 &&
        removeDigits(number, 14) != 55 &&
        removeDigits(number, 12) != 4 &&
        removeDigits(number, 15) != 4)
    {
        printf("INVALID\n");
        return 0;
    }

    // Perform Luhn's algorithm
    long sumOfProductsDigits = 0;
    for (long a = 0; a < 9; a++)
    {
        for (long b = 0; b < 2; b++)
        {
            sumOfProductsDigits += removeDigits((removeDigits(number, 2 * a + 1) % 10) * 2, b) % 10;
        }
    }
    for (long c = 0; c < 9; c++)
    {
        sumOfProductsDigits += removeDigits(number, 2 * c) % 10;
    }
    if (sumOfProductsDigits % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }

    // Find type of card
    if (removeDigits(number, 13) == 34 ||
        removeDigits(number, 13) == 37)
    {
        printf("AMEX\n");
        return 0;
    }
    if (removeDigits(number, 14) == 51 ||
        removeDigits(number, 14) == 52 ||
        removeDigits(number, 14) == 53 ||
        removeDigits(number, 14) == 54 ||
        removeDigits(number, 14) == 55)
    {
        printf("MASTERCARD\n");
        return 0;
    }
    if (removeDigits(number, 12) == 4 ||
        removeDigits(number, 15) == 4)
    {
        printf("VISA\n");
        return 0;
    }
}