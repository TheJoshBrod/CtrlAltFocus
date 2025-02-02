# Development start script for main.cpp

# TODO: Replace this eventually by starting the cpp process in python server

# Define working directory
$workingDir = "."

# Define source and destination paths for DLL and EXE
$dllSource = "$workingDir\wiiuse\build\src\Release\wiiuse.dll"
$exeSource = "$workingDir\build\src\Release\main.exe"
$dllDest = "$workingDir\wiiuse.dll"
$exeDest = "$workingDir\main.exe"

# Copy the DLL and EXE files to the working directory
Copy-Item -Path $dllSource -Destination $dllDest -Force
Copy-Item -Path $exeSource -Destination $exeDest -Force

# Run the EXE file
Write-Host "Running main.exe..."
Start-Process -FilePath $exeDest -Wait

# After execution, clean up the copied files
Write-Host "Cleaning up..."
Remove-Item -Path $dllDest -Force
Remove-Item -Path $exeDest -Force

Write-Host "Done!"
