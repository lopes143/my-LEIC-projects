/* iaed25 - ist1113963 - project */

/**
 * A program that manages batches of vaccines and its applications, written in C
 * Each batch contains multiple vaccines that can be applied to multiple users
 * The program tracks the applications and their time of application
 * @file: project.c
 * @author: ist1113963 (Rodrigo Lopes)
 */

#include "project.h"

/** Allocates memory to inoculations list
 * @param data state information
 * @param n 1 to add 1 place, -1 to remove last place
 * @param pt flag to display errors in portuguese
*/
void alloc_inoc_memory(sys *data, int n, int pt) {
    if (n == 0) return;
    inoc *temp=NULL;
    int newCount=(data->inoc_count)+n;

    /* If we're removing the only element in the inoculation list
    we just do free() */
    if (newCount==0) {
        free(data->allInoc);
        data->allInoc=NULL;
        data->inoc_count=newCount;
        return; }

    //We can't subtract more elements that the existent ones
    else if (newCount<0) return;

    temp = realloc(data->allInoc, newCount * sizeof(inoc));

    if (temp == NULL) {
        if (pt) puts(ERRNOMEM_PT);
        else puts(ERRNOMEM);
        return; }
    
    data->allInoc=temp;
    data->inoc_count=newCount;
}


/** Recieves two batches and swap their pointers
 * @param batch1 pointer of first batch
 * @param batch2 pointer of second batch
 */
void swap_batches(batch *batch1,batch *batch2){
    batch temp = *batch1;
    *batch1 = *batch2;
    *batch2 = temp;
}


/** Recieves two inoculations and swap their positions
 * @param inoc1 pointer of first inoculation
 * @param inoc2 pointer of second inoculation
 */
void swap_inocs(inoc *inoc1, inoc *inoc2) {
    inoc temp = *inoc1;
    *inoc1 = *inoc2;
    *inoc2 = temp;
}


/** Recieves two dates and return a number saying what's the oldest
 * @param d1 day of the first date
 * @param m1 month of the first date
 * @param y1 year of the first date
 * @param d1 day of the second date
 * @param m2 month of the second date
 * @param y2 year of the second date
 * @return 1 if the first date is older, 2 if it's second's and 0 if they're equal
 */
int check_older_date(int d1,int m1,int y1,int d2,int m2,int y2) {
    //return 1: fist date is older
    //return 2: second date is older

    if (y1<y2) return 1;
    else if (y1>y2) return 2;
    else {
        if (m1<m2) return 1;
        else if (m1>m2) return 2;
        else {
            if (d1<d2) return 1;
            else if (d1>d2) return 2;
            else return 0; //both dates are the same
            //here we need to return 0 to trigger hex checking
        }
    }
}


/** Recieves two hex, corresponding to batch IDs,
 * and returns a number saying what shoud come first, when ordering
 * @param hex1 first batch ID
 * @param hex2 second batch ID
 * @return 1 if first batch ID should come first, 2 if it's second's
 */
int check_hex(char *hex1, char *hex2) {
    //the function returns the first one

    int len1=strlen(hex1);
    int len2=strlen(hex2);

    //check for length of hex
    //shorter - comes first

    if (len1>len2) return 2;
    else if (len1<len2) return 1;
    else {
        //both hexs have the same length
        for (int i=0; i<len1; i++) {
            if (hex1[i]>hex2[i]) return 2;
            else if (hex1[i]<hex2[i]) return 1;
            else continue; }
        /* After the for loop, if nothing were returned,
        both hexs are the same.
        We return 1 to avoid unnecessary swapping*/
        return 1;
    }
}


/** Sorts the batch list by date of expire, then by hex
 * Uses an optimized version of Bubble Sort
 * @param data state information
 */
void sort_batches(sys *data){
    int i, j, n=data->batch_count;
    int swapped;

    for (i=0; i<n-1; i++) {
        swapped=0;
        for (j=0; j<n-i-1; j++) {
            int d1=data->allBat[j].day;
            int m1=data->allBat[j].mon;
            int y1=data->allBat[j].yr;
            int d2=data->allBat[j+1].day;
            int m2=data->allBat[j+1].mon;
            int y2=data->allBat[j+1].yr;

            switch (check_older_date(d1,m1,y1,d2,m2,y2)) {
                case 2:
                    swap_batches(&data->allBat[j], &data->allBat[j+1]);
                    swapped = 1;
                    break;
                case 0:
                    //both dates are same, we need to check hex values
                    switch (check_hex(data->allBat[j].hex,data->allBat[j+1].hex)) {
                        case 2:
                            swap_batches(&data->allBat[j], &data->allBat[j+1]);
                            swapped = 1;
                            break; } } }

        /* If no elements were swapped, it means batch list is already sorted.
        So we break */
        if (swapped == 0)
            break;
    }
}


/** Compute how many days the given month have, according to its year (needed for february)
 * @param mon month number
 * @param yr year number
 * @return number of days the given month have
 */
int get_month_days(int mon, int yr) {
    int leap_year=0;
    if ((yr%4==0 && yr%100!=0) || (yr%400 == 0))
        leap_year=1;

    switch (mon) {
        case 1:
        case 3:
        case 5:
        case 7:
        case 8:
        case 10:
        case 12:
            return 31;
        case 4:
        case 6:
        case 9:
        case 11:
            return 30;
        case 2:
            switch (leap_year) {
                case 0: return 28;
                case 1: return 29; } }
    return 0;
}


/** Check is given date is valid
 * @param day day number
 * @param mon month number
 * @param yr year number
 * @return 1 for valid, 0 for invalid
 */
int check_valid_date(int day, int mon, int yr) {
    int month_days=get_month_days(mon,yr);
    if (day<=0 || mon<=0 || mon>12 || yr<0) return 0;
    if (day>month_days) return 0;
    return 1;
}


/** Deletes a specific inoculation, indentified by its index
 * @param data state information
 * @param index inoculation index to delete
 */
void delete_inoc(sys *data, int index, int pt) {
    // int nameLen = strlen(data->allInoc[index].name);

    free(data->allInoc[index].name);
    data->allInoc[index].name=NULL;

    //We can't swap if we're deleting the last element
    if (index != data->inoc_count-1)
        swap_inocs(&data->allInoc[index], &data->allInoc[data->inoc_count-1]);

    //we just need to do realloc, no need to reset all values to zero
    alloc_inoc_memory(data,-1,pt);


    // for (int i=0; i<nameLen; i++)
    //     data->allInoc[index].name[i]='\0'; //delete person name
    // for (int i=0; i<MAXHEX; i++)
    //     data->allInoc[index].hex[i]='\0'; //delete batch ID
    // for (int i=0; i<BATMAXNAME; i++)
    //     data->allInoc[index].vaccName[i]='\0'; //delete batch name
    // data->allInoc[index].day=0; //delete date of application
    // data->allInoc[index].mon=0;
    // data->allInoc[index].yr=0;
    // swap_inocs(&data->allInoc[index], &data->allInoc[(data->inoc_count)-1]);
    // free(&data->allInoc[index]);
}


/** Auxiliary function to print batch to stdout
 * @param data state information
 * @param i batch index to print
 */
void print_batch(sys *data, int i) {
    printf("%s ",data->allBat[i].name);
    printf("%s ",data->allBat[i].hex);
    printf("%.2d-",data->allBat[i].day);
    printf("%.2d-",data->allBat[i].mon);
    printf("%.4d ",data->allBat[i].yr);
    printf("%d ",data->allBat[i].availableVaccines);
    printf("%d\n",data->allBat[i].inocCount);
}


/** Auxiliary function to print inoculation to stdout
 * @param data state information
 * @param i inoculation index to print
 */
void print_inoc(sys *data, int i) {
    printf("%s ",data->allInoc[i].name);
    printf("%s ",data->allInoc[i].hex);
    printf("%.2d-",data->allInoc[i].day);
    printf("%.2d-",data->allInoc[i].mon);
    printf("%.4d\n",data->allInoc[i].yr);
}

/** Add a new batch to the batches list (command 'c')
 * @param data state information
 * @param in input line
 * @param pt flag to display errors in portuguese
 */
void create_batch(sys *data, char *in, int pt) {
    //variables are allocated dynamically
    char *batchName=NULL, *batchID=NULL;
    int day,mon,yr,count;

    if(sscanf(in,"c %ms %d-%d-%d %d %ms",
        &batchID,&day,&mon,&yr,&count,&batchName)<6) {
            //if (pt) puts(UNKNOWNCMD_PT);
            //else puts(UNKNOWNCMD);
            free(batchID),free(batchName);
            return; }
            
    int batchIDlen=strlen(batchID);
    int batchNameLen=strlen(batchName);

    //check if batch count will be exceded
    if (data->batch_count >= BATMAXCOUNT) {
        if (pt) puts(TOOMANYVACC_PT);
        else puts(TOOMANYVACC);
        free(batchID),free(batchName);
        return; }

    //check if batch ID already exists
    for (int i=0; i<(data->batch_count); i++)
        if (strcmp(batchID, data->allBat[i].hex)==0) {
            if (pt) puts(DUPNAME_PT);
            else puts(DUPNAME);
            free(batchID),free(batchName);
            return; }
    
    //check if batch ID is valid
    for (int i=0; i<batchIDlen; i++)
        if (!(('0'<=batchID[i]&&batchID[i]<='9') || 
            ('A'<=batchID[i]&&batchID[i]<='F'))) {
            if (pt) puts(INVBAT_PT);
            else puts(INVBAT);
            free(batchID),free(batchName);
            return; }

    //check if batch ID doesn't exceed max length
    if (batchIDlen>MAXHEX) {
        if (pt) puts(INVBAT_PT);
        else puts(INVBAT);
        free(batchID),free(batchName);
        return; }
    
    //check if batch name is valid
    for (int i=0; i<batchNameLen; i++)
        switch (batchName[i]) {
            case ' ':
            case '\n':
            case '\t':
                if (pt) puts(INVNAME_PT); 
                else puts(INVNAME); 
                free(batchID),free(batchName);
                break; }
    
    //check if batch name doesn't exceed max length
    if (batchNameLen>BATMAXNAME) {
        if (pt) puts(INVNAME_PT);
        else puts(INVNAME);
        free(batchID),free(batchName);
        return; }

    //check if date is valid
    if (!check_valid_date(day,mon,yr) || 
        check_older_date(day,mon,yr,data->todayDay,data->todayMon,data->todayYr)==1)  {
            if (pt) puts(INVDATE);
            else puts(INVDATE);
            free(batchID),free(batchName);
            return; }

    //check if quantity is valid
    if (count<0) {
        if (pt) puts(INVQUANT_PT);
        else puts(INVQUANT);
        free(batchID),free(batchName);
        return; }
    
    strcpy(data->allBat[data->batch_count].name,batchName);
    strcpy(data->allBat[data->batch_count].hex,batchID);

    data->allBat[data->batch_count].day=(unsigned short)day;
    data->allBat[data->batch_count].mon=(unsigned short)mon;
    data->allBat[data->batch_count].yr=(unsigned short)yr;
    data->allBat[data->batch_count].availableVaccines=(unsigned short)count;
    data->allBat[data->batch_count].inocCount=0;
    data->batch_count++;

    printf("%s\n",batchID);
    sort_batches(data);
    free(batchID),free(batchName);
    
}


/** List all batches, according to optional filtering arguments (command 'l')
 * @param data state information
 * @param in input line
 * @param pt flag to display errors in portuguese
 */
void list_batches(sys *data, char *in, int pt) {
    char *argument=strtok(in, " ");
    char **allArguments=NULL;
    int argCount=0;
    int currentArgLen=0;
    int printed=0; //temp value to store wether we've printed something or not

    if (strcmp(&in[0], "l")==0) {
        //get following filters
        while ((argument=strtok(NULL, " ")) != NULL) {
            currentArgLen=strlen(argument);
            argument[strcspn(argument, "\n")] = '\0'; //remove /n from last filter

            //expand arguments list for another argument
            allArguments=realloc(allArguments, sizeof(allArguments)+sizeof(char *));

            //allocate memory to accomodate argument value
            allArguments[argCount] = malloc(currentArgLen+1);

            //last value should be EOF
            allArguments[argCount][currentArgLen]='\0'; 
            
            //copy argument value to arguments array
            strcpy(allArguments[argCount],argument);
            argCount++;
        }
    }

    if (argCount==0) {
        //list all batches
        for(int i=0; i<(data->batch_count);i++)
            print_batch(data,i);
    }

    else {
        for (int i=0; i<argCount; i++) {
            for(int j=0; j<(data->batch_count);j++)
                if (strcmp(data->allBat[j].name,allArguments[i])==0) {
                    print_batch(data, j);
                    printed++;
                }
            if (printed==0) {
                /*if nothing was printed, error "no such vaccine" should be printed*/
                if (pt) printf("%s: %s\n",allArguments[i],NOVACC_PT);
                else printf("%s: %s\n",allArguments[i],NOVACC);
            }
            printed=0; //reset printing counter to 0
        }
    }

    //free variables
    for (int i=0; i<argCount;i++)
        free(allArguments[i]);
    free(allArguments);
}


/** Applies an innoculation with vaccines from batch list (command 'a')
 * @param data state information
 * @param in input line
 * @param pt flag to display errors in portuguese
 */
void apply_inoc(sys *data, char *in, int pt) {
    int intLen=strlen(in);
    char chosenHex[MAXHEX]={0};
    char PersonName[MAXINPUTLEN]={0}, VaccName[BATMAXNAME]={0};
    int d1,m1,y1,d2,m2,y2;
    int PersonNameIndex=0, VaccNameIndex=0;
    int chosenBatchIndex=-1, inBrackets=0, copyTo=0;

    //ignore 'a' and space after and '\n' in the end
    for (int i=2; i<(intLen-1); i++) {

        if (in[i]==' ') {
            //if found a space and we're not inside brackets, switch where to store
            if(!inBrackets) copyTo=!copyTo;
            else PersonName[PersonNameIndex++]=in[i]; //the only name that accept spaces is person name
            continue;
        }
        //if found a '/', disable swapping on whitespace
        if (in[i]=='\"') {
            inBrackets=!inBrackets;
            continue;}

        if (!copyTo)
            PersonName[PersonNameIndex++]=in[i];
        else if (copyTo)
            VaccName[VaccNameIndex++]=in[i];
    }

    for (int i=0; i<(data->inoc_count); i++) {
        //check if person is already vaccinated with same vaccine today
        d1=data->allInoc[i].day;
        m1=data->allInoc[i].mon;
        y1=data->allInoc[i].yr;
        d2=data->todayDay;
        m2=data->todayMon;
        y2=data->todayYr;
        if (!strcmp(data->allInoc[i].name,PersonName))
            if (!strcmp(data->allInoc[i].vaccName,VaccName))
                if (check_older_date(d1,m1,y1,d2,m2,y2)==0) {
                    if (pt) puts(ALRVACC_PT);
                    else puts(ALRVACC);
                    return; } }

    /*search for older batch and has vaccines to apply
    The batches are already sorted by date, so we need to find
    the first one that matches name & has available vaccines */
    for (int i=0; i<(data->batch_count); i++) {
        int iCount = data->allBat[i].availableVaccines;
        if (strcmp(data->allBat[i].name,VaccName)==0  && iCount>0) {
            strcpy(chosenHex,data->allBat[i].hex);
            chosenBatchIndex=i;
            break;
        }
    }

    if (strlen(chosenHex)==0 || chosenBatchIndex<0) {
        //didn't found a valid batch to use
        if (pt) puts(NOSTK_PT);
        else puts(NOSTK);
        return; }


    //copy values to inoculation register
    alloc_inoc_memory(data,1,pt);  
    data->allInoc[data->inoc_count-1].day=(unsigned short)(data->todayDay);
    data->allInoc[data->inoc_count-1].mon=(unsigned short)(data->todayMon);
    data->allInoc[data->inoc_count-1].yr=(unsigned short)(data->todayYr);
    strcpy(data->allInoc[data->inoc_count-1].hex,chosenHex);
    data->allInoc[data->inoc_count-1].name=malloc((PersonNameIndex+1)*sizeof(char));
    strcpy(data->allInoc[data->inoc_count-1].name,PersonName);
    strcpy(data->allInoc[data->inoc_count-1].vaccName,VaccName);

    //update values to chosen batch
    data->allBat[chosenBatchIndex].availableVaccines--;
    data->allBat[chosenBatchIndex].inocCount++;

    printf("%s\n",chosenHex);
}

/** Remove a batch from the system (command 'r')
 * @param data state information
 * @param in input line
 * @param pt flag to display errors in portuguese
 */
void remove_batch(sys *data, char *in, int pt) {
    char *batchID=NULL;
    if (sscanf(in,"r %ms",&batchID)<1) {
        //if (pt) puts(UNKNOWNCMD_PT);
        //else puts(UNKNOWNCMD);
        return;
    }

    //search for batch in batch list
    for (int i=0; i<data->batch_count; i++) {
        if (!strcmp(data->allBat[i].hex,batchID)) {
            printf("%d\n",data->allBat[i].inocCount);
            if (data->allBat[i].inocCount>0)
                data->allBat[i].availableVaccines=0;
            else {
                for (int j=0; j<BATMAXNAME; j++)
                    data->allBat[i].name[j]='\0';
                for (int j=0; j<MAXHEX; j++)
                    data->allBat[i].hex[j]='\0';
                data->allBat[i].availableVaccines=0;
                data->allBat[i].inocCount=0;
                data->allBat[i].day=0;
                data->allBat[i].mon=0;
                data->allBat[i].yr=0;
                /*if we delete a batch from the middle of the batch list
                we swap it with the last of the list to fill that hole */
                swap_batches(&data->allBat[i], &data->allBat[(data->batch_count)-1]);
                data->batch_count--;
                sort_batches(data); }
            free(batchID);
            return;
        }
    }

    //if the program ended here, it did not find the batch with given name
    if (pt) printf("%s: %s\n",batchID, NOBAT_PT);
    else printf("%s: %s\n",batchID, NOBAT);
    free(batchID);
    return;
}

/** Remove all vacine applications for given user from the system (command 'd')
 * @param data state information
 * @param in input line
 * @param pt flag to display errors in portuguese
 */
void remove_inoc(sys *data, char *in, int pt) {
    char *personName=NULL,batchID[MAXHEX]={0};
    int d=0,m=0,y=0;
    int deleted=0,hexFound=0;
    int inocD,inocM,inocY;
    
    int argsRead=sscanf(in,"d %ms %d-%d-%d %s",&personName,&d,&m,&y,batchID);
    /* argsRead:
    1 - no arguments (just name)
    4 - just 1 argument: date
    5 - all arguments (date & batch ID)
    */
    if (argsRead<1) {
        //did not match nothing
        free(personName);
        return; }

    //check if date is valid, when it's given
    if (argsRead>1)
        if (check_valid_date(d,m,y)==0) {
            if (pt) puts(INVDATE_PT);
            else puts(INVDATE);
            free(personName);
            return;
        }      

    //check if batch exists
    if (argsRead==5) {
        for (int i=0; i<data->batch_count; i++) {
            if (strcmp(data->allBat[i].hex,batchID)==0){
                hexFound=1;
                break; } }
        if (hexFound==0) {
            if (pt) printf("%s: %s\n",batchID,NOBAT_PT);
            else printf("%s: %s\n",batchID,NOBAT);
            free(personName);
            return; } }

    for (int i=0; i<data->inoc_count; i++) {
        inocD=data->allInoc[i].day;
        inocM=data->allInoc[i].mon;
        inocY=data->allInoc[i].yr;
        if (argsRead==1 && strcmp(data->allInoc[i].name,personName)==0) {
            //just delete based on name
            delete_inoc(data,i,pt);
            deleted++; }
        else if (argsRead==4 && strcmp(data->allInoc[i].name,personName)==0 &&
            check_older_date(d,m,y,inocD,inocM,inocY)==0) {
                //delete based on name & date
                delete_inoc(data,i,pt);
                deleted++; }
        else if (argsRead==5 && strcmp(data->allInoc[i].name,personName)==0 &&
            check_older_date(d,m,y,inocD,inocM,inocY)==0 &&
            strcmp(data->allInoc[i].hex,batchID)==0) {
                //delete based on name, date & ID
                delete_inoc(data,i,pt);
                deleted++; } }
    
    //if nothing were deleted, error should be displayed
    if (deleted==0) {
        if (pt) printf("%s: %s\n",personName,NOUSR_PT);
        else printf("%s: %s\n",personName,NOUSR);
        free(personName);
        return; }

    printf("%d\n",deleted);
    free(personName);

}

/** List all innoculations, according to optional filtering arguments (command 'u')
 * @param data state information
 * @param in input line
 * @param pt flag to display errors in portuguese
 */
void list_inocs(sys *data, char *in, int pt) {
    //parse input
    char name[MAXINPUTLEN]={0};
    int inputLen=strlen(in), nameIndex=0, printed=0;

    if (inputLen<=2) { // input is just "u ": list all
        for (int i=0; i<(data->inoc_count); i++) {
            print_inoc(data, i);
            printed=1;
        }
    }
    else { //input has argument: filter list
        //get argument
        for (int i=2; i<(inputLen-1); i++) {
            //remove "u " from beginning & '\n' at the end
            if (in[i]=='\"') continue; //ignore quotation marks
            name[nameIndex++]=in[i];
        }

        //search for match
        for (int i=0; i<(data->inoc_count); i++) {
            if (!strcmp(data->allInoc[i].name,name)) {
                print_inoc(data,i);
                printed=1;
            }
        }
    }

    //check for errors
    if (printed==0) {
        if (pt) printf("%s: %s\n", name, NOUSR_PT);
        else printf("%s: %s\n", name, NOUSR);
        return;
    }
}

/** Advance system's time by 1 day or to specific date (command 't')
 * @param data state information
 * @param in input line
 * @param pt flag to display errors in portuguese
 */
void advance_time(sys *data, char *in, int pt) {
    int newDay=0,newMon=0,newYr=0;
    int currDay=data->todayDay;
    int currMon=data->todayMon;
    int currYr=data->todayYr;
    int n=sscanf(in,"%*s %d-%d-%d",&newDay,&newMon,&newYr);
    switch (n) {
        case EOF:
        case 0: //no custom date matched: advance 1 day
            newDay=(currDay)+1;
            newMon=currMon;
            newYr=currYr;
            int monDays=get_month_days(newMon,newYr);
            if (newDay>monDays) {
                newMon++;
                newDay-=monDays; }
            if (newMon>12) {
                newYr++;
                newMon-=12; }
            break;
        case 1:
        case 2:
            if (pt) puts(INVDATE_PT);
            else puts(INVDATE);
            return;
            break;
        case 3:
            //input date might be the same as system's, and it's valid
            int check = check_older_date(currDay,currMon,currYr,newDay,newMon,newYr);
            if (!(newYr>0 && newMon>0 && newMon<=12 &&
                newDay<=get_month_days(newMon,newDay) && (check==0 || check==1))) {
                    if (pt) puts(INVDATE_PT);
                    else puts(INVDATE);
                    return; }
    }

    printf("%.2d-%.2d-%.4d\n",newDay,newMon,newYr);
    data->todayDay=newDay;
    data->todayMon=newMon;
    data->todayYr=newYr;

    //now we need to check for all batches if they're good to use
    for (int i=0; i<(data->batch_count); i++) {
        int d=data->allBat[i].day;
        int m=data->allBat[i].mon;
        int y=data->allBat[i].yr;
        if(check_older_date(d,m,y,newDay,newMon,newYr)==1)
            //batch is outdated, but its ID still need to exist
            data->allBat[i].availableVaccines=0;
    }
    return;
}

/** Stop the program safely by freeing all dynamic variables (command 'q')
 * @param data state information
 */
void quit(sys *data) {
    for (int i=0; i<data->inoc_count; i++) {
        free(data->allInoc[i].name);
    }
    free(data->allInoc);
}

/** Vaccines & inoculations manager
 * @param argn number of input arguments
 * @param argv array of input arguments
 * @return always returns 0
 */
int main(int argn, char **argv) {
    //setup language
    int pt=0;
    if (argn==2)
        if (!strcmp(argv[1],"pt"))
            pt=1;
    
    char input[MAXINPUTLEN];
    sys data;
    data.batch_count=0,data.inoc_count=0;
    data.todayDay=1,data.todayMon=1,data.todayYr=2025;
    data.allInoc=NULL;
    while(fgets(input,MAXINPUTLEN,stdin))
    switch (input[0]) {
            case 'q': quit(&data); return 0;
            case 'c': create_batch(&data, input, pt); break;
            case 'l': list_batches(&data, input, pt); break;
            case 'a': apply_inoc(&data, input, pt); break;
            case 'r': remove_batch(&data, input, pt); break;
            case 'd': remove_inoc(&data,input,pt); break;
            case 'u': list_inocs(&data, input, pt); break;
            case 't': advance_time(&data, input, pt); break;
            //default: puts(UNKNOWNCMD); break;
    }
    return 0;
}