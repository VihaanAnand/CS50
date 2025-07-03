#include <cmath>
#include <iostream>
#include <vector>
using namespace std;
int main() {
        ios_base::sync_with_stdio(false);
        cin.tie(0);
        int n, e;
        cin >> n >> e;
        vector<string> conveyors(n);
        for (int i = 0; i < n; i++) {
                cin >> conveyors[i];
        }
        vector<int> results(1 << n, e / (1 << n));
        for (int i = 0; i < (e % (1 << n)); i++) {
                int col = 0;
                for (int row = 0; row < n; row++) {
                        int newcol;
                        if (conveyors[row][col] == '>') {
                                newcol = 2 * col + 1;
                        }
                        else {
                                newcol = 2 * col;
                        }
                        if (conveyors[row][col] == '>') {
                                conveyors[row][col] = '<';
                        }
                        else {
                                conveyors[row][col] = '>';
                        }
                        col = newcol;
                }
                results[col]++;
        }
        for (int i = 0; i < results.size(); i++) {
                if (i == results.size() - 1) {
                        cout << results[i];
                }
                else {
                        cout << results[i] << " ";
                }
        }
        cout << "\n";
}