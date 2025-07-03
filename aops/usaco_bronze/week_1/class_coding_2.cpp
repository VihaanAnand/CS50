#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        int n;
        cin >> n;
        vector<int> fis(n);
        for (int i = 0; i < n; i++) {
                cin >> fis[i];
        }
        sort(fis.begin(), fis.end());
        int num_standing = 0;
        for (int i = 0; i < n; i++) {
                if (fis[i] <= num_standing) {
                        num_standing++;
                }
        }
        cout << num_standing << "\n";
}