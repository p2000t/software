Tape    .equ    $0018

.org $9100
first   .byte   0

.org $9110
start:  ld      a,(first)
        or      0
        jr      nz,no_rewind
        ld      a,1
        ld      (first),a
        call    Tape
no_rewind:
        ld      hl,Buffer
        ld      ($6030),hl
        ld      hl,$400
        ld      ($6032),hl
        ld      a,6
        call    Tape
        ret

.org    $9400
Buffer: .byte   0

.end

