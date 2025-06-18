#include <algorithm>
#include <iostream>
#include <set>
using namespace std;
int main() {
        int k;
        cin >> k;
        set<int> squbes;
        for (int i = 1; i <= k; i++) {
                for (int j = 1; j <= k; j++) {
                        if (i != j) {
                                int sqube = i * i + j * j * j;
                                squbes.insert(sqube);
                        }
                }
        }
        auto first = squbes.begin();
        auto kth = next(first, k - 1);
        cout << *kth << "\n";
}