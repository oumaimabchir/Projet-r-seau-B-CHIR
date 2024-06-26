#include "../header_c/py_net.h"
#include "../header_c/type_msg.h"

static const uint32_t header_size =  sizeof(uint8_t ) + 2 * sizeof(uint32_t);
static char *python_buffer;
static unsigned int python_buffer_size = 0;

//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------

int connect_to_py(int s_port){
    struct sockaddr_in sockaddre = {0};
    sockaddre.sin_family = AF_INET;
    sockaddre.sin_port = htons(s_port);
    sockaddre.sin_addr.s_addr = inet_addr("127.0.0.1");
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1){
        perror("erroor => socket");
        return -1;
    }
    if (connect(sock, (struct sockaddr *)&sockaddre, sizeof(sockaddre)) == -1){
        perror("erroor => connect");
        close(sock);
        return -1;
    }
    python_packet *packet = create_python_packet();
    do{
        fd_set fd_read;
        FD_ZERO(&fd_read);
        FD_SET(sock, &fd_read);
        select(sock + 1, &fd_read, NULL, NULL, NULL);
        if (FD_ISSET(sock, &fd_read))
        {
            
            if (receive_python_packet(packet, sock) == 0)
            {
                printf("errooor Server ==> disconnected\n");
                close(sock);
                return 1;
            }
        }
    }while( packet -> type != PYMSG_CONNECT_OK);
    printf(" C | ==> Connecte succes into py\n");
    return sock;
}

//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------

static void resize_python_buffer( int size){
    if ( python_buffer_size ){
        free(python_buffer);
    }
    python_buffer = calloc(size, 1);
    python_buffer_size = size;
}

//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------

int init_python_packet( python_packet* packet, uint8_t type, uint32_t port, uint32_t size ){
    packet -> type = type;
    packet ->  port = port;
    packet ->  size = size;
    if (size){
        packet -> data = calloc(size, 1);
    }
    
}

//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------

python_packet *create_python_packet(){
    python_packet *new_packet = calloc(sizeof(python_packet), 1);
    if (new_packet == NULL){
        return NULL;
    }
    new_packet->data = NULL;
    return new_packet;
}

//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------

int receive_python_packet( python_packet *packet, int socket){
    char* buf = calloc(header_size, 1);
    int recv_size = recv(socket, buf, header_size, 0);
    memcpy(&(packet -> type), buf, sizeof(uint8_t));
    memcpy(&(packet -> port), buf + sizeof(uint8_t), sizeof(uint32_t));
    memcpy(&(packet -> size), buf + sizeof(uint8_t) + sizeof(uint32_t), sizeof(uint32_t));
    if (recv_size == -1){
        perror("eroor recv ");
        return -1;
    }
    if ( packet -> size ){
        packet -> data = calloc(packet -> size, 1);
        recv_size += recv(socket, packet -> data, packet -> size, 0);
    }
    // print_python_packet(packet);
    return recv_size;

}

//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------

int send_python_packet( python_packet* packet, int socket){
    uint32_t send_size = header_size;
    if ( packet ->  size > 0 && packet -> data != NULL){
        send_size += packet ->  size;
    }
    if ( send_size > python_buffer_size){
        resize_python_buffer(send_size);
    }
    memset(python_buffer, '\0', send_size);
    if ( memcpy(python_buffer, &(packet -> type), sizeof(u_int8_t)) == NULL){
        return -1;
    }
    if ( memcpy(python_buffer + sizeof(u_int8_t), &(packet -> port), sizeof(u_int32_t)) == NULL){
        return -1;
    }
    if ( memcpy(python_buffer + sizeof(u_int8_t) + sizeof(u_int32_t), &(packet -> size), sizeof(u_int32_t)) == NULL){
        return -1;
    }
    if ( packet ->  size > 0 && packet -> data != NULL){
        if (memcpy(python_buffer + header_size, packet -> data, packet ->  size) == NULL){
            return -1;
        }
    }
    int a = (int) send(socket, python_buffer, send_size, 0);
    // printf("[C] Sent %d bytes\n", a);
    return a;

}
//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------

void flush_python_socket( int socket){
    int received_size;
    char buffer[1024];
    do{
        received_size = recv(socket, buffer, 1024, MSG_DONTWAIT);
        if (received_size == -1 && errno == EAGAIN){
            return;
        }
    } while (received_size >= 1024);
}
//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------

void print_python_packet( python_packet* packet){
    printf(" C   ==> We Received Python Packet ");
    printf("Type ==> %d ", packet -> type);
    printf("Port ==> %d ", packet -> port);
    printf("Size ==> %d ", packet -> size);
    printf("Data ==> %s \n", packet -> data);

}
//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------