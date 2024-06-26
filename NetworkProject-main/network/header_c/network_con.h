#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/select.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <ifaddrs.h>
#include <netinet/in.h>
#include <netdb.h>

#ifndef NETWORK_CON_H
#define NETWORK_CON_H

#include "packet_handler.h"
#include "cl_manager.h"
#include "py_net.h"

#define CHAR_SIZE 1024

typedef uint32_t game_ip;

static uint16_t main_port = -1;
static int listen_socket = -1;
static int python_socket = -1;
static uint8_t main_color = 0;
static int s_port = -1;

extern char* extractIpAddress();
extern int connect_to_server(const char* ip_server, int port_server, int new_player);
extern int init_connection();
extern int create_listen_socket();
extern int game_listen();
extern int listen_all_client(fd_set *fd_listen);
extern client* accept_new_client(int listen_socket);
extern int message_type_handler(game_packet* packet, client* current_client);
extern int req_connection(client* current_client, game_packet* packet);
extern int new_connection(client* current_client, game_packet* packet);
extern int send_all_ip_port(client* current_client);
extern int affiche_all_ip_port(game_packet* packet);
extern int pymsg_type_handler(python_packet* packet);
extern int listen_from_python();
extern int join_room(python_packet* packet);
extern uint8_t color_generator();
extern game_packet* encapsulate_python_packet(python_packet* packet);
extern int send_to_all_client(python_packet* packet);
int send_to_python(game_packet* packet);

#endif 
