; This routine reads the next record (header + data payload) from the P2000 cassette
; - the header is read into $6030 - $604F
; - the 1024 bytes data payload is read into a RAM Buffer ($9400 - $97FF)

Tape    .equ    $0018           ; Monitor's cassette routine address

.org $9100
first   .byte   0               ; contains 0 the first time, which trigeers a rewind

.org $9110
start:  ld      a,(first)    
        or      0             
        jr      nz,no_rewind    ; if (first) != 0, skip rewinding the tape
        ld      a,1             
        ld      (first),a       ; make sure rewind is only done once
        call    Tape            ; when A contains 1, calling Tape ($0018) rewinds the cassette
no_rewind:
        ld      hl,Buffer 
        ld      ($6030),hl      ; sets data transfer address to the RAM Buffer at $9400 - instead of BASIC's default $6547
        ld      hl,$400         
        ld      ($6032),hl      ; need to read 1024 bytes of data
        ld      a,6 
        call    Tape            ; when A contains 6, calling Tape ($0018) reads a cassette block (header + data)
        ret

.org    $9400
Buffer: .byte   0               ; 1024 bytes of buffer

.end
