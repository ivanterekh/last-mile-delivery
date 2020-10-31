set FACILITIES;#identification m facilities (satellites)
set CUSTOMERS;#identification n customers
set DEPOTS;#identification of nn depots (CDC)

param supply {FACILITIES}>=0;#supply capacity bi of facilities
param demand {CUSTOMERS}>=0;#customers’ demands aj
param costijk {FACILITIES,CUSTOMERS,DEPOTS}>=0;#cost cijk of facility i, from depot k to customer j
param costik {FACILITIES, DEPOTS}>=0;     #cost of assigning facility to depot k
param costk {DEPOTS}>=0;#cost of opening depot k

var x { FACILITIES, CUSTOMERS,DEPOTS} binary;#xijk=1 customer j allocated to facility j serviced from depot k
var y {FACILITIES,DEPOTS} binary;#yik =1 facility i open and served from depot k
var z {DEPOTS}binary;#zk=1 depot k is open

minimize Total_Cost:
    sum{i in FACILITIES, j in CUSTOMERS, k in DEPOTS } costijk[i,j,k]*x[i,j,k]+sum{i in FACILITIES, k in DEPOTS} costik[i,k]*y[i,k]+sum{k in DEPOTS} costk[k]*z[k];

subject to capacity_constraint {i in FACILITIES, k in DEPOTS}:
    sum {j in CUSTOMERS} demand[j]*x[i,j,k]<=supply[i];

subject to customer_allocation {j in CUSTOMERS}:
    sum {i in FACILITIES, k in DEPOTS} x[i,j,k]=1;

subject to customer_facility{i in FACILITIES, j in CUSTOMERS, k in DEPOTS}:
    x[i,j,k]<=y[i,k];

subject to facility_depot{i in FACILITIES, k in DEPOTS}:
    y[i,k]<=z[k];
