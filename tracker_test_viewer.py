import triad_openvr
import time
import sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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
            txt = ""
            for each in v.devices[tracker_names[ii]].get_pose_euler():
                txt += "%.4f" % each
                txt += " "
            print(tracker_names[ii])
            print("\r" + txt, end="")
            print("\n")

            poses[ii] = np.asarray(
                v.devices[tracker_names[ii]].get_pose_matrix()._getArray()
            )
            positions[ii] = poses[ii][:3, 3]
            orientations[ii] = poses[ii][:3, :3]

            ax.cla()

            for position, orientation in zip(positions, orientations):
                # color = "orange" if ii == 0 else "pink"
                # ax.scatter(
                #     positions[ii][0],
                #     positions[ii][1],
                #     positions[ii][2],
                #     color=color,
                #     label=tracker_names[ii] + "_origin",
                # )

                ax.quiver(
                    position[0],
                    position[1],
                    position[2],
                    orientation[0, 0],
                    orientation[1, 0],
                    orientation[2, 0],
                    color="r",
                )
                ax.quiver(
                    position[0],
                    position[1],
                    position[2],
                    orientation[0, 1],
                    orientation[1, 1],
                    orientation[2, 1],
                    color="g",
                )
                ax.quiver(
                    position[0],
                    position[1],
                    position[2],
                    orientation[0, 2],
                    orientation[1, 2],
                    orientation[2, 2],
                    color="b",
                )

            ax.set_xlim([-1, 1])
            ax.set_ylim([-1, 1])
            ax.set_zlim([-1, 1])
            ax.legend()

            plt.pause(0.001)
