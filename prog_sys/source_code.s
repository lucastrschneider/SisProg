START 0x030
 
first:
LDUR r16, var1
LDUR r17, var2
ADD r18, r16, r17
STUR r18, var3
B second
 
third:
AND r21, r18, r17
CBZ r21, fourth
 
second:
AND r19, r16, r17
ORR r20, r19, r20
B third
 
fourth:
END
 
var1:
   word 1
var2:
   word 3
var3:
   word 0
 
