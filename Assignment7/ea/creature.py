import random

import pyrosim.pyrosim as pyrosim

def Transform_Link(name, size, pos):
  sensor_tag = random.sample([True,False],k=1)[0]
  color_name = 'green' if sensor_tag else 'red'
  link_color = '0 1.0 0 1.0' if sensor_tag else '0 0 1.0 1.0'
  link_dict = {
    "name": name,
    "size": size,
    "pos": pos,
    'sensor_tag': sensor_tag, 'color': link_color, 'color_name': color_name,
  }
  return link_dict

def generate_sec(leg_type, sec_width_range, sec_length_rage, leg_width_range, leg_length_range):
  # size 
  body_size_x, upper_leg_size_x, lower_leg_size_x = -1, 0, 0
  while (body_size_x < upper_leg_size_x )or (body_size_x < lower_leg_size_x):
    body_size_x, body_size_y, body_size_z = random.uniform(*sec_length_rage), random.uniform(*sec_width_range), random.uniform(*sec_width_range)
    if leg_type == "spider":
      upper_leg_size_x =  random.uniform(*leg_width_range)
      upper_leg_size_y =  random.uniform(*leg_length_range)
      upper_leg_size_z =  random.uniform(*leg_width_range)
    elif leg_type == "qudrapedal":
      upper_leg_size_x =  random.uniform(*leg_width_range)
      upper_leg_size_y =  random.uniform(*leg_width_range)
      upper_leg_size_z =  random.uniform(*leg_length_range)
    lower_leg_size_x = random.uniform(*leg_width_range)
    lower_leg_size_y = random.uniform(*leg_width_range)
    lower_leg_size_z = random.uniform(*leg_length_range)
  return (body_size_x, body_size_y, body_size_z), (upper_leg_size_x, upper_leg_size_y, upper_leg_size_z), (lower_leg_size_x,lower_leg_size_y,lower_leg_size_z)


def Geneate_Climber():
  # shape is good at climbing the steps 
  links, joints = {}, {}

  # number of section, for each section, (body szie, leg type, leg size)
  num_sec = random.randint(2,5)
  sec_width_range, sec_length_rage = (0.1, 0.5), (0.1, 0.5)
  sec_connection_type = random.sample(["snake","horse",],k=1)[0]
  leg_type = random.sample(["spider","qudrapedal",],k=1)[0]
  leg_width_range, leg_length_range = (0.1, 0.3), (0.2, 0.6)

  # size 
  (body_size_x, body_size_y, body_size_z), \
  (upper_leg_size_x, upper_leg_size_y, upper_leg_size_z), \
  (lower_leg_size_x,lower_leg_size_y,lower_leg_size_z) \
  = generate_sec(leg_type, sec_width_range, sec_length_rage, leg_width_range, leg_length_range)

  # links
  for i in range(num_sec):
    # (body_size_x, body_size_y, body_size_z), \
    # (upper_leg_size_x, upper_leg_size_y, upper_leg_size_z), \
    # (lower_leg_size_x,lower_leg_size_y,lower_leg_size_z) \
    # = generate_sec(leg_type, sec_width_range, sec_length_rage, leg_width_range, leg_length_range)
    # pos
    if i == 0:
      body_pos_x, body_pos_y, body_pos_z = body_size_x/2.0, 0,  upper_leg_size_z + lower_leg_size_z
    else:
      body_pos_x, body_pos_y, body_pos_z = body_size_x/2.0, 0, 0
    link_dict = Transform_Link(f"body{i}", [body_size_x, body_size_y, body_size_z], [body_pos_x, body_pos_y, body_pos_z])
    links[f"body{i}"] = link_dict
    # right leg
    right_upper_pos_x, right_upper_pos_y, right_upper_pos_z = 0, -upper_leg_size_y/2.0, -upper_leg_size_z/2.0
    left_upper_pos_x, left_upper_pos_y, left_upper_pos_z = 0, upper_leg_size_y/2.0, -upper_leg_size_z/2.0
    if leg_type == "spider":
      right_lower_pos_x, right_lower_pos_y, right_lower_pos_z = 0, -lower_leg_size_y/2.0, -lower_leg_size_z/2.0
      left_lower_pos_x, left_lower_pos_y, left_lower_pos_z = 0, lower_leg_size_y/2.0, -lower_leg_size_z/2.0
    elif leg_type == "qudrapedal":
      right_lower_pos_x, right_lower_pos_y, right_lower_pos_z = 0, 0, -lower_leg_size_z/2.0
      left_lower_pos_x, left_lower_pos_y, left_lower_pos_z = 0, 0, -lower_leg_size_z/2.0
    link_dict = Transform_Link(f"RightUpperLeg{i}", [upper_leg_size_x, upper_leg_size_y, upper_leg_size_z], \
    [right_upper_pos_x, right_upper_pos_y, right_upper_pos_z])
    links[f"RightUpperLeg{i}"] = link_dict
    link_dict = Transform_Link(f"LeftUpperLeg{i}", [upper_leg_size_x, upper_leg_size_y, upper_leg_size_z], \
    [left_upper_pos_x, left_upper_pos_y, left_upper_pos_z])
    links[f"LeftUpperLeg{i}"] = link_dict
    link_dict = Transform_Link(f"RightLowerLeg{i}", [lower_leg_size_x, lower_leg_size_y, lower_leg_size_z], \
    [right_lower_pos_x, right_lower_pos_y, right_lower_pos_z])
    links[f"RightLowerLeg{i}"] = link_dict
    link_dict = Transform_Link(f"LeftLowerLeg{i}", [lower_leg_size_x, lower_leg_size_y, lower_leg_size_z], \
    [left_lower_pos_x, left_lower_pos_y, left_lower_pos_z])
    links[f"LeftLowerLeg{i}"] = link_dict

  # generate sec joint
  for i in range(num_sec):
    # body joint
    if i < num_sec-1:
      parent, child = f"body{i}", f"body{i+1}"
      joint_name = f"{parent}_{child}"
      if i == 0: 
        pos_x, pos_y, pos_z = links[parent]["size"][0], 0, links[parent]["pos"][2]
      else:
        pos_x, pos_y, pos_z = links[parent]["size"][0], 0, 0
      if sec_connection_type == "snake":
        joint_axis = "0 0 1"
      elif sec_connection_type == "horse":
        joint_axis = "0 1 0"
      joint_dict = {
      'name': joint_name,
      'parent': parent, 'child': child, 
      'position': [pos_x, pos_y, pos_z], 'jointAxis': joint_axis,
      }
      joints[joint_name] = joint_dict
    # right upper
    parent, child  = f"body{i}", f"RightUpperLeg{i}"
    joint_name = f"{parent}_{child}"
    if i == 0:
      pos_x, pos_y, pos_z = links[parent]["size"][0]/2.0, -links[parent]["size"][1]/2.0, links[parent]["pos"][2]
    else:
      pos_x, pos_y, pos_z = links[parent]["size"][0]/2.0, -links[parent]["size"][1]/2.0, 0
    if leg_type == "spider":
      joint_axis = "1 0 0 "
    elif leg_type == "qudrapedal":
      joint_axis = "0 1 0"
    joint_dict = {'name': joint_name,'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z], 'jointAxis': joint_axis,}
    joints[joint_name] = joint_dict
    # left upper 
    parent, child  = f"body{i}", f"LeftUpperLeg{i}"
    joint_name = f"{parent}_{child}"
    if i == 0:
      pos_x, pos_y, pos_z = links[parent]["size"][0]/2.0, links[parent]["size"][1]/2.0, links[parent]["pos"][2]
    else:
      pos_x, pos_y, pos_z = links[parent]["size"][0]/2.0, links[parent]["size"][1]/2.0, 0
    if leg_type == "spider":
      joint_axis = "1 0 0 "
    elif leg_type == "qudrapedal":
      joint_axis = "0 1 0"
    joint_dict = {'name': joint_name,'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z], 'jointAxis': joint_axis,}
    joints[joint_name] = joint_dict
    # right_lower
    parent, child  = f"RightUpperLeg{i}", f"RightLowerLeg{i}"
    joint_name = f"{parent}_{child}"
    if leg_type == "spider":
      joint_axis = "1 0 0 "
      pos_x, pos_y, pos_z = 0, -links[parent]["size"][1], -links[parent]["size"][2]
    elif leg_type == "qudrapedal":
      joint_axis = "0 1 0"
      pos_x, pos_y, pos_z = 0, -links[parent]["size"][1]/2.0, -links[parent]["size"][2]
    joint_dict = {'name': joint_name,'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z], 'jointAxis': joint_axis,}
    joints[joint_name] = joint_dict
    #left lower
    parent, child  = f"LeftUpperLeg{i}", f"LeftLowerLeg{i}"
    joint_name = f"{parent}_{child}"
    if leg_type == "spider":
      joint_axis = "1 0 0 "
      pos_x, pos_y, pos_z = 0, links[parent]["size"][1], -links[parent]["size"][2]
    elif leg_type == "qudrapedal":
      joint_axis = "0 1 0"
      pos_x, pos_y, pos_z = 0, links[parent]["size"][1]/2.0, -links[parent]["size"][2]
    joint_dict = {'name': joint_name,'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z], 'jointAxis': joint_axis,}
    joints[joint_name] = joint_dict

  # generate urdf file
  pyrosim.Start_URDF("./data/body.urdf")
  for link_dict in links.values():
    pyrosim.Send_Cube(name=link_dict['name'], pos=link_dict['pos'], size=link_dict['size'], color=link_dict['color'], color_name=link_dict['color_name'])
  for joint_dict in joints.values():
    pyrosim.Send_Joint(name=joint_dict['name'], parent=joint_dict['parent'], child=joint_dict['child'], \
      type = "revolute", position=joint_dict['position'], jointAxis=joint_dict['jointAxis'])
  pyrosim.End()
  return list(links.values()), list(joints.values())


def Generate_Snake():
  # generate a snake along x axis
  # generate all n links(name,position and size) and n-1 joints(name, parent, child, position and jointAxis)
  links, joints = [], []
  link_number = random.randint(3,15) #3 15
  for i in range(link_number):
    size_range = (0.2,1.5) #0.2 1.5
    size_x, size_y, size_z = random.uniform(*size_range), random.uniform(*size_range), random.uniform(*size_range)
    if i ==0:
      pos_x, pos_y, pos_z = size_x/2.0, 0.0, size_z/2.0 #a snake along x axis
    else:
      parent_size_z = links[i-1]['size'][2]
      relative_posz = size_z/2.0 - parent_size_z/2.0 
      pos_x, pos_y, pos_z = size_x/2.0, 0.0, relative_posz #a snake along x axis
    sensor_tag = random.sample([True,False],k=1)[0]
    color_name = 'green' if sensor_tag else 'red'
    link_color = '0 1.0 0 1.0' if sensor_tag else '0 0 1.0 1.0'
    link_dict = {
      "name": f"link{i}",
      "size": [size_x, size_y, size_z],
      "pos": [pos_x, pos_y, pos_z],
      'sensor_tag': sensor_tag, 'color': link_color, 'color_name': color_name,
    }
    links.append(link_dict)

  for i in range(link_number-1):
    parent,child = links[i]['name'], links[i+1]['name']
    joint_name = f'{parent}_{child}'
    parent_size_z = links[i]['size'][2]
    if i ==0:
      position_x, position_y, position_z = links[i]['size'][0], 0, parent_size_z/2.0 #a snake along x axis
    else:
      parent_of_parent_size_z = links[i-1]['size'][2]
      position_x, position_y, position_z = links[i]['size'][0], 0, parent_size_z/2.0 - parent_of_parent_size_z/2.0 #a snake along x axis
    # jointAxis = '0 0 1' #rotate along z axis
    joint_axis_type = random.sample(['z','y'],k=1)[0]
    jointAxis = '0 0 1' if joint_axis_type=='z' else '0 1 0' #rotate along z axis or y axis
    joint_dict = {
      'name': joint_name,
      'parent': parent, 'child': child, 
      'position': [position_x, position_y, position_z], 'jointAxis': jointAxis,
    }
    joints.append(joint_dict)

  #generating urdf
  pyrosim.Start_URDF("./data/body.urdf")
  for i in range(link_number):
    link_dict = links[i]
    pyrosim.Send_Cube(name=link_dict['name'], pos=link_dict['pos'], size=link_dict['size'], color=link_dict['color'], color_name=link_dict['color_name'])
    if i<link_number-1:
      joint_dict = joints[i]
      pyrosim.Send_Joint(name=joint_dict['name'], parent=joint_dict['parent'], child=joint_dict['child'], \
      type = "revolute", position=joint_dict['position'], jointAxis=joint_dict['jointAxis'])
  pyrosim.End()
  return links,joints

def Create_World(links=None, joints=None):
  pyrosim.Start_SDF("./data/world.sdf")
  delta_x, delta_z = 1.5, 0.2
  init_x = 1.0
  if joints and links:
    init_x = sum([l['size'][0] for l in links if 'body' in l['name']]) + 0.75
  mass=100.0
  pyrosim.Send_Cube(name="Box1", pos=[init_x+delta_x*0.5,0,delta_z/2.0] , size=[delta_x,20,delta_z], mass=mass)
  pyrosim.Send_Cube(name="Box2", pos=[init_x+delta_x*1.5,0,(delta_z*2)/2.0] , size=[delta_x,20,delta_z*2], mass=mass)
  pyrosim.Send_Cube(name="Box3", pos=[init_x+delta_x*2.5,0,(delta_z*3)/2.0] , size=[delta_x,20,delta_z*3], mass=mass)
  pyrosim.Send_Cube(name="Box4", pos=[init_x+delta_x*3.5,0,(delta_z*4)/2.0] , size=[delta_x,20,delta_z*4], mass=mass)
  pyrosim.Send_Cube(name="Box5", pos=[init_x+delta_x*4.5,0,(delta_z*5)/2.0] , size=[delta_x,20,delta_z*5], mass=mass)
  pyrosim.Send_Cube(name="Box6", pos=[init_x+delta_x*5.5,0,(delta_z*6)/2.0] , size=[delta_x,20,delta_z*6], mass=mass)
  pyrosim.End()
  return