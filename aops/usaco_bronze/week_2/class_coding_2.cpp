#include <iostream>
#include <vector>
using namespace std;
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        long long r, c;
        cin >> r >> c;
        vector<vector<long long>> a(r, vector<long long>(c));
        for (long long i = 0; i < r; i++) {
                for (long long j = 0; j < c; j++) {
                        cin >> a[i][j];
                }
        }
        long long maxval = -4000000001;
        for (int i = 0; i < r - 1; i++) {
                for (int k = i + 1; k < r; k++) {
                        vector<long long> col_sum(c);
                        for (int j = 0; j < c; j++) {
                                col_sum[j] = a[i][j] + a[k][j];
                        }
                        long long max1 = col_sum[0];
                        for (int j = 1; j < c; j++) {
                                if (max1 + col_sum[j] > maxval) {
                                        maxval = max1 + col_sum[j];
                                }
                                if (col_sum[j] > max1) {
                                        max1 = col_sum[j];
                                }
                        }
                }
        }
        cout << maxval << "\n";
}