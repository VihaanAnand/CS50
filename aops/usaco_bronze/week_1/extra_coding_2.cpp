#include <iostream>
#include <vector>
using namespace std;
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        int n, k;
        cin >> n >> k;
        vector<int> c(n);
        for (int i = 0; i < n; i++) {
                cin >> c[i];
        }
        vector<int> final(n, -1);
        for (int i = n - 1; i >= 0; i--) {
                int next = i + c[i];
                if (next >= n) {
                        final[i] = i;
                }
                else {
                        final[i] = final[next];
                }
        }
        int count = 0;
        for (int i = 0; i < k; i++) {
                if (final[i] == final[0]) {
                        count++;
                }
        }
        cout << count << "\n";
}