- valores finais dos registradores e posição de memória
r16 = 1
r17 = 11
r18 = 100
r19 = 1
r20 = 1
r21 = 0000

0x03B = 1
0x03C = 11
0x03D = 100


first:
    LDR r16, [x]
    LDR r17, [x+1]
    ADD r18, r16, r17
    STR r18, [y]
    B second

third:
    AND r21, r18, r17
    CBZ r21, end



second:
    AND r19, r16, r17
    ORR r20, r19, r20
    B third

end:
    STOP