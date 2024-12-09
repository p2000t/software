
;
; pc2p2000t is a utility to load a .cas file from a PC (via serial RS-232)
; into the P2000T. As most modern PCs don't have a serial connection, you'll
; need a USB-to-serial adapter cable.
; pc2p2000t expects 9600 baud, 1 start bit, 8 data bits and 1 stop bit.
; For more information, please see:
; https://github.com/p2000t/software/tree/master/utilities/pc2p2000t
;
; Note: I used https://www.asm80.com/onepage/asmz80.html for Z80 assembling

BasicProgStart      .equ    $6547
ProgramBlocks       .equ    $9f4f ; word
ProgramLength       .equ    $9f34 ; word
TransferAddress     .equ    $9f30 ; word

    .org $9e00

; reads a byte from the serial port (9600 baud) and returns in A
read_byte:
    push bc                 ; C5 [11]
check_start_bit:
    in a,($20)              ; DB 20 [11]
    and $01                 ; E6 01 [7] - check until bit D0 is 0 (start bit)
    jr nz, check_start_bit  ; 20 FA [7] 
    ld b, $15               ; 06 15 [7] - used for delay after start bit (*)
delay_on_start_bit:
    djnz delay_on_start_bit ; 10 FE [13/8]
    ld b, $08               ; 06 08 [7] - call read_next_bit for 8 data bits

    ; (*)
    ; There are 47 CPU clocks between check_start_bit and read_next_bit, when
    ; register B is 1 (so without additional delay). But we need to spend/burn 
    ; additional CPU clocks to make sure that read_next_bit is picking up the
    ; correct next bit from the serial port at the right time.

    ; We're expecting 9600 baud, which is 9600 bits per second. So every
    ; bit's signal is available for 1/9600 = 104.17 microseconds.
    ; The P2000T has a 2.5Mhz CPU, so 104.17 microseconds = 260.4 CPU clock
    ; cycles (104.17 / 0.4).
    ; Now after receiving the start bit we need to wait slightly more (say 20%)
    ; than 260.4 CPU clock cycles, so that the next reading of port &H20 will 
    ; be nicely within the next RS-232 bit signal.
    ; We can spend/burn CPU cycles by increasing the B register, because every 
    ; additional djnz check adds 13 CPU cycles, so we calculate B:
    ;   B = (1.2*260.4 - 47) / 13 = 20.42 + 1 (alreaydy in B) = 21 ($15)
    ;
    ; for 2400 baud we need B = (1.2*1041.67 - 47)/ 13 = 92.54 + 1 = 93 ($5D)
    ; for 4800 baud we need B = (1.2*520.8 - 47) / 13 = 44.46 + 1 = 45 ($2D)
    ; for 9600 baud we need B = (1.2*260.4 - 47) / 13 = 20.42 + 1 = 21 ($15)

read_next_bit:
    in a,($20)              ; DB 20 [11]
    rra                     ; 1F [4] - bit 0 into carry
    rr c                    ; CB 19 [8]
    push bc                 ; C5 [11]
    ld b, $10               ; 06 10 [7] - used for delay between data bits (**)
delay_bit:
    djnz delay_bit          ; 10 FE [13/8]
    pop bc                  ; C1 [10]
    djnz read_next_bit      ; 10 F3 [13]

    ; (**)
    ; 72 CPU clocks between port reads without extra delay. So we calculate B2: 
    ; 2400 baud: (1041.67 - 72) / 13 = 74.6 + 1 = 76 ($4C)
    ; 4800 baud: (520.84 - 72) / 13 = 34.53 + 1 = 36 ($24)
    ; 9600 baud: (260.42 - 72) / 13 = 14.49 + 1 = 16 ($10)

    ld a,c                  ; 79 [4]
    pop bc                  ; C1 [10]
    ret                     ; C9 [10]

read_program:               ; starts at $9E1D
    di                      ; F3 - disable interrupts

read_header:                ; read 256-byte header into $9f00 - $9fff
    ld b,0                  ; 06 00
    ld hl, $9f00            ; 21 00 9F
read_header_loop:
    call read_byte          ; CD 00 9E
    ld (hl),a               ; 77
    inc hl                  ; 23
    djnz read_header_loop   ; 10 F9

    ;read the blocks and put into basic memory
    ld hl, ProgramBlocks    ; 21 4F 9F
    ld c, (hl)              ; 4E - load number of blocks into C
    ld hl,(TransferAddress) ; 2A 30 9F - loads transfer address into hl
    jr read_block           ; 18 07 - first header already read, so skip
ignore_header:
    ld b, $00               ; 06 00 - ignore later 256-byte headers
ignore_header_loop:
    call read_byte          ; CD 00 9E
    djnz ignore_header_loop ; 10 FB
read_block:
    ld de, $400             ; 11 00 04
read_block_loop:
    call read_byte          ; CD 00 9E
    ld (hl),a               ; 77
    inc hl                  ; 23
    dec de                  ; 1B
    ld a,d                  ; 7A
    or e                    ; B3
    jr nz, read_block_loop  ; 20 F6
    dec c                   ; 0D
    jr nz, ignore_header    ; 20 E9

    ld de, BasicProgStart   ; 11 47 65 
    ld hl, (ProgramLength)  ; 2A 34 9F
    add hl,de               ; 19
    ld ($6405), hl          ; 22 05 64 - set basic pointers to var space
    ld ($6407), hl          ; 22 07 64
    ld ($6409), hl          ; 22 09 64

    ; succes: play beep
    ld a,$07                ; 3E 07
    call $104a              ; CD 4A 10

    ei                      ; FB - enable interrupts
    ret                     ; C9

write_to_cas_loop:          ; starts at $9E61
    call read_program       ; CD 1D 9E

    ; copy block of 32 bytes at TransferAddress to $6030 (hl -> de)
    ld hl, TransferAddress  ; 21 30 9F
    ld de, $6030            ; 11 30 60
    ld bc, $20              ; 01 20 00
    ldir                    ; ED B0

    ; write program out to cassette
    ld a, $5                ; 3E 05 - 5 is command number for write
    call $0018              ; CD 18 00 - call cass write
    jp write_to_cas_loop    ; C3 61 9E