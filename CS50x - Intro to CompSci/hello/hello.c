// Include libraries
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get name
    string name = get_string("What is your name? ");

    // Print Hello
    printf("hello, %s\n", name);

    return 0;
}