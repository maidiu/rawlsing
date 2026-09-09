#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct { int slot; const char *name; } Sel;
static Sel sel[] = {
 {8,"A_YEAR"},{10,"B_COUNTR"},{14,"D_INTERV"},{15,"S007"},{44,"S025"},
 {346,"Q264"},{348,"Q265"},{352,"Q267"},{354,"Q268"},{358,"Q271"},{360,"Q273"},
 {365,"Q276"},{366,"Q276A"},{368,"Q277"},{369,"Q277A"},{371,"Q278"},{372,"Q278A"},
 {375,"Q280"},{377,"Q282"},{378,"Q283"}
};
#define NSEL (sizeof(sel)/sizeof(sel[0]))

static int find_sel(int slot){ for(int i=0;i<(int)NSEL;i++) if(sel[i].slot==slot) return i; return -1; }
static double rd_double_le(const unsigned char b[8]) { double x; memcpy(&x,b,8); return x; }

int main(int argc,char **argv){
 if(argc<3){fprintf(stderr,"usage: %s input.sav output.csv\n",argv[0]); return 2;}
 FILE *f=fopen(argv[1],"rb"); if(!f){perror("open");return 2;}
 FILE *o=fopen(argv[2],"w"); if(!o){perror("out");return 2;}
 const long data_off=719566; const int case_size=645; const int ncases=97220; const double bias=100.0;
 if(fseek(f,data_off,SEEK_SET)!=0){perror("seek");return 2;}
 fprintf(o,"source_row_ordinal"); for(int i=0;i<(int)NSEL;i++) fprintf(o,",%s",sel[i].name); fputc('\n',o);
 int row=1, slot=0; double vals[NSEL]; unsigned char present[NSEL]; memset(present,0,sizeof(present));
 while(row<=ncases){
   unsigned char codes[8]; if(fread(codes,1,8,f)!=8){fprintf(stderr,"EOF codes row=%d slot=%d\n",row,slot);return 3;}
   for(int ci=0;ci<8;ci++){
     unsigned c=codes[ci];
     if(c==0) continue;
     if(c==252){ fprintf(stderr,"end marker row=%d slot=%d\n",row,slot); goto done; }
     unsigned char raw[8]; double v=NAN; int hasnum=1;
     if(c==253){ if(fread(raw,1,8,f)!=8){fprintf(stderr,"EOF raw\n");return 4;} v=rd_double_le(raw); }
     else if(c==254){ hasnum=0; }
     else if(c==255){ v=NAN; }
     else { v=((double)c)-bias; }
     int si=find_sel(slot);
     if(si>=0){ vals[si]=v; present[si]=(unsigned char)hasnum; }
     slot++;
     if(slot==case_size){
       fprintf(o,"%d",row);
       for(int j=0;j<(int)NSEL;j++){
         if(!present[j] || isnan(vals[j]) || vals[j] < -1e307) fprintf(o,",");
         else fprintf(o,",%.17g",vals[j]);
       }
       fputc('\n',o);
       row++; slot=0; memset(present,0,sizeof(present));
       if(row>ncases) goto done;
     }
   }
 }
done:
 fclose(f); fclose(o);
 fprintf(stderr,"rows_written=%d final_slot=%d\n",row-1,slot);
 return (row-1==ncases)?0:5;
}
