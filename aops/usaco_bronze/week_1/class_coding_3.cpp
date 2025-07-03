#include <iostream>
using namespace std;
// https://math.stackexchange.com/questions/3400630/fast-calculation-of-fibonacci-numbers
pair<long long, long long> fib(long long n, long long j0, long long j1, long long mod) {
        if (n == 0) {
                return {0, 1};
        }
        auto [a, b] = fib(n / 2, j0, j1, mod);
        long long c = (a * (b * 2 - a)) % mod;
        if (c < 0) {
                c += mod;
        }
        long long d = (a * a + b * b) % mod;
        if (n % 2 == 0) {
                return {c, d};
        }
        else {
                return {d, (c + d) % mod};
        }
}
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        long long j0, j1, n, k;
        cin >> j0 >> j1 >> n >> k;
        long long mod = 1000;
        if (k == 1) {
                mod = 10;
        }
        else if (k == 2) {
                mod = 100;
        }
        long long fn = fib(n, j0, j1, mod).first;
        long long fn1 = fib(n - 1, j0, j1, mod).first;
        cout << (j0 * fn1 + j1 * fn) % mod << "\n";
}