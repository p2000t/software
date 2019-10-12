BaudRate        .equ    $6016

.org $9000
ptr:            .word   0
numchars:       .word   0

.org $9010
start:  ld      hl,(ptr)
        ld      de,(numchars)
loop:   ld      c,(hl)
        call    print
        inc     hl
        dec     de
        ld      a,d
        or      e
        jr      nz,loop
        ret

print:  push    bc
        push    de
        scf
        ccf
        ld      d,$0A
        di
pri1:   ld      a,$C0
        jr      nc,pri2
        res     7,a
pri2:   out     ($10),a
        ld      b,$49
        ld      a,(BaudRate)
        res     7,a
        inc     a
pri3:   djnz    pri3
        ld      b,$4E
        dec     a
        add     a,$00
        jr      nz,pri3
        scf
        rr      c
        dec     d
        jr      nz,pri1
        ld      b,a
pri4:   djnz    pri4
        ei
        pop     de
        pop     bc
        ret

.end

