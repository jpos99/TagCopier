[Setup]
AppName=Tag Copier
AppVersion=1.0
DefaultDirName={pf}\TagCopier
DefaultGroupName=Tag Copier
OutputDir=Output
OutputBaseFilename=TagCopierSetup

[Files]
Source: "dist\TagCopier.exe"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\Tag Copier"; Filename: "{app}\TagCopier.exe"
Name: "{commondesktop}\Tag Copier"; Filename: "{app}\TagCopier.exe" 