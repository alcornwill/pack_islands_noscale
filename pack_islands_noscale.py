
# Author: Will Alcorn 2017

import bpy
import bmesh
from mathutils import Vector
from bpy.props import BoolProperty, FloatProperty

class PackIslandsNoScale(bpy.types.Operator):
    bl_idname = 'uv.packislands_noscale'
    bl_label = 'Pack Islands No Scale'
    bl_description = 'Pack Islands preserve face scale'
    bl_options = {'REGISTER', 'UNDO'}
    
    rotate = BoolProperty(
        name="Rotate",
        description="Rotate option used by default pack islands function",
        default=False)
    margin = FloatProperty(
        name="Margin",
        description="Margin used by default pack islands function",
        min=0,
        max=1,
        default=0.001)
        
    def execute(self, context):
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        uv_layer = bm.loops.layers.uv.verify()

        selected_faces = [f for f in bm.faces if f.select]
        # get scale of one face
        face = selected_faces[0]
        scale = self.get_face_scale(uv_layer, face)

        # pack islands
        #bpy.ops.uv.pack_islands(rotate=self.rotate, margin=self.margin)
        bpy.ops.uv.pack_islands(rotate=True, margin=0.0)

        # get scale of face again
        scale1 = self.get_face_scale(uv_layer, face)
        # get difference
        dx = scale.x / scale1.x
        dy = scale.y / scale1.y
        # undo scaling
        bpy.context.space_data.cursor_location[0] = 0
        bpy.context.space_data.cursor_location[1] = 0
        bpy.ops.transform.resize(value=(dx, dy, 1))
        
        return {'FINISHED'}
    
    def get_face_scale(self, uv_layer, face):
        max_uv = Vector((-10000000.0, -10000000.0))
        min_uv = Vector((10000000.0, 10000000.0))

        for l in face.loops:
            uv = l[uv_layer].uv
            if uv.x > max_uv.x:
                max_uv.x = uv.x
            if uv.y > max_uv.y:
                max_uv.y = uv.y
            if uv.x < min_uv.x:
                min_uv.x = uv.x
            if uv.y < min_uv.y:
                min_uv.y = uv.y

        return max_uv - min_uv
        
def image_uvs_menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(PackIslandsNoScale.bl_idname)
        
def register():
    bpy.utils.register_class(PackIslandsNoScale)
    bpy.types.IMAGE_MT_uvs.append(image_uvs_menu_fn)

def unregister():
    bpy.utils.unregister_class(PackIslandsNoScale)
    bpy.types.IMAGE_MT_uvs.remove(image_uvs_menu_fn)

if __name__ == "__main__":
    register()