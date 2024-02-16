import triad_openvr
import time
import sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation
import csv
import datetime
import matplotlib.pyplot as plt

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

if len(sys.argv) == 1:
    interval = 1 / 250
elif len(sys.argv) == 2:
    interval = 1 / float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False

if interval:
    data = []
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")  # Create a single axis

    tracker_names = ["tracker_1", "tracker_2"]
    poses = [np.eye(4)] * len(tracker_names)
    positions = [np.zeros(3)] * len(tracker_names)
    orientations = [np.eye(3)] * len(tracker_names)
    while True:
        start = time.time()
        for ii in range(len(tracker_names)):
            poses[ii] = np.asarray(
                v.devices[tracker_names[ii]].get_pose_matrix()._getArray()
            )
            positions[ii] = poses[ii][:3, 3]
            orientations[ii] = poses[ii][:3, :3]

            ax.cla()

            # Calculate the relative position and orientation of tracker_2 with respect to tracker_1
            relative_position = positions[1] - positions[0]
            relative_orientation = np.dot(
                np.linalg.inv(orientations[0]), orientations[1]
            )
            print("Relative Position:", relative_position)
            print("Relative Orientation:")
            print(relative_orientation)

            ax.quiver(
                positions[0][0],
                positions[0][1],
                positions[0][2],
                relative_orientation[0, 0],
                relative_orientation[1, 0],
                relative_orientation[2, 0],
                color="r",
            )
            ax.quiver(
                positions[0][0],
                positions[0][1],
                positions[0][2],
                relative_orientation[0, 1],
                relative_orientation[1, 1],
                relative_orientation[2, 1],
                color="g",
            )
            ax.quiver(
                positions[0][0],
                positions[0][1],
                positions[0][2],
                relative_orientation[0, 2],
                relative_orientation[1, 2],
                relative_orientation[2, 2],
                color="b",
            )

            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")

            ax.set_xlim([-1, 1])
            ax.set_ylim([-1, 1])
            ax.set_zlim([-1, 1])

            # Save position and orientation to CSV file
            with open("tracker_data.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        tracker_names[ii],
                        datetime.datetime.now(),
                        positions[0][0],
                        positions[0][1],
                        positions[0][2],
                        orientations[0][0, 0],
                        orientations[0][0, 1],
                        orientations[0][0, 2],
                        orientations[0][1, 0],
                        orientations[0][1, 1],
                        orientations[0][1, 2],
                        orientations[0][2, 0],
                        orientations[0][2, 1],
                        orientations[0][2, 2],
                    ]
                )

            plt.pause(0.001)
