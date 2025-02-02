#include "wiiuse-lib/src/wiiuse.h"
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <chrono>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")  // Link Winsock library

#define BUFFER_SIZE 1024

std::string active_action_id;
std::string active_action;
std::mutex mtx;
std::condition_variable cv;

wiimote_t ** wiimotes;

int main(int argc, char **argv) {
    // Create a singular wiimote_t structure
    wiimotes = wiiuse_init(1);

    if (!wiimotes) {
        std::cout << "Failed to initialize wiimotes" << std::endl;
        return 1;
    }

    wiiuse_motion_sensing(wiimotes[0], 1);

    // Start tcp_listener thread
    std::thread tcp_t(tcp_listener_fn);

    // idea: poll the wii remote for events every X milliseconds, use
    // information learned to transmit information to the python server
    while(true) { // TODO: have python server send tcp message when finished
        if(!WIIMOTE_IS_CONNECTED(wiimotes[0])) {
            // FIRST: search for nearby wiimotes using wiiuse_find(wiimotes, 1, 5)
            std::cout << "Searching for wiimotes..." << std::endl;
            while(wiiuse_find(wiimotes, 1, 5) <= 0) {
                std::cout << "Pausing for 5 seconds..." << std::endl;
                std::this_thread::sleep_for(std::chrono::seconds(5));  // Pauses for 5 seconds
                std::cout << "No wiimotes found. Retrying..." << std::endl;
            }

            // Connect to wiimote once address is known (filled by wiiuse_find())
            if(wiiuse_connect(wiimotes, 1) <= 0) {
                std::cout << "Failed to connect to wiimote" << std::endl;
                return 1;
            }
        }

        // Check for events from wiimote
        wiiuse_update(wiimotes, 1, update_wiimote);

        // If bop it signal received, listen for what buttons should be pressed, 
        // poll the wiimote, and determine player accuracy

        std::this_thread::sleep_for(std::chrono::milliseconds(500));  // Pauses for 0.5 seconds
    }

    // Close connection with wii remote and free wiimote_t structure
    wiiuse_disconnect(wiimotes[0]);
    wiiuse_cleanup(wiimotes, 1);
    return 0;
}


// PURPOSE: Listens for incoming tcp messages coming from python server.
//          Synchronizes main thread using thread::cv and thread::mutex
int tcp_listener_fn(const int server_port) {
    WSADATA wsaData;
    char buf[BUFFER_SIZE];
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed.\n";
        return 1;
    }

    // Create server socket
    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == INVALID_SOCKET) {
        std::cerr << "Socket creation failed.\n";
        WSACleanup();
        return 1;
    }

    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(server_port);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    // Bind socket
    if (bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "Bind failed.\n";
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    // Listen for connections
    if (listen(serverSocket, SOMAXCONN) == SOCKET_ERROR) {
        std::cerr << "Listen failed.\n";
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    std::cout << "Server listening on port " << server_port << "...\n";

    sockaddr_in clientAddr{};
    int clientAddrSize = sizeof(clientAddr);
    SOCKET clientSocket;
    while(clientSocket = accept(serverSocket, (sockaddr*)&clientAddr, &clientAddrSize)) {
        if (clientSocket == INVALID_SOCKET) {
            std::cerr << "Accept failed.\n";
            closesocket(serverSocket);
            WSACleanup();
        }

        int bytes_received;
        while(bytes_received = recv(clientSocket, buf, BUFFER_SIZE, 0)) {
            if(bytes_received > 0) {
                std::string action_id, action;
                std::string data(buf);
                size_t delim_pos = data.find('$');
                action_id = data.substr(0, delim_pos);
                action = data.substr(delim_pos+1); 
                // Set globals for action, signal to thread new action has been sent
                std::lock_guard<std::mutex> lock(mtx);
                active_action_id = action_id;
                active_action = action;
            }
            else if(bytes_received == 0) {
                std::cout << "Connection closing with client\n";
            }
            else {
                std::cerr << "Failed to recv from client\n";
                return -1;
            }
        }
        
    }
}


bool action_fn(wiimote_t ** wm, const std::string & action_id, const std::string & action) {
    
    if(action == "+") {
        return IS_PRESSED(wm[0], CLASSIC_CTRL_BUTTON_PLUS) || IS_HELD(wm[0], CLASSIC_CTRL_BUTTON_PLUS) || IS_JUST_PRESSED(wm[0], CLASSIC_CTRL_BUTTON_PLUS);
    }
    else if(action == "-") {
        return IS_PRESSED(wm[0], CLASSIC_CTRL_BUTTON_MINUS) || IS_HELD(wm[0], CLASSIC_CTRL_BUTTON_MINUS) || IS_JUST_PRESSED(wm[0], CLASSIC_CTRL_BUTTON_MINUS);
    }
    else if(action == "1") {
        return IS_PRESSED(wm[0], WIIMOTE_BUTTON_ONE) || IS_HELD(wm[0], WIIMOTE_BUTTON_ONE) || IS_JUST_PRESSED(wm[0], WIIMOTE_BUTTON_ONE);
    }
    else if(action == "2") {
        return IS_PRESSED(wm[0], WIIMOTE_BUTTON_TWO) || IS_HELD(wm[0], WIIMOTE_BUTTON_TWO) || IS_JUST_PRESSED(wm[0], WIIMOTE_BUTTON_TWO);
    }
    else if(action == "A") {
        return IS_PRESSED(wm[0], WIIMOTE_BUTTON_A) || IS_HELD(wm[0], WIIMOTE_BUTTON_A) || IS_JUST_PRESSED(wm[0], WIIMOTE_BUTTON_A);
    }
    else if(action == "B") {
        return IS_PRESSED(wm[0], WIIMOTE_BUTTON_B) || IS_HELD(wm[0], WIIMOTE_BUTTON_B) || IS_JUST_PRESSED(wm[0], WIIMOTE_BUTTON_B);
    }
    else if(action == "left") {
        return IS_PRESSED(wm[0], WIIMOTE_BUTTON_LEFT) || IS_HELD(wm[0], WIIMOTE_BUTTON_LEFT) || IS_JUST_PRESSED(wm[0], WIIMOTE_BUTTON_LEFT);
    }
    else if(action == "right") {
        return IS_PRESSED(wm[0], WIIMOTE_BUTTON_RIGHT) || IS_HELD(wm[0], WIIMOTE_BUTTON_RIGHT) || IS_JUST_PRESSED(wm[0], WIIMOTE_BUTTON_RIGHT);
    }
    else if(action == "up") {
        return IS_PRESSED(wm[0], WIIMOTE_BUTTON_UP) || IS_HELD(wm[0], WIIMOTE_BUTTON_UP) || IS_JUST_PRESSED(wm[0], WIIMOTE_BUTTON_UP);
    }
    else if(action == "down") {
        return IS_PRESSED(wm[0], WIIMOTE_BUTTON_DOWN) || IS_HELD(wm[0], WIIMOTE_BUTTON_DOWN) || IS_JUST_PRESSED(wm[0], WIIMOTE_BUTTON_DOWN);
    }
    else if(action == "shake-it") {
        double accel = sqrt((wm[0]->accel.x - wm[0]->lstate.accel.x)^2 + (wm[0]->accel.y - wm[0]->lstate.accel.y)^2
            + (wm[0]->accel.z - wm[0]->lstate.accel.z)^2);

        std::cout << accel << std::endl;

        return (accel > wm[0]->accel_threshold);      
    }
}


void update_wiimote(wiimote_callback_data_t * wm) {
    // Set last state values
    wiimotes[0]->lstate.accel = wiimotes[0]->accel;
    wiimotes[0]->lstate.btns = wiimotes[0]->btns;
    wiimotes[0]->lstate.orient = wiimotes[0]->orient;
    // Set new state values
    wiimotes[0]->leds = wm->leds;
    wiimotes[0]->battery_level = wm->battery_level;
    wiimotes[0]->accel = wm->accel;
    wiimotes[0]->orient = wm->orient;
    wiimotes[0]->gforce = wm->gforce;
    wiimotes[0]->btns = wm->buttons;
    wiimotes[0]->btns_held = wm->buttons_held;
    wiimotes[0]->btns_released = wm->buttons_released;
    wiimotes[0]->state = wm->state;
    wiimotes[0]->event = wm->event;

    std::lock_guard<std::mutex> lock(mtx);
    action_fn(wiimotes, active_action_id, active_action);
}




