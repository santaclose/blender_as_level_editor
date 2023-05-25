mkdir ./santas_level_editor
mv ./__init__.py ./santas_level_editor/__init__.py
mv ./exporter.py ./santas_level_editor/exporter.py
mv ./per_object_info.py ./santas_level_editor/per_object_info.py
rm ./santas_level_editor.zip
zip -r santas_level_editor.zip santas_level_editor/*
mv ./santas_level_editor/__init__.py ./__init__.py
mv ./santas_level_editor/exporter.py ./exporter.py
mv ./santas_level_editor/per_object_info.py ./per_object_info.py
rm -d ./santas_level_editor