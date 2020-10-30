x [*] :=
 1  0
 2  0
 3  0
 4  0
 5  0
 6  0
 7  0
 8  1
 9  1
10  0
11  0
12  0
13  0
14  0
15  0
16  0
17  0
18  0
19  0
;

y [*,*] (tr)
:    1   2   3   4   5   6   7    :=
1    0   0   0   0   0   0   0
2    0   0   0   0   0   0   0
3    0   0   0   0   0   0   0
4    0   0   0   0   0   0   0
5    0   0   0   0   0   0   0
6    0   0   0   0   0   0   0
7    0   0   0   0   0   0   0
8    1   1   1   1   1   0   1
9    0   0   0   0   0   1   0
10   0   0   0   0   0   0   0
11   0   0   0   0   0   0   0
12   0   0   0   0   0   0   0
13   0   0   0   0   0   0   0
14   0   0   0   0   0   0   0
15   0   0   0   0   0   0   0
16   0   0   0   0   0   0   0
17   0   0   0   0   0   0   0
18   0   0   0   0   0   0   0
19   0   0   0   0   0   0   0
;

sum{i in CUSTOMERS, j in FACILITIES} distance[j,i]*y[i,j]*routing_cost*30/
  3600 = 63.5

sum{j in FACILITIES} fixcost[j]*x[j] = 580

