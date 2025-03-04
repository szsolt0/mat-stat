# Pi Estimation Project

This project is developed for the Mathematical Statistics course at the University of Miskolc. It estimates the value of π using Buffon's needle problem and the Monte Carlo method.

## Usage

To generate matchsticks:

```sh
./generate 1000
```

Replace `1000` with the desired number of samples.

To plot while generating data:

```sh
./generator | ./plotter.py
```

Alternatively, you can redirect the generated values to files and read them for plotting later using standard Unix redirection.

## Compilation

To compile using `g++`:

```sh
g++ -Wall -Wextra -O2 -o generator generator.cpp
```

You may use any compatible C++ compiler of your choice.

## Customization

- The `MAX_SINGLE_ROUNDS` static constant determines the number of matchsticks stored in memory at once. Adjust this value based on the available RAM.
- The program allocates `MAX_SINGLE_ROUNDS * sizeof(Matchstick)` bytes of memory. Choose an appropriate value to balance memory usage and performance.
- The `PRINT_RESULTS` static constant controls whether individual matchstick coordinates are printed. Disable this option when running large simulations (e.g., 1 trillion samples) to improve efficiency.
- The `ANIMATE` variable in `plotter.py` determines whether the visualization is animated.

## Non-Unix Platform Compatibility

The code follows standard C++ conventions, with two Unix-specific exceptions:

- The `mmap()` call: Replace it with an equivalent `malloc()` allocation.
- The `madvise()` call: This can be safely commented out without affecting functionality.

These modifications will enable the program to run on non-Unix platforms.

## License

This project is licensed under the MIT License.
