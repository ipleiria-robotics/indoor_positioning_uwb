'''
    gdop calculation using the position and the set of anchors
'''
import numpy as np
import math


def gdop_calculatio(position, coordinates):
    try:
        if len(coordinates) > 0 and len(coordinates) > 3:
            a_matrix = []
            x = position[0]
            y = position[1]
            z = position[2]

            for row in coordinates:
                r_matrix = math.sqrt((row[0] - x) ** 2 + (row[1] - y) ** 2 + (row[2] - z) ** 2)

                t_matrix = np.array([(np.array(row[0] - x) / r_matrix),
                                     (np.array(row[1] - y) / r_matrix),
                                     (np.array(row[2] - z) / r_matrix),
                                     1])
                a_matrix.append(t_matrix)

            # Test = np.cov(A)
            q_matrix = np.linalg.inv(np.matmul(np.transpose(a_matrix), a_matrix))
            # inv(A.' * A) * A.' * b
            # print(Q)

            vdop = round(math.sqrt(q_matrix[2, 2]), 2)
            hdop = round(math.sqrt(q_matrix[0, 0] + q_matrix[1, 1]), 2)
            pdop = round(math.sqrt(q_matrix[0, 0] + q_matrix[1, 1] + q_matrix[2, 2]), 2)
            # tdop = round(mth.sqrt(Q[3, 3]), 2)
            # gdop = round(mth.sqrt(pow(PDOP, 2) + pow(TDOP, 2)), 2)
        else:
            hdop, vdop, pdop = "nan"

        return hdop, vdop, pdop

    except:
        return "nan", "nan", "nan"

