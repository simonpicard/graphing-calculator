# -*- coding: utf8 -*-


def matrixToFile(M, fileName):
    """
    Writes the image to the file 'fileName
    Each pixel (or triplet) is written on a separate line.

    """
    fd = open(fileName, "w")
    fd.write("P3\n")
    fd.write("# File generated for graphing calculator\n")
    height = len(M[0])
    width = len(M)
    maxIntensity = 255
    fd.write(str(width) + " " + str(height) + "\n")
    fd.write(str(maxIntensity) + "\n")

    for yi in range(height):
        for xi in range(width):
            strpixel = (
                str(M[xi][yi][0])
                + " "
                + str(M[xi][yi][1])
                + " "
                + str(M[xi][yi][2])
                + "\n"
            )
            fd.write(strpixel)

    fd.write("#end ...")

    fd.close()
