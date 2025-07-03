#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        int n;
        cin >> n;
        if (n == 1) {
                cout << "-1\n";
                return 0;
        }
        vector<int> x(n);
        for (int i = 0; i < n; i++) {
                cin >> x[i];
        }
        sort(x.begin(), x.end());
        for (int i = 0; i < n; i++) {
                if (x[i + 1] - x[i] > 1) {
                        cout << x[i] + 1 << "\n";
                        return 0;
                }
        }
        cout << "-1\n";
}