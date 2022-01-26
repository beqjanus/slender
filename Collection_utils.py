'''
Utility functions for interacting with Collections
'''
'''
Copyright (C) 2019 Beq Janus


Created by Beq Janus (beqjanus@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
Find the first collection that this object belongs to
'''

import bpy

def hide_all_collections():
    for collection in bpy.context.window.view_layer.layer_collection.children:
        if collection is not None:
            collection.hide_viewport = True
def show_all_collections():
    for collection in bpy.data.collections:
        if collection is not None:
            collection.hide_viewport = False

def show_slender_collection(collection_name, show=True):
    collection = bpy.data.collections[collection_name]
    if show == True :
        bpy.context.window.view_layer.layer_collection.children['SLender'].hide_viewport = not show
    if collection is not None:
        # collection.hide_viewport = not show
        bpy.context.window.view_layer.layer_collection.children['SLender'].children[collection_name].hide_viewport= not show

def is_collection_visible(collection_name):
    collection = bpy.data.collections[collection_name]
    if collection is not None:
        if(collection.hide_viewport == True):
            return False
        return not bpy.context.window.view_layer.layer_collection.children['SLender'].children[collection_name].hide_viewport


def find_collection_for_object(item):
    collections = item.users_collection
    if len(collections) > 0:
        return collections[0]
    return bpy.context.scene.collection

def find_collection(collection_name):
    if collection_name in bpy.data.collections:
        return bpy.data.collections[collection_name]
    return None

def make_child_collection(collection_name, parent_collection):
    if collection_name in bpy.data.collections: # Does the collection already exist?
        return bpy.data.collections[collection_name]
    else:
        new_collection = bpy.data.collections.new(collection_name)
        if parent_collection is not None:
            parent_collection.children.link(new_collection) # Add the new collection under a parent
        else:
            bpy.context.scene.collection.children.link(new_collection)
        return new_collection

def make_collection(collection_name):
    return make_child_collection(collection_name, None)

def collection_exists(collection_name):
    if collection_name in bpy.data.collections: # Does the collection already exist?
        return True
    return False

def is_in_collection(item, collection_name):
    if collection_name in [coll.name for coll in item.users_collection]:
        return True
    return False

def copy_to_collection(item, collection_name):
    to_collection = find_collection(collection_name)
    if to_collection is not None:
        to_collection.objects.link(item)  # put the item in the new collection

def move_to_collection(item, collection_name):
    if len (item.users_collection) == 1:
        from_collection=item.users_collection[0]
    else:
        from_collection=None

    to_collection = find_collection(collection_name)
    if to_collection is not None:
        to_collection.objects.link(item)  # put the item in the new collection
        if from_collection is not None:
            from_collection.objects.unlink(item) # unlink from the existing collection IFF we linked it to a new one.
