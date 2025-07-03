#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        long long m, n;
        cin >> m >> n;
        vector<long long> g(m);
        for (long long i = 0; i < m; i++) {
                cin >> g[i];
        }
        sort(g.begin(), g.end());
        vector<long long> h(n);
        for (long long i = 0; i < n; i++) {
                cin >> h[i];
        }
        sort(h.begin(), h.end());
        long long mindiff = 1000000000000000001;
        for (long long i = 0; i < m; i++) {
                long long pos = lower_bound(h.begin(), h.end(), g[i]) - h.begin();
                if (pos < n) {
                        long long diff = abs(g[i] - h[pos]);
                        if (diff < mindiff) {
                                mindiff = diff;
                        }
                }
                if (pos > 0) {
                        long long diff = abs(g[i] - h[pos - 1]);
                        if (diff < mindiff) {
                                mindiff = diff;
                        }
                }
        }
        cout << mindiff << "\n";
}