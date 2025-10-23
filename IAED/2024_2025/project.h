#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define BATMAXNAME 50    //max batch name length
#define INOCMAXNAME 200   //max inoculation name length
#define MAXHEX 20         //max hex ID length
#define BATMAXCOUNT 1000  //how many batches are accepted on the system
#define MAXINPUTLEN 65535 //max input length
#define UNKNOWNCMD "unknown command"
#define UNKNOWNCMD_PT "comando inválido"
#define ERRNOMEM "No memory."
#define ERRNOMEM_PT "Sem memória."

//errors for 'c'
#define TOOMANYVACC "too many vaccines"
#define TOOMANYVACC_PT "demasiadas vacinas"
#define DUPNAME "duplicate batch number"
#define DUPNAME_PT "número de lote duplicado"
#define INVBAT "invalid batch"
#define INVBAT_PT "lote inválido"
#define INVNAME "invalid name"
#define INVNAME_PT "nome inválido"
#define INVDATE "invalid date"
#define INVDATE_PT "data inválida"
#define INVQUANT "invalid quantity"
#define INVQUANT_PT "quantidade inválida"
#define NOVACC "no such vaccine"
#define NOVACC_PT "vacina inexistente"
#define NOUSR "no such user"
#define NOUSR_PT "utente inexistente"
#define NOSTK "no stock"
#define NOSTK_PT "esgotado"
#define NOBAT "no such batch"
#define NOBAT_PT "lote inexistente"
#define ALRVACC "already vaccinated"
#define ALRVACC_PT "já vacinado"

typedef struct{
    char name[BATMAXNAME];
    char hex[MAXHEX];
    unsigned short day;
    unsigned short mon;
    unsigned short yr;
    unsigned short availableVaccines;
    unsigned short inocCount;
    
} batch;

typedef struct{
    char *name;
    char hex[MAXHEX];
    char vaccName[BATMAXNAME];
    unsigned short day;
    unsigned short mon;
    unsigned short yr;
} inoc;

typedef struct{
    batch allBat[BATMAXCOUNT];
    inoc allInoc[20000]; //FIX THIS!!!!
    unsigned short todayDay;
    unsigned short todayMon;
    unsigned short todayYr;
    unsigned short batch_count;
    unsigned short inoc_count;
} sys;