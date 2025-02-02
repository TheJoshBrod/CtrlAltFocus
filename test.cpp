#include "wiiuse-lib/src/wiiuse.h"
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <chrono>
#include <winsock2.h>
#include <ws2tcpip.h>


int main(int argc, char * argv[]) {
    wiimotes **wm = wiiuse_init(1);

    wiiuse_motion_sensing(wiimotes[0], 1);

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

    }
}