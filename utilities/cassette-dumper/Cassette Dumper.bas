0 REM Cassette Dumper 2.0
5 T=0 : M=&H9010
10 A=0
20 READ A$
30 IF A$="next" THEN M=&H9110 : GOTO 10
35 IF A$="stop" THEN GOTO 70
40 P=VAL("&h"+A$) : POKE M+A,P
50 A=A+1 : T=T+P
60 GOTO 20
70 IF T=7304 THEN GOTO 72
71 PRINT"Typfout gemaakt in DATA":END
72 PRINT"Voer nu de cassette in die gedumpt"
73 PRINT"moet worden en druk een toets ..."
74 WACHT=INP("")
79 T=0:POKE &H9100,0
80 DEF USR=&H9110:PRINT"Lezen cassette ..."
81 POKE &H6034,0:POKE &H6035,4:A=USR (0)
82 F=PEEK(&H6017):IF F<>0 THEN GOTO 100
83 POKE &H9000,&H00:POKE &H9001,&H60
84 POKE &H9002,0:POKE &H9003,1
85 T=T+1:PRINT"Zenden blok";T;"..."
86 DEF USR=&H9010:A=USR(0)
87 POKE &H9000,0:POKE &H9001,&H94
88 POKE &H9002,0:POKE &H9003,4
89 A=USR (0)
90 GOTO 80
100 IF F=69 OR F=77 THEN PRINT"Dumper klaar":END
110 PRINT"Cassette fout ";CHR$(F):END
1000 DATA 2a,00,90,ed,5b,02,90,4e,cd,22
1010 DATA 90,23,1b,7a,b3,20,f6,c9,c5,d5
1020 DATA 37,3f,16,0a,f3,3e,00,3f,1f,c3
1030 DATA 30,90,d3,10,06,0f,10,fe,37,cb
1040 DATA 19,15,20,ed,fb,d1,c1,c9
1050 DATA next
2000 DATA 3a,00,91,f6,00,20,08,3e,01,32
2010 DATA 00,91,cd,18,00,21,00,94,22,30
2020 DATA 60,21,00,04,22,32,60,3e,06,cd
2030 DATA 18,00,c9
2040 DATA stop