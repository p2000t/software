; This routine sends a specified number of bytes [numchars] found in memory location (ptr) to the serial/printer port as RS232 signal.
; Note that RS232 sends a byte bit-by-bit, LSB (least significant bit) first and MSB (most significant bit) last.
; Also note that when using the OUT instruction on port $10 (serial data out), a logical 0 is indicated by setting bit 7 of register A
; and a logical 1 is indicated by clearing bit 7 of A. This is exactly then opposite when using the IN instruction and bit 0 of A.

BaudRate        .equ    $6016   ; contains the configured serial baudrate (set as '0' by SERIAL.BAS = 2400 Bd)

.org $9000
ptr:            .word   0       ; pointer to address containing the data to send
numchars:       .word   0       ; number of bytes to write

.org $9010
start:  ld      hl,(ptr)        ; HL now contains pointer to data address
        ld      de,(numchars)   ; DE now contains (remaining) number of bytes to send
loop:   ld      c,(hl)          ; load next byte of data from pointer HL into C
        call    print           ; print this byte (i.e., send to serial OUT)
        inc     hl      
        dec     de              ; move to next byte
        ld      a,d
        or      e
        jr      nz,loop         ; if DE (remaining number of bytes) == 0, exit loop
        ret

; sends the byte in register C to the serial port (i.e., print)
print:  push    bc              
        push    de              ; push values in BC and DE to stack (so registers can be reused)
        scf                     ; set carry flag...
        ccf                     ; ...and invert (so unsets) carry flag. note that "or a" also would have cleared the carry flag
        ld      d,$0A           ; run pri1 10 times (1 start bit + 8 data bits + 1 end bit)
        di                      ; disable interrupts
pri1:   ld      a,$C0           ; load %11000000 into A. Note: I suspect that %10000000 ($80) would also work
        jr      nc,pri2         ; skip resetting bit 7 of A if carry clear
        res     7,a             ; carry set? A = %01000000. carry unset? A = %11000000
pri2:   out     ($10),a         ; writes MSB (i.e. left bit) of A to port $10 (serial data out)
        ld      b,$49           ; set next delay-loop counter
        ld      a,(BaudRate)    ; load BaudRate value into A (%000 = 2400 Bd, %001 = 1200 Bd, %011 = 600 Bd, %111 = 300 Bd, etc.)
        res     7,a             ; clear possibly set non-automatic CR+LF bit
        inc     a               ; increment A to get pri3 delay loop working correctly
pri3:   djnz    pri3            ; perform delay loop for correct RS232 signal timing
        ld      b,$4E           ; set next delay-loop counter
        dec     a               ; decrement A to check if we can break the pri3 delay-loop
        add     a,$00           ; this will just populate the zero flag using value in A
        jr      nz,pri3         ; the lower the BaudRate (= higher value in A), the more often pri3 delay-loop is called
        scf                     ; set carry flag to force correct stop-bit
        rr      c               ; C is bit-rotated to right. the bit leaving is copied the carry
        dec     d               ; another bit was sent out, so decrement d
        jr      nz,pri1         ; already 10 bits sent out?
        ld      b,a             ; puts remainer of A into B for the endbit's delay loop
pri4:   djnz    pri4            ; perform endbit's delay loop
        ei                      ; enable interrupts again
        pop     de
        pop     bc              ; pop values bc and de from stack
        ret

.end
