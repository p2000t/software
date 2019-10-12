
; 9600 baud!!!

BasicProgStart      .equ    $6547
ProgramBlocks       .equ    $9f4f ; byte
ProgramLength       .equ    $9f34 ; word

    .org $9e00

; reads a byte from the serial port (9600 baud) and returns in A
read_byte:
    push bc                 ; C5 [11]
check_start_bit:
    in a,($20)              ; DB 20 [11]
    and $01                 ; E6 01 [7] - check if bit D0 is 0
    jr nz, check_start_bit  ; 20 FA [7] 
    ld b, $15               ; 06 15 [7]
delay_on_start_bit:
    djnz delay_on_start_bit ; 10 FE [13/8]
    ld b, $08               ; 06 08 [7]

read_next_bit:
    in a,($20)              ; DB 20 [11]

    ; 58 clocks without extra delay
    ; 1.2 * 1041.67 = 1250. Need delay in B: 
    ; 2400 baud: (1250 - 58) / 13 = 91,7 + 1 = 93 (&h5D)

    ; 4800 baud: 1.2 * 520.84 = 625
    ; delay in B: (625 - 58) / 13 = 43,62 + 1 = 45 (&h2D)

    ; 9600 baud: 1.2 * 260.42 = 312.5
    ; delay in B: (312.5 - 58) / 13 = 19.6 + 1 = 21 (&h15)

    rra                     ; 1F [4] - bit 0 into carry
    rr c                    ; CB 19 [8]
    push bc                 ; C5 [11]
    ld b, $10               ; 06 10 [7]
delay_bit:
    djnz delay_bit          ; 10 FE [13/8]
    pop bc                  ; C1 [10]
    djnz read_next_bit      ; 10 F3 [13]

    ; 72 clocks without extra delay. So delay in B: 
    ; 2400 baud: (1041.67 - 72) / 13 = 74.6 + 1 = 76 (&h4C)
    ; 4800 baud: (520.84 - 72) / 13 = 34.53 + 1 = 35 (&h23)
    ; 9600 baud: (260.42 - 72) / 13 = 14.49 + 1 = 16 (&h10)

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
    ld hl, BasicProgStart   ; 21 47 65 - IDEA: read pointer from $625c?
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

    ; reset the pointers to end of memory for BASIC
    ld a, ($63b9)           ; 3A B9 63
    add a, 2                ; C6 02
    ld ($63b9), a           ; 32 B9 63
    ld ($6259), a           ; 32 59 62

    ; succes: play beep
    ld a,$07                ; 3E 07
    call $104a              ; CD 4A 10

    ei                      ; FB - enable interrupts
    ret                     ; C9

