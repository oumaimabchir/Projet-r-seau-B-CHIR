//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
#include "../header_c/extract_ip.h"

char* extractIpAddress() {
    struct ifaddrs *ifaddr, *ifa;
    int family, s;
    char host[1025];
    char *loopbackIP = NULL;
    const char* interfaces[] = {"eth0", "wlan0", "lo", "wlp4s0"}; // List of common interface names
    size_t num_interfaces = sizeof(interfaces) / sizeof(interfaces[0]);

    if (getifaddrs(&ifaddr) == -1) {
        perror("getifaddrs");
        return NULL;
    }
    // Walk through linked list, maintaining head pointer so we can free list later
    for (size_t i = 0; i < num_interfaces; ++i) {
        for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
            if (ifa->ifa_addr == NULL) {
                continue;
            }
            family = ifa->ifa_addr->sa_family;

            if (family == AF_INET && strcmp(ifa->ifa_name, interfaces[i]) == 0) {
                s = getnameinfo(ifa->ifa_addr, sizeof(struct sockaddr_in), host, 1025, NULL, 0, 1);
                if (s != 0) {
                    printf("getnameinfo() failed: %s\n", gai_strerror(s));
                    continue;
                }
                loopbackIP = strdup(host); // strdup allocates memory and copies the string
                break; // We've found the interface, no need to continue
            }
        }
        if (loopbackIP != NULL) {
            break;
        }
    }
    freeifaddrs(ifaddr);
    if (loopbackIP == NULL) {
        loopbackIP = strdup("127.0.0.1"); // Fallback to localhost
    }
    return loopbackIP;
}
