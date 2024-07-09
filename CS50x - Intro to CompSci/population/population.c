// Include libraries
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get starting population
    double start;
    do
    {
        start = (double) get_long("Start size: ");
    }
    while (start < 9);

    // Get ending population
    double end;
    do
    {
        end = (double) get_long("End size: ");
    }
    while (end < start);

    // Calculate amount of years
    long years = 0;
    long born, died;
    while (end > start)
    {
        born = start / 3;
        died = start / 4;
        start = start + born - died;
        years++;
    }

    // Print amount of years
    printf("Years: %li\n", years);

    return 0;
}