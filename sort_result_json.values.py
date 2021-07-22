#!/usr/bin/env python3
# usage: [THIS SCRIPT] [JSON file from test.py]

import sys
import json
import numpy as np

key_points = ["nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_shoulder", "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist", "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle"]

output1 = open("coordinate_table.txt", "w")
output2 = open("distance_table.txt", "w")

header1 = "image_id\t"
for point in key_points:
	header1 += (point + "\t")
print(header1.rstrip(), file = output1)

header2 = "image_id\t"
for i in range(len(key_points) - 1):
	for j in range(i+1, len(key_points)):
		edge = key_points[i] + "-" + key_points[j]
		header2 += edge + "\t"
print(header2.rstrip(), file = output2)

with open(sys.argv[1]) as INPUT:
	data = json.load(INPUT)

for image in data:
	image_id = image["image_id"]
	keypoints = image["keypoints"]

	out_str1 = str(image_id) + "\t"
	out_str2 = str(image_id) + "\t"
	for i in range(17):
		out_str1 += f"{keypoints[i*3]},{keypoints[i*3 + 1]}\t"
	print(out_str1.rstrip(), file = output1)
	
	for i in range(len(key_points) - 1):
		for j in range(i+1, len(key_points)):
			point1 = np.array([keypoints[i*3], keypoints[i*3+1]])
			point2 = np.array([keypoints[j*3], keypoints[j*3+1]])
			dist = np.linalg.norm(point1 - point2)
			out_str2 += (str(dist) + "\t")
	print(out_str2.rstrip(), file = output2)
	
output1.close()
output2.close()
