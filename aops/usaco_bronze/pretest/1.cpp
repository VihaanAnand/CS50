#include <iostream>
#include <vector>
using namespace std;
int main() {
        int n, k;
        cin >> n >> k;
        vector<int> array(n);
        for (int i = 1; i <= n; i++) {
                array[i - 1] = i * i;
        }
        for (int i = 0; i < k; i++) {
                int index = 0;
                int max = 0;
                for (int j = 0; j < n; j++) {
                        if (array[j] >= max) {
                                index = j;
                                max = array[j];
                        }
                }
                array[index] /= 2;
        }
        cout << array[n - 3] << " " << array[n - 2] << " " << array[n - 1] << "\n";
}