param N;
param M;
param L;

set FACILITIES = {1..N};#identification m facilities (satellites)
set CUSTOMERS = {1..M};#identification n customers
set DEPOTS = {1..L};#identification of nn depots (CDC)

param capacity {FACILITIES}>=0;#capacity capacity bi of facilities
param demand {CUSTOMERS}>=0;#customers’ demands aj
param dist_from_sat {FACILITIES,CUSTOMERS}>=0;#cost cijk of facility i, from depot k to customer j
param dist_from_dep {DEPOTS, FACILITIES}>=0;     #cost of assigning facility to depot k
param cost_dep {DEPOTS}>=0;#cost of opening depot k

param cost_from_sat;
param cost_from_dep;

var x { FACILITIES, CUSTOMERS} binary;#xijk=1 customer j allocated to facility j serviced from depot k
var y {FACILITIES,DEPOTS} binary;#yik =1 facility i open and served from depot k
var z {DEPOTS}binary;#zk=1 depot k is open

minimize Total_Cost:
    sum{i in FACILITIES, j in CUSTOMERS, k in DEPOTS } x[i,j]*dist_from_sat[i,j]*30/3600*cost_from_sat+sum{i in FACILITIES, k in DEPOTS} y[i,k]*dist_from_dep[k,i]*cost_from_dep+sum{k in DEPOTS} cost_dep[k]*z[k];

subject to capacity_constraint {i in FACILITIES, k in DEPOTS}:
    sum {j in CUSTOMERS} demand[j]*x[i,j]<=capacity[i];

subject to customer_allocation {j in CUSTOMERS}:
    sum {i in FACILITIES} x[i,j]=1;

subject to facilities_allocation {i in FACILITIES}:
    sum {k in DEPOTS} y[i,k]=1;

subject to facility_depot{i in FACILITIES, k in DEPOTS}:
    y[i,k]<=z[k];

subject to one_depot:
    sum{k in DEPOTS} z[k] = 1;
