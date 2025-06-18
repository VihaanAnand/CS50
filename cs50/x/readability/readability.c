// Include libraries
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Get text
    string text = get_string("Text: ");

    // Calculate number of letters
    long characters = strlen(text);
    long letters = characters;
    for (long a = 0; a < characters; a++)
    {
        if (!((text[a] >= 'a' && text[a] <= 'z') || (text[a] >= 'A' && text[a] <= 'Z')))
        {
            letters--;
        }
    }

    // Calculate number of words
    long words = 0;
    for (long a = 0; a < characters; a++)
    {
        if (text[a] == ' ')
        {
            words++;
        }
    }
    words++;

    // Calculate number of sentences
    long sentences = 0;
    for (long a = 0; a < characters; a++)
    {
        if (text[a] == '.' || text[a] == '?' || text[a] == '!')
        {
            sentences++;
        }
    }

    // Calculate averages per 100 words
    double lettersPer100 = (double) letters / (double) words * 100;
    double sentencesPer100 = (double) sentences / (double) words * 100;

    // Use Coleman-Liau formula
    long colemanLiau = (long) (0.0588 * lettersPer100 - 0.296 * sentencesPer100 - 15.8 + 0.5);

    // Print Coleman-Liau index
    if (colemanLiau < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (colemanLiau >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %li\n", colemanLiau);
    }
}