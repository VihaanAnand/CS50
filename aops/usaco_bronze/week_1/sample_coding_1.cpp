// #include <bits/stdc++.h>
#include <iostream>
using namespace std;
const int MAX_SIZE = 100000;
int ais[MAX_SIZE];
int sorted_ais[MAX_SIZE];
typedef long long ll;

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(0);
  int n, ai;
  cin >> n;
  for (int i = 0; i < n; ++i) {
    cin >> ai;
    ais[i] = ai;
    sorted_ais[i] = ai;
  }
  sort(sorted_ais, sorted_ais + n);
  ll total = 0;
  for (int i = 0; i < n; ++i) {
    if (ais[i] != sorted_ais[i]) {
      total++;
    }
  }
  cout << total << '\n';
}