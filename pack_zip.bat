if not exist "%~dp0santas_level_editor" mkdir "%~dp0santas_level_editor"
move /y "%~dp0__init__.py" "%~dp0santas_level_editor\__init__.py"
move /y "%~dp0exporter.py" "%~dp0santas_level_editor\exporter.py"
move /y "%~dp0per_object_info.py" "%~dp0santas_level_editor\per_object_info.py"
if exist "%~dp0santas_level_editor.zip" del "%~dp0santas_level_editor.zip"
powershell -Command "Compress-Archive -Path .\santas_level_editor" -DestinationPath "santas_level_editor.zip"
move /y "%~dp0santas_level_editor\__init__.py" "%~dp0__init__.py"
move /y "%~dp0santas_level_editor\exporter.py" "%~dp0exporter.py"
move /y "%~dp0santas_level_editor\per_object_info.py" "%~dp0per_object_info.py"
rmdir /q "%~dp0santas_level_editor"
pause