// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26 * 27 * LENGTH + 2;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    node *bucket = table[hash(word)];
    while (bucket != NULL)
    {
        if (strcasecmp(word, bucket->word) == 0)
        {
            return true;
        }
        if (bucket->next != NULL)
        {
            bucket = bucket->next;
        }
        else
        {
            break;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    if (strlen(word) == 1)
    {
        return toupper(word[0]) - 64;
    }
    else if (strlen(word) >= 2)
    {
        int first = toupper(word[0]) - 64;
        int second = toupper(word[1]) - 64;
        if (second == 39 - 64)
        {
            second = 27;
        }
        int length = strlen(word);
        return first * second * length;
    }
    else
    {
        return 0;
    }
}

FILE *inputDictionary;

bool loadWord(char *word)
{
    node *newWord = malloc(sizeof(node));
    if (newWord == NULL)
    {
        return false;
    }
    strcpy(newWord->word, word);
    newWord->next = NULL;
    node *wordMemory = table[hash(word)];
    if (wordMemory == NULL)
    {
        table[hash(word)] = newWord;
    }
    else
    {
        while (wordMemory->next != NULL)
        {
            wordMemory = wordMemory->next;
        }
        wordMemory->next = newWord;
    }
    return true;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    inputDictionary = fopen(dictionary, "r");
    if (inputDictionary == NULL)
    {
        return false;
    }
    char word[LENGTH + 1];
    for (int characterID = 0; true; characterID++)
    {
        if (fscanf(inputDictionary, "%s", word) == EOF)
        {
            break;
        }
        if (!loadWord(word))
        {
            return false;
        }
    }
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    int words = 0;
    for (int bucketID = 0; bucketID < N; bucketID++)
    {
        node *bucket = table[bucketID];
        while (bucket != NULL)
        {
            words++;
            if (bucket->next != NULL)
            {
                bucket = bucket->next;
            }
            else
            {
                break;
            }
        }
    }
    return words;
}

void freeBranch(node *branch)
{
    if (branch == NULL)
    {
        return;
    }
    if (branch->next != NULL)
    {
        freeBranch(branch->next);
        branch->next = NULL;
    }
    free(branch);
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int bucketID = 0; bucketID < N; bucketID++)
    {
        node *bucket = table[bucketID];
        freeBranch(bucket);
    }
    if (fclose(inputDictionary) == EOF)
    {
        return false;
    }
    else
    {
        return true;
    }
}
