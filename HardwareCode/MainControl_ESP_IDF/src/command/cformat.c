#include "cformat.h"

void cformat_return_value(char *prefix, int value, char *output, int size){
    // pass in prefix and data
    // return format: "prefix" + "=" + "data"
    strncpy(output, prefix, size);
    strcat(output, "=");

    char buff[50];
    sprintf(buff, "%d", value);
    strcat(output, buff);
}

