#include <iostream>
using namespace std;
int position(int p, int r, int k) {
        if (k % 2 == 1) {
                return (k + r) % p;
        }
        return (k - r + p) % p;
}
int revpos(int p, int r, int pos, int parity) {
        int result;
        if (parity == 1) {
                result = (pos - r + p) % p;
        }
        else {
                result = (pos + r) % p;
        }
        if (result == 0) {
                return p;
        }
        return result;
}
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        int p, r, k;
        cin >> p >> r >> k;
        r %= p;
        int pos = position(p, r, k);
        int leftpos = (pos - 1 + p) % p;
        int rightpos = (pos + 1) % p;
        int leftnum = revpos(p, r, leftpos, (k + 1) % 2);
        int rightnum = revpos(p, r, rightpos, (k + 1) % 2);
        cout << leftnum << " " << rightnum << "\n";
}