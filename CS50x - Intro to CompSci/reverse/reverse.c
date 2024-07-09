#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "wav.h"

bool check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 3)
    {
        printf("Usage: ./reverse input.wav output.wav\n");
        return 1;
    }

    // Open input file for reading
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open %s. Please try a different file.\n", argv[1]);
        return 1;
    }

    // Read header
    WAVHEADER header;
    fread(&header, sizeof(WAVHEADER), 1, input);

    // Use check_format to ensure WAV format
    if (!check_format(header))
    {
        printf("Input is not a WAV file.");
        return 1;
    }

    // Open output file for writing
    FILE *output = fopen(argv[2], "w");

    // Write header to file
    fwrite(&header, sizeof(WAVHEADER), 1, output);

    // Use get_block_size to calculate size of block
    int blockSize = get_block_size(header);

    // Write reversed audio to file
    int eoh = ftell(input);
    fseek(input, -1 * blockSize, SEEK_END);
    BYTE block[blockSize];
    while (ftell(input) >= eoh)
    {
        fread(&block, sizeof(block), 1, input);
        fwrite(&block, sizeof(block), 1, output);
        fseek(input, -2 * blockSize, SEEK_CUR);
    }

    fclose(input);
    fclose(output);
}

bool check_format(WAVHEADER header)
{
    if (header.format[0] != 87 || header.format[1] != 65 || header.format[2] != 86 || header.format[3] != 69)
    {
        return false;
    }
    return true;
}

int get_block_size(WAVHEADER header)
{
    return header.numChannels * header.bitsPerSample / 8;
}