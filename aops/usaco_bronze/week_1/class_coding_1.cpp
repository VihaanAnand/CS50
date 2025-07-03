#include <iostream>
#include <set>
using namespace std;
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        long long n;
        cin >> n;
        if (n == 0) {
                cout << "-1\n";
                return 0;
        }
        long long current_number = n;
        set<char> digits_seen;
        while (true) {
                for (char c : to_string(current_number)) {
                        digits_seen.insert(c);
                }
                if (digits_seen.size() == 10) {
                        cout << current_number << "\n";
                        return 0;
                }
                current_number += n;
        }
}