; Inno Setup script for full version "Конструктор схем ВОЛП".
; AppId: {7E59C1B4-C23E-517B-8AA0-6292B5CEF0FF} (UUID v5, volp-constructor.local) — идентификация в реестре и при обновлениях.
; Build after Nuitka: run from project root: iscc build\installer_full.iss
; Requires: main.dist.full\main.dist\ populated (python build/build_variant.py --full, then Nuitka).

#define MyAppName "Конструктор схем ВОЛП"
#define MyAppExe "Конструктор схем ВОЛП.exe"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Конструктор схем ВОЛП"

[Setup]
AppId={{7E59C1B4-C23E-517B-8AA0-6292B5CEF0FF}}
AppName={#MyAppName}
AppVerName={#MyAppName} {#MyAppVersion}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=..\output
OutputBaseFilename=Конструктор схем ВОЛП Setup
SetupIconFile=..\resources\app-icon.ico
UninstallDisplayIcon={app}\{#MyAppExe}
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
WizardStyle=modern
; Оценка места на диске (200 МБ)
ExtraDiskSpaceRequired=209715200
; Закрыть приложение при обновлении, чтобы не блокировать файлы
CloseApplications=yes
CloseApplicationsFilter={#MyAppExe}
; Refresh file associations on install/uninstall
ChangesAssociations=yes

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "Создать значок на рабочем столе"; GroupDescription: "Дополнительные значки:"
Name: "nceassociation"; Description: "Открывать файлы .nce этой программой"; GroupDescription: "Ассоциации файлов:"

[Files]
Source: "..\main.dist.full\main.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"
Name: "{group}\Удалить {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"; Tasks: desktopicon

[Registry]
; Associate .nce with the application (optional task) — per-user, no admin required
Root: HKCU; Subkey: "Software\Classes\.nce"; ValueType: string; ValueName: ""; ValueData: "VolpConstructor.nce"; Flags: uninsdeletevalue; Tasks: nceassociation
Root: HKCU; Subkey: "Software\Classes\VolpConstructor.nce"; ValueType: string; ValueName: ""; ValueData: "Файл проекта ВОЛП"; Flags: uninsdeletekey; Tasks: nceassociation
Root: HKCU; Subkey: "Software\Classes\VolpConstructor.nce\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExe},0"; Tasks: nceassociation
Root: HKCU; Subkey: "Software\Classes\VolpConstructor.nce\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExe}"" ""%1"""; Tasks: nceassociation

[Run]
Filename: "{app}\{#MyAppExe}"; Description: "Запустить {#MyAppName}"; Flags: nowait postinstall skipifsilent
