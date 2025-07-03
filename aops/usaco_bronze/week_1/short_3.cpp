#include <iostream>
using namespace std;
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        int n;
        cin >> n;
        int count = 1;
        for (count = 1; n != 1; count++) {
                if (n % 2 == 0) {
                        n /= 2;
                }
                else {
                        n *= 3;
                        n += 1;
                }
        }
        cout << count << "\n";
}