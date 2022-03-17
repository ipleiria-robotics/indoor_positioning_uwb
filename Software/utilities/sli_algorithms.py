"""
File containing the algorithms to estimate positions
https://www.mathworks.com/matlabcentral/fileexchange/65016-iterative-weighted-least-squares
"""
import numpy as np
import math as mth


# Least square method
def least_square(distances, acoord):
    try:
        num_acoord = len(distances)
        A = np.zeros((num_acoord - 1, 3))
        b = np.zeros((num_acoord - 1, 1))
        for i in range(1, num_acoord):
            A[i - 1, 0] = acoord[0, 0] - acoord[i, 0]
            A[i - 1, 1] = acoord[0, 1] - acoord[i, 1]
            A[i - 1, 2] = acoord[0, 2] - acoord[i, 2]
            b[i - 1] = acoord[0, 0] ** 2 + acoord[0, 1] ** 2 + acoord[0, 2] ** 2 - \
                acoord[i, 0] ** 2 - acoord[i, 1] ** 2 - acoord[i, 2] ** 2 + \
                distances[i] ** 2 - distances[0] ** 2

        b = np.true_divide(b, 2)
        r = np.linalg.lstsq(A, b, rcond=1)[0]
        return np.array([r[0][0], r[1][0], r[2][0]])
    except:
        return "NaN"


# Iterative Least Square method
def iterative_least_square(distances, acoord, ref_position):
    try:
        # iterative method to solve resolve a position
        iterations = 100
        tol = 1e-8
        # xPos = [0, 0, 0]
        xPos = [ref_position[0], ref_position[1], ref_position[2]]
        dxPos = 0
        posIter = np.zeros([len(acoord), 3])
        posIter[:, 0] = xPos[0]
        posIter[:, 1] = xPos[1]
        posIter[:, 2] = xPos[2]
        # posIter = xPos
        iter = 0

        for ite in range(0, iterations):
            diff = acoord - posIter
            rTag = np.transpose(np.sqrt(np.sum(diff ** 2, axis=1)))
            matrix_aux = np.zeros([len(acoord), 3])
            for i, val in enumerate(rTag):
                matrix_aux[i, :] = val

            G = [-diff / matrix_aux][0]
            # diffRange = distances - rTag
            diffRange = distances - rTag
            dxPos = np.linalg.lstsq(G, diffRange, rcond=1)[0]
            xPos = xPos + dxPos

            # print(diffRange)

            if abs(dxPos[0]) < tol and abs(dxPos[1]) < tol and abs(dxPos[2]) < tol:
                break

            for i, val in enumerate(acoord):
                posIter[i, :] = xPos

            iter = iter + 1
        # print(f"iterations: {iter}")
        # print(f"Position estimate: {xPos}")
        return xPos

    except:
        return None


# Form the the rotation matrix used on Fang's method
def rotation_matrix(axis, angle):
    # rotation in X
    if axis[0] == 1:
        return np.array([[1, 0, 0],
                         [0, mth.cos(angle), - mth.sin(angle)],
                         [0, mth.sin(angle), mth.cos(angle)]
                         ])
    # rotation in Y
    if axis[1] == 1:
        return np.array([[mth.cos(angle), 0, mth.sin(angle)],
                         [0, 1, 0],
                         [-mth.sin(angle), 0, mth.cos(angle)]
                         ])
    # rotation in Z
    if axis[2] == 1:
        return np.array([[mth.cos(angle), -mth.sin(angle), 0],
                         [mth.sin(angle), mth.cos(angle), 0],
                         [0, 0, 1]
                         ])


# Fangs method position estimate
def fangs_trilateration(ranges, anchors):
    e1 = anchors[0]
    e2 = anchors[1]
    e3 = anchors[2]
    et1 = e1 - e1
    et2 = e2 - e1
    et3 = e3 - e1

    r1 = ranges[0]
    r2 = ranges[1]
    r3 = ranges[2]

    angRy = np.arctan2(et2[2], et2[0])
    et2 = np.dot(rotation_matrix([0, 1, 0], angRy), et2)
    et3 = np.dot(rotation_matrix([0, 1, 0], angRy), et3)

    angRz = np.arctan2(et2[1], et2[0])
    et2 = np.dot(rotation_matrix([0, 0, 1], -angRz), et2)
    et3 = np.dot(rotation_matrix([0, 0, 1], -angRz), et3)

    angRx = np.arctan2(et3[2], et3[1])
    et2 = np.dot(rotation_matrix([1, 0, 0], -angRx), et2)
    et3 = np.dot(rotation_matrix([1, 0, 0], -angRx), et3)

    x = (r1 ** 2 - r2 ** 2 + et2[0] ** 2) / (2 * et2[0])
    y = (r1 ** 2 - r3 ** 2 + et3[0] ** 2 + et3[1]
         ** 2 - (2 * et3[0]) * x) / (2 * et3[1])

    if (r1 ** 2 - x ** 2 - y ** 2) > 0:
        z = mth.sqrt(r1 ** 2 - x ** 2 - y ** 2)
        sol = np.array([x, y, z])
        sol = np.dot(rotation_matrix([1, 0, 0], angRx), sol)
        sol = np.dot(rotation_matrix([0, 0, 1], angRz), sol)
        sol = np.dot(rotation_matrix([0, 1, 0], -angRy), sol)
        sol = sol + e1
        # position = np.array([sol[0], sol[1], sol[2]])
        position = sol
    else:
        # position = np.array(['NaN', 'NaN', 'NaN'])
        t = np.zeros(3)
        t[0] = x
        t[1] = y
        t[2] = None
        position = np.array(t)

    return position
    # return position, combinatations


# weight least square
def iterative_weighted_least_square(ranges, anchors_coords, weights_array, iter, tol):
    pos = [0, 0, 0]
    iterations = iter
    residual_tolerance = tol
    W = np.diag(weights_array)

    posIter = np.zeros([len(anchors_coords), 3])

    for ite in range(0, iterations):
        diff = anchors_coords - posIter
        rTag = np.transpose(np.sqrt(np.sum(diff ** 2, axis=1)))
        matrix_aux = np.zeros([len(anchors_coords), 3])
        for i, val in enumerate(rTag):
            matrix_aux[i, :] = val

        G = [-diff / matrix_aux][0]
        #G = np.dot(G, W)
        diffRange = ranges - rTag
        # dxPos = np.linalg.lstsq(G, diffRange, rcond=1)[0]
        # dxPos = np.linalg.lstsq(G, diffRange, rcond=1)[0]

        first_term = np.linalg.inv(np.dot(np.dot(G.T, W.T), np.dot(W, G)))
        second_term = np.dot(np.dot(G.T, W.T), np.dot(W, diffRange))

        dxPos = np.dot(first_term, second_term)

        pos = pos + dxPos

        if abs(dxPos[0]) < residual_tolerance and abs(dxPos[1]) < residual_tolerance and abs(dxPos[2]) < residual_tolerance:
            # print(f"tol value: {dxPos}")
            break

        for i, val in enumerate(anchors_coords):
            posIter[i, :] = pos

    return pos
