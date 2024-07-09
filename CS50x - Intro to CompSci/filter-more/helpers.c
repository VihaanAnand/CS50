#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (long heightBit = 0; heightBit < height; heightBit++)
    {
        for (long widthBit = 0; widthBit < width; widthBit++)
        {
            BYTE average = (BYTE) round(
                (image[heightBit][widthBit].rgbtRed + image[heightBit][widthBit].rgbtGreen + image[heightBit][widthBit].rgbtBlue) /
                3.0);
            image[heightBit][widthBit].rgbtRed = average;
            image[heightBit][widthBit].rgbtGreen = average;
            image[heightBit][widthBit].rgbtBlue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE original[height][width];
    for (long heightBit = 0; heightBit < height; heightBit++)
    {
        for (long widthBit = 0; widthBit < width; widthBit++)
        {
            original[heightBit][widthBit].rgbtRed = image[heightBit][widthBit].rgbtRed;
            original[heightBit][widthBit].rgbtGreen = image[heightBit][widthBit].rgbtGreen;
            original[heightBit][widthBit].rgbtBlue = image[heightBit][widthBit].rgbtBlue;
        }
    }
    for (long heightBit = 0; heightBit < height; heightBit++)
    {
        for (long widthBit = 0; widthBit < width; widthBit++)
        {
            image[heightBit][widthBit].rgbtRed = original[heightBit][width - widthBit - 1].rgbtRed;
            image[heightBit][widthBit].rgbtGreen = original[heightBit][width - widthBit - 1].rgbtGreen;
            image[heightBit][widthBit].rgbtBlue = original[heightBit][width - widthBit - 1].rgbtBlue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE original[height][width];
    for (long heightBit = 0; heightBit < height; heightBit++)
    {
        for (long widthBit = 0; widthBit < width; widthBit++)
        {
            original[heightBit][widthBit].rgbtRed = image[heightBit][widthBit].rgbtRed;
            original[heightBit][widthBit].rgbtGreen = image[heightBit][widthBit].rgbtGreen;
            original[heightBit][widthBit].rgbtBlue = image[heightBit][widthBit].rgbtBlue;
        }
    }
    for (long heightBit = 0; heightBit < height; heightBit++)
    {
        for (long widthBit = 0; widthBit < width; widthBit++)
        {
            long count = 0;
            long red = 0;
            long green = 0;
            long blue = 0;
            for (long row = -1; row < 2; row++)
            {
                for (long column = -1; column < 2; column++)
                {
                    if (row + heightBit < 0 || row + heightBit > height - 1 || column + widthBit < 0 ||
                        column + widthBit > width - 1)
                    {
                        continue;
                    }
                    count++;
                    red += original[row + heightBit][column + widthBit].rgbtRed;
                    green += original[row + heightBit][column + widthBit].rgbtGreen;
                    blue += original[row + heightBit][column + widthBit].rgbtBlue;
                }
            }
            BYTE red2 = (BYTE) (round(red / ((double) (count))));
            BYTE green2 = (BYTE) (round(green / ((double) (count))));
            BYTE blue2 = (BYTE) (round(blue / ((double) (count))));
            image[heightBit][widthBit].rgbtRed = red2;
            image[heightBit][widthBit].rgbtGreen = green2;
            image[heightBit][widthBit].rgbtBlue = blue2;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE original[height][width];
    for (long heightBit = 0; heightBit < height; heightBit++)
    {
        for (long widthBit = 0; widthBit < width; widthBit++)
        {
            original[heightBit][widthBit].rgbtRed = image[heightBit][widthBit].rgbtRed;
            original[heightBit][widthBit].rgbtGreen = image[heightBit][widthBit].rgbtGreen;
            original[heightBit][widthBit].rgbtBlue = image[heightBit][widthBit].rgbtBlue;
        }
    }
    for (long heightBit = 0; heightBit < height; heightBit++)
    {
        for (long widthBit = 0; widthBit < width; widthBit++)
        {
            long redX = 0;
            long greenX = 0;
            long blueX = 0;
            long redY = 0;
            long greenY = 0;
            long blueY = 0;
            long x[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
            long y[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
            for (long row = -1; row < 2; row++)
            {
                for (long column = -1; column < 2; column++)
                {
                    if (row + heightBit < 0 || row + heightBit > height - 1 || column + widthBit < 0 ||
                        column + widthBit > width - 1)
                    {
                        continue;
                    }
                    redX += (x[row + 1][column + 1] * original[row + heightBit][column + widthBit].rgbtRed);
                    greenX += (x[row + 1][column + 1] * original[row + heightBit][column + widthBit].rgbtGreen);
                    blueX += (x[row + 1][column + 1] * original[row + heightBit][column + widthBit].rgbtBlue);
                    redY += (y[row + 1][column + 1] * original[row + heightBit][column + widthBit].rgbtRed);
                    greenY += (y[row + 1][column + 1] * original[row + heightBit][column + widthBit].rgbtGreen);
                    blueY += (y[row + 1][column + 1] * original[row + heightBit][column + widthBit].rgbtBlue);
                    BYTE red = (BYTE) (fmin(round(sqrt(redX * redX + redY * redY)), 255));
                    BYTE green = (BYTE) (fmin(round(sqrt(greenX * greenX + greenY * greenY)), 255));
                    BYTE blue = (BYTE) (fmin(round(sqrt(blueX * blueX + blueY * blueY)), 255));
                    if (red > 255)
                    {
                        red = 255;
                    }
                    if (green > 255)
                    {
                        green = 255;
                    }
                    if (blue > 255)
                    {
                        blue = 255;
                    }
                    image[heightBit][widthBit].rgbtRed = red;
                    image[heightBit][widthBit].rgbtGreen = green;
                    image[heightBit][widthBit].rgbtBlue = blue;
                }
            }
        }
    }
    return;
}
