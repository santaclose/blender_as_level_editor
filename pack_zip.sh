mkdir ./santas_level_editor
mv ./__init__.py ./santas_level_editor/__init__.py
mv ./json_exporter.py ./santas_level_editor/json_exporter.py
mv ./obj_tree_exporter.py ./santas_level_editor/obj_tree_exporter.py
mv ./per_object_info.py ./santas_level_editor/per_object_info.py
rm ./santas_level_editor.zip
zip -r santas_level_editor.zip santas_level_editor/*
mv ./santas_level_editor/__init__.py ./__init__.py
mv ./santas_level_editor/json_exporter.py ./json_exporter.py
mv ./santas_level_editor/obj_tree_exporter.py ./obj_tree_exporter.py
mv ./santas_level_editor/per_object_info.py ./per_object_info.py
rm -d ./santas_level_editor