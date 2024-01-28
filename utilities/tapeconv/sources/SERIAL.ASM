; This routine sends a specified number of bytes [numchars] found in memory location (ptr) to the serial/printer port as RS232 signal.
; Note that RS232 sends a byte bit-by-bit, LSB (least significant bit) first and MSB (most significant bit) last.
; Also note that when using the OUT instruction on port $10 (serial data out) the bits are sent inverted. So sending a logical 0 is 
; done by setting bit 7 of register A. For a logical 1, bit 7 of A needs to be cleared. This is exactly then opposite when using 
; the IN instruction and bit 0 of A.
; For each byte, 10 bits are ouputted to port $10: 1 start bit (1), 8 data bits (inverted) and 1 stop bit (0)

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
        ccf                     ; ...and toggle (so resets) carry flag. note that "or a" also would have cleared the carry flag
        ld      d,$0A           ; run pri1-loop 10 times (1 start bit + 8 data bits + 1 end bit)
        di                      ; disable interrupts
pri1:   ld      a,$00           ; [7] A=0
        ccf                     ; [4] Complement/toggle Carry
        rra                     ; [4] Rotate the Carry into bit 7
        jp      pri2            ; [10] Burn 10 T-states for RS-232 timing purposes
pri2:   out     ($10),a         ; [11] writes MSB (i.e. left bit) of A to port $10 (serial data out)
        ld      b,$0f           ; [7] set the delay-loop counter for RS-232 timing 
pri3:   djnz    pri3            ; [13/8] perform delay loop for correct RS232 signal timing (waits 14x13+8 T-states)
        scf                     ; [4] set carry flag, so bit 7 of C will is set after 'rr'. This is the stop-bit
        rr      c               ; [8] C is bit-rotated to right. the bit leaving is copied the carry
        dec     d               ; [4] another bit was sent out, so decrement d
        jr      nz,pri1         ; [12/7] already 10 bits sent out?
        ei                      ; [4] enable interrupts again
        pop     de              ; [10]
        pop     bc              ; [10] pop values bc and de from stack
        ret                     ; [10]
.end
