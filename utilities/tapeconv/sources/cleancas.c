/*** M2000: Portable P2000 emulator *****************************************/
/***                                                                      ***/
/***                          cleancas.c                                  ***/
/***                                                                      ***/
/*** This utility cleans a P2000T .cas cassette dump file by clearing     ***/
/*** irrelevant bytes that weren't part of a cassette data record (header ***/
/*** or data).                                                            ***/
/*** Cleaned .cas files allow for better compression and de-duplication.  ***/
/***                                                                      ***/
/*** Copyright (C) Dion Olsthoorn 2023                                    ***/
/****************************************************************************/

#include <stdio.h>
#include <stdbool.h>

int main (int argc, char *argv[])
{
 static unsigned char buffer[1024+256];
 FILE *infile;
 int blockcount=0;
 int i,j;
 bool dirty;

 printf ("cleancas v1.0: Clears irrelevant bytes in a P2000T .cas file\n"
         "Copyright (C) Dion Olsthoorn 2023\n");
 if (argc!=2)
 {
  printf ("Usage: cleancas <cassette dump file>\n");
  return 1;
 }
 infile=fopen (argv[1],"rb+");
 if (!infile)
 {
  printf ("Can't open %s\n",argv[1]);
  return 1;
 }
 while (fread(buffer,1024+256,1,infile))
 {
  blockcount++;
  dirty = false;
  for (i=0;i<256;++i)
  {
    //clear irrelevant bytes
    if ((i<0x30 || i>=0x50) && buffer[i] != 0) 
    {
      buffer[i] = 0;
      dirty = true;
    }
  }
  if (dirty)
  {
    j = ftell(infile);
    fseek(infile, j-1024-256, SEEK_SET);
    fwrite (buffer,256,1,infile);
    fseek(infile, j, SEEK_SET);
  }
 }
 fclose (infile);
 printf ("Cleaned %d blocks\n",blockcount);
 return 0;
}
