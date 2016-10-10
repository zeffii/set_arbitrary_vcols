# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import random

bl_info = {
    'author': 'zeffii',
    'category': '3D View',
    'description': 'Set vcols by selecting verts/edges/faces and running this operator',
    'name': 'Set Vertex Colors'
}


def set_verts_colors(new_color):

    # must switch to Object Mode briefly to get the new set of selected elements
    # and then change the vertex_color layer
    bpy.ops.object.mode_set(mode='OBJECT')
    obj = bpy.context.active_object

    mesh = obj.data
    color_layer = mesh.vertex_colors.active  
    selected = set(v.index for v in obj.data.vertices if v.select)

    i = 0
    for poly in mesh.polygons:
        for loop_index in poly.loop_indices:
            vidx = mesh.loops[loop_index].vertex_index            
            if vidx in selected:
                color_layer.data[i].color = new_color
            i += 1

    # set to vertex paint mode to see the result
    # bpy.ops.object.mode_set(mode='VERTEX_PAINT')
    bpy.ops.object.mode_set(mode='EDIT')


class BSEVtexSetter(bpy.types.Operator):
    bl_idname = "object.vertex_color_setter"
    bl_label = "Set VCols of any Geometry"
 
    def draw(self, context):
        self.layout.prop(context.scene, 'BSE_new_color')
 
    def execute(self, context):
        set_verts_colors(context.scene.BSE_new_color)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
 
def register():
    bpy.types.Scene.BSE_new_color = bpy.props.FloatVectorProperty(
        name="Color to work with", subtype='COLOR', min=0.0, max=1.0, size=3
    )
    bpy.utils.register_class(BSEVtexSetter)

def unregister():
    bpy.utils.unregister_class(BSEVtexSetter)
    del bpy.types.Scene.BSE_new_color

if __name__ == "__main__":
    register()
