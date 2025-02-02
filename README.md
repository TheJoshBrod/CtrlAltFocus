![CtrlAltFocus](resources/photos/logo.png)

## What is CtrlAltFocus?

CtrlAltFocus is the browser that torments you when you're not focusing. Various challenges/events occur and you have to focus to stop the chaos.

This repo serves as our group entry to SpartaHack W25 Mad Scientist Track.

## Requirements

1. Python >=3.9.13

2. Runs Windows 10-11

3. Windows Powershell

4. Wii Remote\*\*

5. Connects to Bluetooth\*\*

\*\*Optional

## How to install

### Python (Browser Engine)

1.) Download Python >=3.9.13
2.) run `pip install -r requirements.txt`

### Llama

1.) Download [Ollama](https://ollama.com/download/windows) from the offical download page
2.) run `ollama run llama3.2`

### C/C++ (Wii Remote API)

This repository contains submodule(s). Before we begin, please run
```
git submodule update --init --recursive
```
to pull said submodules' code into this repository.

#### Building the Wii Controller Program

In order to build the binaries for this project, you will need [cmake](https://cmake.org/download/) installed. I recommend installing the latest version (currently 3.31.5 for x86 systems, 64-bit).

After installing cmake, you'll want to add its executable to your systems $Env:PATH variable. To do this, go to Settings > System > About > Advanced System Settings > Environment Variables, then add 'C:\Program Files\CMake\bin' to the Path variable under your both the system and user sections.

Next, head to the wiiuse/ directory of this repository.

Run: 
```
mkdir build
cd build
```
Then:
```
cmake -DBUILD_SHARED_LIBS=ON ..
cmake --build . --config Release
```
This will generate the .lib and .dll executables for the wiiuse package (located at wiiuse/build/src/Release/).

Next, head to the top-level of this directory.
Run: 
```
mkdir build
cd build
```
Then:
```
cmake ..
cmake --build . --config Release
```
This will generate the main executable for this project.

To run the wiimote controller program, simply run:
```
.\start
```

## How to Run (once installed)

1. Connect Wiimote to your pc

    - [Windows 11](https://www.youtube.com/watch?v=J-s9gZJNp8o)
    - [Windows 10](https://www.youtube.com/watch?v=jsZmR-z0IOE)

2. Open executable `launcher.exe` to open the browser.

    - This executable will open the browser, a Llama instance, begin to connect the Wiimote to the c library

3. Mash `1` + `2` on your Wiimote until sounds plays

4. Enjoy!