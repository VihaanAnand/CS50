#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;
bool compare(const vector<int>& a, const vector<int>& b) {
        if (a[0] != b[0]) {
                return a[0] < b[0];
        }
        return a[1] > b[1];
}
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        int n;
        cin >> n;
        vector<int> start(n);
        for (int i = 0; i < n; i++) {
                cin >> start[i];
        }
        vector<int> end(n);
        for (int i = 0; i < n; i++) {
                cin >> end[i];
        }
        vector<vector<int>> times(2 * n, vector<int>(2));
        for (int i = 0; i < n; i++) {
                times[2 * i] = {start[i], 1};
                times[2 * i + 1] = {end[i], -1};
        }
        sort(times.begin(), times.end(), compare);
        int max_cows = 0;
        int cows = 0;
        for (int i = 0; i < 2 * n; i++) {
                cows += times[i][1];
                if (cows > max_cows) {
                        max_cows = cows;
                }
        }
        cout << max_cows << "\n";
}