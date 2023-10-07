/*** M2000: Portable P2000 emulator *****************************************/
/***                                                                      ***/
/***                              splitape.c                              ***/
/***                                                                      ***/
/*** This program splits a tape image to several tape images all          ***/
/*** containing only one file                                             ***/
/***                                                                      ***/
/*** Copyright (C) Marcel de Kogel 1996,1997                              ***/
/***     You are not allowed to distribute this software commercially     ***/
/***     Please, notify me, if you make any changes to this file          ***/
/****************************************************************************/

#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>

bool charAllowed (char c)
{
  return isprint(c) && c!='<' && c!='>' && c!=':' && c!='"' && c!='/' && c!='\\' && c!='|' && c!='?' && c!='*';
}

int main (int argc, char *argv[])
{
 static unsigned char buffer[1024+256];
 FILE *infile;
 FILE *outfile;
 char p2000name[16];
 char filename[16+4+1];
 int filecount=0;
 int i,j,pos;
 printf ("splitape v2.0: Tape image splitter\n"
         "Copyright (C) Marcel de Kogel 1996\n");
 if (argc!=2)
 {
  printf ("Usage: splitape <tape image>\n");
  return 1;
 }
 if (!(infile=fopen (argv[1],"rb")))
 {
  printf ("ERROR: Can't open %s\n",argv[1]);
  return 1;
 }
 while (fread(buffer,1024+256,1,infile))
 {
  for (i=0;i<256;++i) //clear irrelevant b ytes
  {
    if (i<0x30 || i>=0x50) buffer[i] = 0;
  }
  for (i=0;i<8;++i)
  {
    //get all 16 characters of original filename
    p2000name[i] = buffer[0x36+i];
    p2000name[i+8] = buffer[0x47+i];
  }
  pos = 0;
  for (i=0;i<16;++i)
  {
    j=p2000name[i];
    if (charAllowed(j)
      && (j!=' ' || (pos>0 && i!=15 && charAllowed(p2000name[i+1]) && p2000name[i+1]!=' '))) //remove extra spaces
    {
      filename[pos++] = j;
    }
  }
  filename[pos++]='.';
  filename[pos++]='c';
  filename[pos++]='a';
  filename[pos++]='s';
  filename[pos++]='\0';
  i=buffer[0x4F];
  if (!i) i=256;
  if ((outfile=fopen(filename,"rb")))
  {
    fclose(outfile);
    printf ("ERROR: Output file %s already exists. \n",filename);
    return 1;
  }
  if ((outfile=fopen (filename,"wb")))
  {
   printf ("Writing %s - %d blocks\n",filename,i);
  }
  else
  {
   printf ("ERROR: Can't open %s\n",filename);
   return 1;
  }
  fwrite (buffer,1024+256,1,outfile);
  for (--i;i;--i)
  {
   fread (buffer,1024+256,1,infile);
   fwrite (buffer,1024+256,1,outfile);
  }
  fclose (outfile);
  filecount++;
 }
 fclose (infile);
 return 0;
}

