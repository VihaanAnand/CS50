#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 == score2)
    {
        printf("Tie!\n");
    }
    else
    {
        printf("Player 2 wins!\n");
    }
}

int compute_score(string word)
{
    // Compute and return score for string
    int score = 0;
    long letters = strlen(word);
    for (long a = 0; a < letters; a++)
    {
        if (word[a] >= 'a' && word[a] <= 'z')
        {
            score += POINTS[word[a] - 97];
        }
        else if (word[a] >= 'A' && word[a] <= 'Z')
        {
            score += POINTS[word[a] - 65];
        }
    }
    return score;
}
