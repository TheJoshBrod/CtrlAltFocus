#include "wiiuse-lib/src/wiiuse.h"
#include <iostream>
#include <thread>
#include <chrono>

int main(int argc, char **argv) {
    // Create a singular wiimote_t structure
    wiimote_t ** wiimotes = wiiuse_init(1);

    if (!wiimotes) {
        std::cout << "Failed to initialize wiimotes" << std::endl;
        return 1;
    }

    // idea: poll the wii remote for events every X milliseconds, use
    // information learned to transmit information to the python server
    while(true) { // Wait for bop it started signal
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

        // Check for bop it signal

        // If bop it signal received, listen for what buttons should be pressed, 
        // poll the wiimote, and determine player accuracy
    }

    // wiiuse_update():
    int leds = 0;
    wiiuse_set_leds(wiimotes[0], leds);

    std::this_thread::sleep_for(std::chrono::seconds(7));  // Pauses for 3 seconds

    // Close connection with wii remote and free wiimote_t structure
    wiiuse_disconnect(wiimotes[0]);
    wiiuse_cleanup(wiimotes, 1);
    return 0;
}




