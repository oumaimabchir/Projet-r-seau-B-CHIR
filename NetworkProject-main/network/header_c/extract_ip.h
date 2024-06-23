#ifndef EXTRACT_IP_H
#define EXTRACT_IP_H

#include <ifaddrs.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>

char* extractIpAddress();

#endif // EXTRACT_IP_H
