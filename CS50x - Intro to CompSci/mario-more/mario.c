// Include libraries
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get height
    long height;
    do
    {
        height = get_long("Height: ");
    }
    while (height > 8 || height < 1);

    // Print pryamids
    for (long row = 0; row < height; row++)
    {
        for (long column = 0; column < 2 * height + 2; column++)
        {
            if (column < height - row - 1 || column == height || column == height + 1)
            {
                printf(" ");
            }
            else if ((column >= height - row - 1 && column < height) || (column <= height + row + 2))
            {
                printf("#");
            }
        }
        printf("\n");
    }
}