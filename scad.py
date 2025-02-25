import copy
import opsc
import oobb
import oobb_base
import yaml
import os

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    # save_type variables
    if True: 
        filter = ""
        filter = "lay_flat"

        kwargs["save_type"] = "none"
        kwargs["save_type"] = "all"
        
        navigation = False
        #navigation = True    

        kwargs["overwrite"] = True
        
        #kwargs["modes"] = ["3dpr", "laser", "true"]
        kwargs["modes"] = ["3dpr"]
        #kwargs["modes"] = ["laser"]

    # default variables
    if True:
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        part_default = {} 
        part_default["project_name"] = "oomlout_oobb_holder_stationery_clip_binder" ####### neeeds setting
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["width"] = 3
        p3["height"] = 1
        p3["thickness"] = 12
        part["kwargs"] = p3
        part["name"] = "string_version"
        parts.append(part)
        

        sizes = []
        sizes.append([3,1,9])
        sizes.append([3,2,9])
        sizes.append([3,3,9])


        for size in sizes:
            part = copy.deepcopy(part_default)
            p3 = copy.deepcopy(kwargs)
            p3["width"] = size[0]
            p3["height"] = size[1]
            p3["thickness"] = size[2]
            p3["extra"] = "stationery_clip_binder_38_mm_width_metal"
            part["kwargs"] = p3
            part["name"] = "oobb_version"
            parts.append(part)

        sizes = []
        sizes.append([3,1,6])
        sizes.append([3,2,6])
        for size in sizes:
            part = copy.deepcopy(part_default)
            p3 = copy.deepcopy(kwargs)
            p3["width"] = size[0]
            p3["height"] = size[1]
            p3["thickness"] = size[2]
            p3["extra"] = "stationery_clip_binder_38_mm_width_metal"
            part["kwargs"] = p3
            part["name"] = "screw_wood_version"
            parts.append(part)


        sizes = []
        sizes.append([3,2,6])  
        extras = []
        extras.append("stationery_clip_binder_38_mm_width_metal")
        extras.append("stationery_clip_binder_100_mm_width_metal")      
        for size in sizes:
            for extra in extras:
                part = copy.deepcopy(part_default)
                p3 = copy.deepcopy(kwargs)
                p3["width"] = size[0]
                p3["height"] = size[1]
                p3["thickness"] = size[2]
                p3["extra"] = extra
                part["kwargs"] = p3
                part["name"] = "lay_flat_version"
                parts.append(part)



    #make the parts
    if True:
        for part in parts:
            name = part.get("name", "default")            
            extra = part["kwargs"].get("extra", "")
            if filter in name or filter in extra:
                print(f"making {part['name']}")
                make_scad_generic(part)            
                print(f"done {part['name']}")
            else:
                print(f"skipping {part['name']}")


    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        generate_navigation(sort = sort)

def get_base(thing, **kwargs):
    extra = kwargs.get("extra", "")
    if "stationery_clip_binder_38_mm_width_metal" in extra:
        return get_base_38_mm(thing, **kwargs)
    elif "stationery_clip_binder_100_mm_width_metal" in extra:
        return get_base_100_mm(thing, **kwargs)

def get_base_38_mm(thing, **kwargs):

    string_level = 3

    prepare_print = kwargs.get("prepare_print", True)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[2] += -depth/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    #oobb_base.append_full(thing,**p3)

    #add connecting screw_countersunk
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = depth
    p3["nut"] = True
    p3["overhang"] = True
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2
    poss = []
    pos11 = copy.deepcopy(pos1)
    pos11[0] += 15
    poss.append(pos11)
    pos12 = copy.deepcopy(pos1)
    pos12[0] -= 15
    poss.append(pos12)
    p3["pos"] = poss
    rot1 = copy.deepcopy(rot)
    #rot1[0] += 180
    p3["rot"] = rot1
    oobb_base.append_full(thing,**p3)

    #cutout for clip
    position_clip = copy.deepcopy(pos)
    position_clip[1] += -4
    position_clip[2] += 3
    

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cylinder"
    radius_clip = 17/2
    depth_clip = 2
    p3["radius"] = radius_clip
    p3["depth"] = depth_clip
    #p3["m"] = "#"
    pos1 = copy.deepcopy(position_clip)
    pos1[2] += -depth_clip/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add countersunk screw
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = depth - string_level
    p3["nut"] = True
    p3["overhang"] = True
    p3["clearance"] = True
    p3["m"] = "#"
    pos1 = copy.deepcopy(position_clip)
    pos1[2] += -depth + string_level
    p3["pos"] = pos1
    rot1 = copy.deepcopy(rot)
    #rot1[0] += 180
    p3["rot"] = rot1
    p3["zz"] = "bottom"
    oobb_base.append_full(thing,**p3)

    

    #add string cutout cube
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    w = width*15
    s = 1.5
    h = s
    d = s
    p3["size"] = [w,h,d]
    p3["depth"] = depth
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += 0
    pos1[1] += 5
    pos1[2] += -d + 3
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)


    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        pos1[2] += string_level + 3
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[2] += string_level
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_base_100_mm(thing, **kwargs):
    pass

def get_oobb_version(thing, **kwargs):
    extra = kwargs.get("extra", "")
    if "stationery_clip_binder_38_mm_width_metal" in extra:
        return get_oobb_version_38_mm(thing, **kwargs)
    elif "stationery_clip_binder_100_mm_width_metal" in extra:
        return get_oobb_version_100_mm(thing, **kwargs)

def get_oobb_version_38_mm(thing, **kwargs):

    string_level = 3

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[2] += -depth/2
    if height !=1:
        pos1[1] += (height-1) * 7.5
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = ["top","bottom"]
    if height > 1:
        p3["holes"] = ["top","bottom","right"]
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos1)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    

    #cutout for clip
    position_clip = copy.deepcopy(pos)
    position_clip[1] += -4
    position_clip[2] += depth/2
    

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cylinder"
    radius_clip = 17/2
    depth_clip = 2
    p3["radius"] = radius_clip
    p3["depth"] = depth_clip
    #p3["m"] = "#"
    pos1 = copy.deepcopy(position_clip)
    pos1[2] += -depth_clip/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add countersunk screw
    clearance_screw = 1.5
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = depth - clearance_screw
    p3["nut"] = True
    p3["overhang"] = True
    p3["clearance"] = ["bottom"]
    #p3["m"] = "#"
    pos1 = copy.deepcopy(position_clip)
    pos1[2] += -depth + clearance_screw
    p3["pos"] = pos1
    rot1 = copy.deepcopy(rot)
    #rot1[0] += 180
    p3["rot"] = rot1
    p3["zz"] = "bottom"
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        pos1[2] += string_level + 3
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[2] += string_level
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_lay_flat_version(thing, **kwargs):
    extra = kwargs.get("extra", "")
    if "stationery_clip_binder_38_mm_width_metal" in extra:
        return get_lay_flat_version_38_mm(thing, **kwargs)
    elif "stationery_clip_binder_100_mm_width_metal" in extra:
        return get_lay_flat_version_100_mm(thing, **kwargs)

def get_lay_flat_version_38_mm(thing, **kwargs):
    
    string_level = 3

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[2] += -depth/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = ["single"]
    p3["locations"] = [[1,1],[3,1],[2,2]]    
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos1)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["radius_name"] = "m3"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = ["single"]
    p3["locations"] = [[1,1.5],[3,1.5],[1.5,2],[2.5,2]]    
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos1)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    


    #cutout for clip
    if True:
        position_clip = copy.deepcopy(pos)
        
        depth_clip = 2
        shift_clip_y_big = -17.5
        shift_clip_y_small = -7.5
        clear = 0.5

        #big cube
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        w = 20 + clear
        h = 20 + clear
        d = depth_clip
        size = [w,h,d]
        p3["size"] = size
        #p3["m"] = "#"
        pos1 = copy.deepcopy(position_clip)
        pos1[0] += 0
        pos1[1] += shift_clip_y_big
        pos1[2] += -depth/2
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #small_cube through
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative_negative"
        p3["shape"] = f"oobb_cube"
        w = 15 + clear
        h = 10 + clear
        d = depth
        size = [w,h,d]
        p3["size"] = size
        p3["m"] = "#"
        pos1 = copy.deepcopy(position_clip)
        pos1[0] += 0
        pos1[1] += -17
        pos1[2] += -depth/2
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #small cylinder
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cylinder"
        p3["radius"] = 20/2 + clear/2
        d = depth_clip
        p3["depth"] = d
        #p3["m"] = "#"
        pos1 = copy.deepcopy(position_clip)
        pos1[0] += 0
        pos1[1] += shift_clip_y_small
        pos1[2] += -depth/2
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #spring_clearnce
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative_negative"
        p3["shape"] = f"oobb_cube"
        w = 5 + clear
        h = 15 + clear
        d = depth
        size = [w,h,d]
        p3["size"] = size
        p3["m"] = "#"
        pos1 = copy.deepcopy(position_clip)
        pos1[0] += -7
        pos1[1] += -15
        pos1[2] += -depth/2
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #add press_cylinder
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive_positive"
        p3["shape"] = f"oobb_cylinder"
        p3["radius"] = 14/2
        p3["depth"] = depth
        #p3["m"] = "#"
        pos1 = copy.deepcopy(position_clip)
        pos1[1] += -7.5
        pos1[2] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

    #add screws
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative_negative"
        p3["shape"] = f"oobb_screw_countersunk"
        p3["radius_name"] = "m3_screw_wood"
        p3["depth"] = depth
        p3["overhang"] = True
        p3["m"] = "#"
        pos1 = copy.deepcopy(position_clip)
        pos1[2] += -depth/2
        poss = []
        pos11 = copy.deepcopy(pos1)
        pos11[0] += 15
        pos11[1] += 7.5        
        poss.append(pos11)
        pos12 = copy.deepcopy(pos1)
        pos12[0] += -15
        pos12[1] += 7.5
        poss.append(pos12)
        pos13 = copy.deepcopy(pos1)        
        pos13[1] += -7.5
        poss.append(pos13)
        p3["pos"] = poss
        rot1 = copy.deepcopy(rot)
        #rot1[0] += 180
        p3["rot"] = rot1
        p3["zz"] = "bottom"
        oobb_base.append_full(thing,**p3)


    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        pos1[2] += string_level + 3
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[2] += string_level
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_lay_flat_version_100_mm(thing, **kwargs):

    string_level = 3

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[2] += -depth/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = ["top","bottom"]
    if height > 1:
        p3["holes"] = ["top","bottom","right"]
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos1)         
    p3["pos"] = pos1
    #oobb_base.append_full(thing,**p3)

    

    #cutout for clip
    if True:
        position_clip = copy.deepcopy(pos)
        
        depth_clip = 2.5
        shift_clip_y_big = -22.5
        shift_clip_y_small = -3.5
        clear = 0.5

        #big cube
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        w = 34 + clear
        h = 30 + clear
        d = depth_clip
        size = [w,h,d]
        p3["size"] = size
        #p3["m"] = "#"
        pos1 = copy.deepcopy(position_clip)
        pos1[0] += 0
        pos1[1] += shift_clip_y_big
        pos1[2] += -depth/2
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #small cube
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        w = 24 + clear
        h = 8 + clear
        d = depth_clip
        size = [w,h,d]
        p3["size"] = size
        #p3["m"] = "#"
        pos1 = copy.deepcopy(position_clip)
        pos1[0] += 0
        pos1[1] += shift_clip_y_small
        pos1[2] += -depth/2
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #spring_clearnce
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        w = 5 + clear
        h = 15 + clear
        d = depth
        size = [w,h,d]
        p3["size"] = size
        p3["m"] = "#"
        pos1 = copy.deepcopy(position_clip)
        pos1[0] += -13
        pos1[1] += -15
        pos1[2] += -depth/2
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #add press_cylinder
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive_positive"
        p3["shape"] = f"oobb_cylinder"
        p3["radius"] = 14/2
        p3["depth"] = depth
        #p3["m"] = "#"
        pos1 = copy.deepcopy(position_clip)
        pos1[1] += -7.5
        pos1[2] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

    #add screws
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative_negative"
        p3["shape"] = f"oobb_screw_countersunk"
        p3["radius_name"] = "m3_screw_wood"
        p3["depth"] = depth
        p3["overhang"] = True
        p3["m"] = "#"
        pos1 = copy.deepcopy(position_clip)
        pos1[2] += -depth/2
        poss = []
        pos11 = copy.deepcopy(pos1)
        pos11[0] += 15
        pos11[1] += 7.5        
        poss.append(pos11)
        pos12 = copy.deepcopy(pos1)
        pos12[0] += -15
        pos12[1] += 7.5
        poss.append(pos12)
        pos13 = copy.deepcopy(pos1)        
        pos13[1] += -7.5
        poss.append(pos13)
        p3["pos"] = poss
        rot1 = copy.deepcopy(rot)
        #rot1[0] += 180
        p3["rot"] = rot1
        p3["zz"] = "bottom"
        oobb_base.append_full(thing,**p3)


    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        pos1[2] += string_level + 3
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[2] += string_level
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_base_38_mm(thing, **kwargs):

    string_level = 3

    prepare_print = kwargs.get("prepare_print", True)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[2] += -depth/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    #oobb_base.append_full(thing,**p3)

    #add connecting screw_countersunk
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = depth
    p3["nut"] = True
    p3["overhang"] = True
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2
    poss = []
    pos11 = copy.deepcopy(pos1)
    pos11[0] += 15
    poss.append(pos11)
    pos12 = copy.deepcopy(pos1)
    pos12[0] -= 15
    poss.append(pos12)
    p3["pos"] = poss
    rot1 = copy.deepcopy(rot)
    #rot1[0] += 180
    p3["rot"] = rot1
    oobb_base.append_full(thing,**p3)

    #cutout for clip
    position_clip = copy.deepcopy(pos)
    position_clip[1] += -4
    position_clip[2] += 3
    

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cylinder"
    radius_clip = 17/2
    depth_clip = 2
    p3["radius"] = radius_clip
    p3["depth"] = depth_clip
    #p3["m"] = "#"
    pos1 = copy.deepcopy(position_clip)
    pos1[2] += -depth_clip/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add countersunk screw
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = depth - string_level
    p3["nut"] = True
    p3["overhang"] = True
    p3["clearance"] = True
    p3["m"] = "#"
    pos1 = copy.deepcopy(position_clip)
    pos1[2] += -depth + string_level
    p3["pos"] = pos1
    rot1 = copy.deepcopy(rot)
    #rot1[0] += 180
    p3["rot"] = rot1
    p3["zz"] = "bottom"
    oobb_base.append_full(thing,**p3)

    

    #add string cutout cube
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    w = width*15
    s = 1.5
    h = s
    d = s
    p3["size"] = [w,h,d]
    p3["depth"] = depth
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += 0
    pos1[1] += 5
    pos1[2] += -d + 3
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)


    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        pos1[2] += string_level + 3
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[2] += string_level
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)




def get_string_version(thing, **kwargs):

    string_level = 3

    prepare_print = kwargs.get("prepare_print", True)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[2] += -depth/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    #oobb_base.append_full(thing,**p3)

    #add connecting screw_countersunk
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = depth
    p3["nut"] = True
    p3["overhang"] = True
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2
    poss = []
    pos11 = copy.deepcopy(pos1)
    pos11[0] += 15
    poss.append(pos11)
    pos12 = copy.deepcopy(pos1)
    pos12[0] -= 15
    poss.append(pos12)
    p3["pos"] = poss
    rot1 = copy.deepcopy(rot)
    #rot1[0] += 180
    p3["rot"] = rot1
    oobb_base.append_full(thing,**p3)

    #cutout for clip
    position_clip = copy.deepcopy(pos)
    position_clip[1] += -4
    position_clip[2] += 3
    

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cylinder"
    radius_clip = 17/2
    depth_clip = 2
    p3["radius"] = radius_clip
    p3["depth"] = depth_clip
    #p3["m"] = "#"
    pos1 = copy.deepcopy(position_clip)
    pos1[2] += -depth_clip/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add countersunk screw
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = depth - string_level
    p3["nut"] = True
    p3["overhang"] = True
    #p3["m"] = "#"
    pos1 = copy.deepcopy(position_clip)
    pos1[2] += -depth + string_level
    p3["pos"] = pos1
    rot1 = copy.deepcopy(rot)
    #rot1[0] += 180
    p3["rot"] = rot1
    p3["zz"] = "bottom"
    oobb_base.append_full(thing,**p3)

    

    #add string cutout cube
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    w = width*15
    s = 1.5
    h = s
    d = s
    p3["size"] = [w,h,d]
    p3["depth"] = depth
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += 0
    pos1[1] += 5
    pos1[2] += -d + 3
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)


    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        pos1[2] += string_level + 3
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[2] += string_level
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_screw_wood_version(thing, **kwargs):

    string_level = 3

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[2] += -depth/2
    if height !=1:
        pos1[1] += (height-1) * 7.5
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = ""
    if height > 1:
        p3["holes"] = ["right"]
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos1)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add screw_countersunk holes radius_name m3_5_wood_screw
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3d5_screw_wood"
    p3["depth"] = depth
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2
    poss = []
    pos11 = copy.deepcopy(pos1)
    pos11[0] += 15
    poss.append(pos11)
    pos12 = copy.deepcopy(pos1)
    pos12[0] -= 15
    poss.append(pos12)
    p3["pos"] = poss
    rot1 = copy.deepcopy(rot)
    #rot1[0] += 180
    p3["rot"] = rot1
    oobb_base.append_full(thing,**p3)

    #cutout for clip
    position_clip = copy.deepcopy(pos)
    position_clip[1] += -4
    position_clip[2] += depth/2
    

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cylinder"
    radius_clip = 17/2
    depth_clip = 2
    p3["radius"] = radius_clip
    p3["depth"] = depth_clip
    #p3["m"] = "#"
    pos1 = copy.deepcopy(position_clip)
    pos1[2] += -depth_clip/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add countersunk screw
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = depth
    p3["nut"] = True
    p3["overhang"] = True
    #p3["m"] = "#"
    pos1 = copy.deepcopy(position_clip)
    pos1[2] += -depth
    p3["pos"] = pos1
    rot1 = copy.deepcopy(rot)
    #rot1[0] += 180
    p3["rot"] = rot1
    p3["zz"] = "bottom"
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        pos1[2] += string_level + 3
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[2] += string_level
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

###### utilities



def make_scad_generic(part):
    
    # fetching variables
    name = part.get("name", "default")
    project_name = part.get("project_name", "default")
    
    kwargs = part.get("kwargs", {})    
    
    modes = kwargs.get("modes", ["3dpr", "laser", "true"])
    save_type = kwargs.get("save_type", "all")
    overwrite = kwargs.get("overwrite", True)

    kwargs["type"] = f"{project_name}_{name}"

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")

    #get the part from the function get_{name}"
    func = globals()[f"get_{name}"]    
    # test if func exists
    if callable(func):            
        func(thing, **kwargs)        
    else:            
        get_base(thing, **kwargs)   
    
    folder = f"scad_output/{thing['id']}"

    for mode in modes:
        depth = thing.get(
            "depth_mm", thing.get("thickness_mm", 3))
        height = thing.get("height_mm", 100)
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2)*3
        if "bunting" in thing:
            start = 0.5
        

        opsc.opsc_make_object(f'{folder}/{mode}.scad', thing["components"], mode=mode, save_type=save_type, overwrite=overwrite, layers=layers, tilediff=tilediff, start=start)  

    yaml_file = f"{folder}/working.yaml"
    with open(yaml_file, 'w') as file:
        part_new = copy.deepcopy(part)
        kwargs_new = part_new.get("kwargs", {})
        kwargs_new.pop("save_type","")
        part_new["kwargs"] = kwargs_new
        import os
        cwd = os.getcwd()
        part_new["project_name"] = cwd
        part_new["id"] = thing["id"]
        part_new["thing"] = thing
        yaml.dump(part_new, file)

def generate_navigation(folder="scad_output", sort=["width", "height", "thickness"]):
    #crawl though all directories in scad_output and load all the working.yaml files
    parts = {}
    for root, dirs, files in os.walk(folder):
        if 'working.yaml' in files:
            yaml_file = os.path.join(root, 'working.yaml')
            #if working.yaml isn't in the root directory, then do it
            if root != folder:
                with open(yaml_file, 'r') as file:
                    part = yaml.safe_load(file)
                    # Process the loaded YAML content as needed
                    part["folder"] = root
                    part_name = root.replace(f"{folder}","")
                    
                    #remove all slashes
                    part_name = part_name.replace("/","").replace("\\","")
                    parts[part_name] = part

                    print(f"Loaded {yaml_file}: {part}")

    pass
    for part_id in parts:
        part = parts[part_id]
        kwarg_copy = copy.deepcopy(part["kwargs"])
        folder_navigation = "navigation_oobb"
        folder_source = part["folder"]
        folder_extra = ""
        for s in sort:
            if s == "name":
                ex = part.get("name", "default")
            else:
                ex = kwarg_copy.get(s, "default")
            folder_extra += f"{s}_{ex}/"

        #replace "." with d
        folder_extra = folder_extra.replace(".","d")            
        folder_destination = f"{folder_navigation}/{folder_extra}"
        if not os.path.exists(folder_destination):
            os.makedirs(folder_destination)
        if os.name == 'nt':
            #copy a full directory auto overwrite
            command = f'xcopy "{folder_source}" "{folder_destination}" /E /I /Y'
            print(command)
            os.system(command)
        else:
            os.system(f"cp {folder_source} {folder_destination}")

if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)