/*** M2000: Portable P2000 emulator *****************************************/
/***                                                                      ***/
/***                          cas32tocas.c                                ***/
/***                                                                      ***/
/***                                                                      ***/
/*** Copyright (C) Dion Olsthoorn 2024                                    ***/
/****************************************************************************/

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main (int argc, char *argv[])
{
 static unsigned char bufferin[1024+32];
 static unsigned char bufferout[1024+256] = {0};
 FILE *infile, *outfile;

 if (argc!=3)
 {
  printf ("cas32tocas v1.0: Converts .cas32 (32-bytes header) to .cas (256-byte header).\n");
  printf ("Usage: cleancas <in .cas32> <out .cas>\n");
  return 1;
 }
 infile=fopen (argv[1],"rb");
 outfile=fopen (argv[2],"wb");
 if (!infile || !outfile)
 {
  printf ("Can't open %s or %s\n",argv[1], argv[2]);
  return 1;
 }
 while (fread(bufferin,1024+32,1,infile))
 {
  memcpy(bufferout+0x30, bufferin, 32);
  memcpy(bufferout+0x100, bufferin+0x20, 1024);
  fwrite (bufferout, 1024+256, 1, outfile);
 }
 fclose (infile);
 fclose (outfile);
 return 0;
}

