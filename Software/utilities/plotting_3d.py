from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations


def set_axes_equal(ax):
    '''
    From https://github.com/mcrovella/CS132-Geometric-Algorithms/blob/master/laUtilities.py

    Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.
    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
      from https://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to
    '''
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


def plotting_data(anchors_coords, position, range_error, num_points):

    anchors_pos = np.copy(anchors_coords)
    num_anchors = len(anchors_pos)

    # Tag position
    tag_pos = position

    # Change the following values to introduce error on the three anchors range.
    # Set to [0, 0, 0] for the error-free case
    range_error = range_error

    NUM_POINTS = num_points

    fig = plt.figure()
    ax = fig.gca(projection='3d', adjustable='box', box_aspect=(1, 1, 1), proj_type='ortho')  # xlim=[-10, 40], ylim=[-10, 40], zlim=[-20, 30],
    # Plot the spheres given by the anchors and tags location
    radius = np.zeros(num_anchors)

    for i in range(num_anchors):
        # Compute the distance from the tag to the anchors. It will be our radius
        radius[i] = np.linalg.norm(anchors_pos[i, :] - tag_pos)
        radius[i] += range_error[i]

        # Plot the sphere
        u = np.linspace(0, 2 * np.pi, NUM_POINTS)
        v = np.linspace(0, np.pi, NUM_POINTS)
        x = anchors_pos[i, 0] + radius[i] * np.outer(np.cos(u), np.sin(v))
        y = anchors_pos[i, 1] + radius[i] * np.outer(np.sin(u), np.sin(v))
        z = anchors_pos[i, 2] + radius[i] * np.outer(np.ones(np.size(u)), np.cos(v))
        color = [(i+1.)/num_anchors, (num_anchors-i)/num_anchors, 0]
        ax.plot_surface(x, y, z,  rstride=4, cstride=4, shade=True, color=[color[0], color[1], color[2], 0.2], alpha=0.05)
        # Plot the sphere center
        ax.scatter(anchors_pos[i, 0], anchors_pos[i, 1], anchors_pos[i, 2], color=color, s=25)

    # Plot the spheres intersections
    # See, for instance, http://www.mat.uc.pt/~engeo/cadeiras/ano3/mg/maiselem.pdf
    # and https://math.stackexchange.com/q/73242
    for i in range(num_anchors):
        for j in range(i+1, num_anchors):
            # Confirm if the intersection is empty, a single point, or a
            # circunference
            dist = np.linalg.norm(anchors_pos[i, :] - anchors_pos[j, :])
            if (dist > radius[i] + radius[j]) or (dist < max(radius[i], radius[j]) - min(radius[i], radius[j])):
                # No intersection exists
                print(f'No interssection exists between sphere {i} and sphere {j}!')
                continue
            elif dist == radius[i] + radius[j]:
                # A single point of intersection (highly unlikely)
                # NOT TESTED YET
                a = anchors_pos[j, 0] - anchors_pos[i, 0]
                b = anchors_pos[j, 1] - anchors_pos[i, 1]
                c = anchors_pos[j, 2] - anchors_pos[i, 2]
                x = anchors_pos[j, 0] + radius[i]*a
                y = anchors_pos[j, 1] + radius[i]*b
                z = anchors_pos[j, 2] + radius[i]*c
                # Plot the intersection point
                ax.scatter(x, y, x, color=[0, 0, 0], s=25)
            else:
                # The intersection is a circunference
                # Vector between from anchor i to j
                axis_centers = np.array([anchors_pos[i, 0] - anchors_pos[j, 0], anchors_pos[i, 1] - anchors_pos[j, 1], anchors_pos[i, 2] - anchors_pos[j, 2]])
                # Normalize vector
                axis_centers = axis_centers/np.linalg.norm(axis_centers)
                # Compute a perpendicular vector to this one
                axis1 = np.zeros(3)
                if not np.isclose(axis_centers[0], 0):
                    axis1[1] = 1.
                    axis1[2] = 1.
                    axis1[0] = (-axis_centers[1]*axis1[1]- axis_centers[2]*axis1[2])/axis_centers[0]
                elif not np.isclose(axis_centers[1], 0):
                    axis1[0] = 1.
                    axis1[2] = 1.
                    axis1[1] = (-axis_centers[0]*axis1[0]- axis_centers[2]*axis1[2])/axis_centers[1]
                elif not np.isclose(axis_centers[2], 0):
                    axis1[0] = 1.
                    axis1[1] = 1.
                    axis1[2] = (-axis_centers[0]*axis1[0]- axis_centers[1]*axis1[1])/axis_centers[2]
                else:
                    raise Exception(f'Anchors {i} and {j} have the same center!')
                # Normalize axis1
                axis1 = axis1/np.linalg.norm(axis1)
                # Compute axis 2, as perpendicular to the vector between the two
                # tags positions and axis1. Axis1 and axis2, which are perpendicular
                # between each other, are the axis that are parallel to the
                # circumference plane.
                axis2 = np.cross(axis_centers, axis1)
                # Compute the intersection circumference radius
                theta = np.arccos((radius[j]**2 + dist**2 - radius[i]**2) /
                                  (2 * radius[j] * dist))
                r = radius[j]*np.sin(theta)
                # Compute the intersection circumference center
                xc = anchors_pos[j, 0] + radius[j] * np.cos(theta)*axis_centers[0]
                yc = anchors_pos[j, 1] + radius[j] * np.cos(theta)*axis_centers[1]
                zc = anchors_pos[j, 2] + radius[j] * np.cos(theta)*axis_centers[2]
                # Plot the cirunference
                u = np.linspace(0, 2 * np.pi, NUM_POINTS)
                x = xc + r * np.cos(u) * axis1[0] + r * np.sin(u) * axis2[0]
                y = yc + r * np.cos(u) * axis1[1] + r * np.sin(u) * axis2[1]
                z = zc + r * np.cos(u) * axis1[2] + r * np.sin(u) * axis2[2]
                ax.plot(x, y, z, linewidth=1)

    # Now compute the solution as given in the "Indoor Robot Positioning using an
    # Enhanced Trilateration Algorithm" paper
    # Beware ith this math, as it assumes the 1st anchor with x=y=z=0, the 2nd
    # anchors with y=z=0 and the third anchor with z=0. You can always translate
    # before doing the math and return back after the math.
    x = (radius[0]**2-radius[1]**2+anchors_pos[1, 0]**2)/(2*anchors_pos[1, 0])
    y = (radius[0]**2-radius[2]**2+anchors_pos[2, 0]**2+anchors_pos[2, 1]**2 - 2*anchors_pos[2, 0]*x) / (2*anchors_pos[2, 1])
    z = np.sqrt(radius[0]**2-x**2-y**2)
    tag_est_pos = np.array([x, y, z])
    # Plot the estimated position
    ax.scatter(tag_est_pos[0], tag_est_pos[1], tag_est_pos[2], color='black', s=25, marker='+')

    # Plot the real positions using an 'x'
    ax.scatter(tag_pos[0], tag_pos[1], tag_pos[2], color='black', s=25, marker='x')

    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Store values to be restored later
    azim = ax.azim
    elev = ax.elev
    # Store X-Y, X-Z and Y-Z views of the plot
    # X-Y
    ax.view_init(90, -90)
    ax.set_title('X-Y view')
    set_axes_equal(ax)
    plt.savefig('2D_X-Y_view.png')
    # X - Z
    ax.view_init(0, -90)
    ax.set_title('X-Z view')
    set_axes_equal(ax)
    plt.savefig('2D_X-Z_.png')
    # Y-Z
    ax.view_init(0, 0)
    ax.set_title('Y-Z view')
    set_axes_equal(ax)
    plt.savefig('2D_Y-Z_view.png')
    # Restore view
    ax.view_init(elev, azim)
    ax.set_title('3D view')
    set_axes_equal(ax)
    plt.savefig('3D_view.png')

    # Print information
    print(f'Anchors position: {anchors_pos}!')
    print(f'Real tag position: {tag_pos}')
    print(f'Estimated tah position: {tag_est_pos}')
    print(f'Range error used: {range_error}')

    # Show the resulting plot
    set_axes_equal(ax)
    plt.show()

    print('Done...')
