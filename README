Python SETCOVER
===============

This is an implementation of [SETCOVER](https://en.wikipedia.org/wiki/Set_cover_problem) in python, hacked together for a friend's PhD thesis. It computes the **complete list of solutions** for the given input set of subsets.

Features
--------
 * Read input from a file
 * Computes **all** the solutions for a given input set of subsets

Usage
-----
Run the program with the input file as the **first** parameter. Optionally you can force new format file behaviour by specifying `--new-file` as the **second** parameter. Example:

    python cover.py input.txt

Input file format
-----------------
The input file contains one subset description per line. Each element has to be a parseable integer value. For example, a simple input file could look like this:

    1 2 3 4 5 6 7
    8 9 10 11 12 13 14
    1 8
    2 3 9 10
    4 5 6 7 11 12 13 14

### Older file format
Older versions used an input file format, where the first to lines contained the number of vertices and the number of subsets respectively. Those files are automatically detected and the first two lines will not be taken as subsets. The example from above would look like this:

    14
    5
    1 2 3 4 5 6 7
    8 9 10 11 12 13 14
    1 8
    2 3 9 10
    4 5 6 7 11 12 13 14


Caveats
-------
 * **Caution!** This code is far from perfect and I cannot guarantee, that it is usefull at all or will suit your needs. 
 * Always make sure, you either specify old format files or use the --new-file option.
 * During runtime, the code outputs subset numbers with an offset of "-1", starting at 0. The final output list starts at 1.
 * Also it is horribly slow, due to the hackish implementation using python sets and the exhaustive nature of the search.
