#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;
bool troublesort(vector<int> &a) {
        bool changed = false;
        for (int i = 0; i < a.size() - 2; i++) {
                if (a[i] > a[i + 2]) {
                        swap(a[i], a[i + 2]);
                        changed = true;
                }
        }
        return changed;
}
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        int n;
        cin >> n;
        vector<int> a(n);
        vector<int> even, odd;
        for (int i = 0; i < n; i++) {
                cin >> a[i];
                if (i % 2 == 0) {
                        even.push_back(a[i]);
                }
                else {
                        odd.push_back(a[i]);
                }
        }
        sort(even.begin(), even.end());
        sort(odd.begin(), odd.end());
        for (int i = 0; i < n; i++) {
                if (i % 2 == 0) {
                        a[i] = even[i / 2];
                }
                else {
                        a[i] = odd[i / 2];
                }
        }
        for (int i = 0; i < n - 1; i++) {
                if (a[i] > a[i + 1]) {
                        cout << i << "\n";
                        return 0;
                }
        }
        cout << n << "\n";
}