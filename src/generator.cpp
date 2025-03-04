#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <cstdint>
#include <limits>
#include <unistd.h>
#include <array>
#include <sys/mman.h>

static constexpr bool PRINT_RESULTS = false;
static constexpr size_t MAX_SINGLE_ROUNDS = 1 << 18; // 1 << 27 == 8 GiB of RAM

struct alignas(32) Matchstick {
	double x0, y0, x1, y1;
	bool c;
};

using MatchstickContainer = std::array<Matchstick, MAX_SINGLE_ROUNDS>;

bool crosses_grid_line(const double y0, const double y1, const double grid_size) {
	return std::floor(y0 / grid_size) != std::floor(y1 / grid_size);
}

void generate_matchsticks(MatchstickContainer& matchsticks, const size_t n, std::mt19937& gen) {
	std::uniform_real_distribution<double> dist_pos(0, 8);
	std::uniform_real_distribution<double> dist_theta(0, 2*M_PI);

	for (size_t i = 0; i < n; ++i) {
		const double x0 = dist_pos(gen);
		const double y0 = dist_pos(gen);
		const double theta = dist_theta(gen);

		const double dx = static_cast<double>(std::sin(theta));
		const double dy = static_cast<double>(std::cos(theta));

		const double x1 = x0 + dx;
		const double y1 = y0 + dy;

		matchsticks[i] = Matchstick {x0, y0, x1, y1, crosses_grid_line(y0, y1, 2)};
	}
}

void print_matchsticks(MatchstickContainer const& matchsticks, const size_t n)
{
	for (size_t i = 0; i < n; ++i) {
		const auto& m = matchsticks[i];
		std::printf("%f %f %f %f %d\n", m.x0, m.y0, m.x1, m.y1, m.c ? 1 : 0);
	}
}

MatchstickContainer& allocate_initial() noexcept
{
	const auto matchsticks_ptr = static_cast<MatchstickContainer*>(
		mmap(0, sizeof(MatchstickContainer), PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_POPULATE, -1, 0)
	);

	if (matchsticks_ptr == MAP_FAILED) [[unlikely]] {
		std::fprintf(stderr, "out of memory\n");
		std::exit(1);
	}

	madvise(matchsticks_ptr, sizeof(MatchstickContainer), MADV_HUGEPAGE|MADV_WILLNEED|MADV_SEQUENTIAL);

	return *matchsticks_ptr;
}

size_t handle_matchsticks(MatchstickContainer& matchsticks, const size_t n, std::mt19937& gen) noexcept
{
	generate_matchsticks(matchsticks, n, gen);

	if constexpr (PRINT_RESULTS) {
		print_matchsticks(matchsticks, n);
	}

	size_t crosses_grid = 0;

	for (size_t i = 0; i < n; ++i) {
		crosses_grid += matchsticks[i].c ? 1 : 0;
	}

	return crosses_grid;
}

int main(const int argc, const char** argv) {
	if (argc != 2) [[unlikely]] {
		std::fprintf(stderr, "usage: %s <sample size>\n", argv[0]);
		return 1;
	}

	const size_t n = std::strtoull(argv[1], nullptr, 10); // max confirfmed to work: 10'000'000'000;
	size_t crosses_grid = 0;

	if (n <= 0) [[unlikely]] {
		std::fprintf(stderr, "n must be larger than 0\n");
		return 1;
	}

	// use a single memory area for the entire thing
	MatchstickContainer& matchsticks = allocate_initial();

	// use a single rng for the entire thing
	std::random_device rd;
	std::mt19937 gen(rd());

	// handle matchtics by MAX_SINGLE_ROUNDS at a time (prevent OOM for too large n)
	for (size_t i = 0; i < n / MAX_SINGLE_ROUNDS; ++i) {
		crosses_grid += handle_matchsticks(matchsticks, MAX_SINGLE_ROUNDS, gen);
	}

	// handle the "remainder"
	crosses_grid += handle_matchsticks(matchsticks, n % MAX_SINGLE_ROUNDS, gen);

	const long double pi_estimate = static_cast<long double>(n) / crosses_grid;

	std::printf("π estimate: %zu/%zu (≈ %Lf), err = %Lf\n", n, crosses_grid, pi_estimate, M_PI - pi_estimate);
}
