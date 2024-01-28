/*** M2000: Portable P2000 emulator *****************************************/
/***                                                                      ***/
/***                          castocas32.c                                ***/
/***                                                                      ***/
/***                                                                      ***/
/*** Copyright (C) Dion Olsthoorn 2024                                    ***/
/****************************************************************************/

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main (int argc, char *argv[])
{
 static unsigned char bufferin[1024+256];
 static unsigned char bufferout[1024+32] = {0};
 FILE *infile, *outfile;

 if (argc!=3)
 {
  printf ("castocas32 v1.0: Converts .cas (256-bytes header) to .cas32 (32-byte header).\n");
  printf ("Usage: cleancas <in .cas> <out .cas32>\n");
  return 1;
 }
 infile=fopen (argv[1],"rb");
 outfile=fopen (argv[2],"wb");
 if (!infile || !outfile)
 {
  printf ("Can't open %s or %s\n",argv[1], argv[2]);
  return 1;
 }
 while (fread(bufferin,1024+256,1,infile))
 {
  memcpy(bufferout, bufferin+0x30, 32);
  memcpy(bufferout+0x20, bufferin+0x100, 1024);
  fwrite (bufferout, 1024+32, 1, outfile);
 }
 fclose (infile);
 fclose (outfile);
 return 0;
}

