import santas_level_editor.exporter as exporter
import santas_level_editor.per_object_info as per_object_info

bl_info = {
	"name": "Santa's level editor",
	"blender": (2, 80, 0),
	"category": "Object",
}

def register():
	per_object_info.register()
	exporter.register()

def unregister():
	exporter.unregister()
	per_object_info.unregister()

if __name__ == "__main__":
	register()