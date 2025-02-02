# SpartaHack-W25

#### This repository contains submodule(s). Before we begin, please run
```
git submodule update --init --recursive
```
#### to pull said submodules' code into this repository.

## Building the Wii Controller Program

### For windows systems

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

