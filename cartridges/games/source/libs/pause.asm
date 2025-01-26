PAUSE_FLAG: EQU $6090       ; flag to indicate if game is paused
PAUSE_ROW:  EQU 12          ; row on screen to display pause message
LINE_STORE: EQU $60A0       ; memory to store current line

    ; This code is used to pause the game. It will display a message on the 
    ; screen and wait until the pause button is pressed again to continue.

    ; !! NMI code must start at location $1016 !!
address_0x1016:
    call pause_saveregs     ; save registers
    call check_pause
    jr z, pause             ; if pause flag not set, jump to pause
    call clear_pause        ; second press -> unpause by clearing pause flag
    jp restore_and_return
pause:
    call set_pause
    call $0032              ; call beep
    call show_pause_message ; show pause message
pause_loop:
    call check_pause
    jr nz,pause_loop        ; wait until pause is cleared
    call clear_pause_message
restore_and_return:
    call pause_restoreregs
    retn                    ; return from NMI

clear_pause:
    xor a
ld_pause_a:
    ld (PAUSE_FLAG),a
    ret

set_pause:
    ld a, 1
    jr ld_pause_a

check_pause:
    ld a, (PAUSE_FLAG)
    or a
    ret

show_pause_message:
    ; copy current line to LINE_STORE memory
    ld hl, $5000 + $50*PAUSE_ROW
    ld de, LINE_STORE
    ld bc, 40               ; full line has 40 characters
    ldir
    ; copy message to screen
    ld hl, PAUSE_MSG
    ld de,$5000 + $50*PAUSE_ROW
    ld bc, 40               ; message has 40 characters
    ldir
    ret
PAUSE_MSG:
    DB $04,$1D,$0D,$03,"PAUZE -",$08,"druk nogmaals voor verder   "

clear_pause_message:
    ld hl, LINE_STORE
    ld de, $5000 + $50 * PAUSE_ROW
    ld bc, 40               ; line has 40 characters
    ldir
    ret

pause_saveregs:   
    ex (sp),hl              ; put HL on, and get return address off, the stack
    push de 
    push bc 
    push af 
    jp (hl)                 ; jump back to where we came from (address is in HL) 

pause_restoreregs:    
    pop hl                  ; calling address off stack  
    pop af                  ; restore other registers
    pop bc  
    pop de  
    ex (sp),hl              ; gets old HL and puts call address back on stack
    ret                     ; return there! 