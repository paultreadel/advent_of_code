filename = "sample.txt"
# filename = "data.txt"


DEBUG = True


if __name__ == "__main__":
    total_part1 = 0
    total_part2 = 0

    with open(filename, "r") as f:
        lines = f.read()

    print(f"Part 1: {total_part1}")
    print(f"Part 2: {total_part2}")

    # Source - https://stackoverflow.com/a
    # Posted by sascha, modified by community. See post 'Timeline' for change history
    # Retrieved 2025-12-11, License - CC BY-SA 3.0

    import copy
    import subprocess

    import matplotlib.pyplot as plt  # plotting-only
    import numpy as np
    import seaborn as sns  # plotting-only

    np.set_printoptions(linewidth=120)  # more nice console-output

    """ Constants / Input
            Example: 5 tetrominoes; no rotation """
    M, N = 38, 39
    polyominos = [
        np.array(
            [
                [1, 1, 1],
                [1, 1, 0],
                [1, 1, 0],
            ]
        ),
        np.array(
            [
                [1, 1, 1],
                [1, 1, 0],
                [0, 1, 1],
            ]
        ),
        np.array(
            [
                [0, 1, 1],
                [1, 1, 1],
                [1, 1, 0],
            ]
        ),
        np.array(
            [
                [1, 1, 0],
                [1, 1, 1],
                [1, 1, 0],
            ]
        ),
        np.array(
            [
                [1, 1, 1],
                [1, 0, 0],
                [1, 1, 1],
            ]
        ),
        np.array(
            [
                [1, 1, 1],
                [0, 1, 0],
                [1, 1, 1],
            ]
        ),
    ]
    polyominos = [
        np.array(
            [
                [1, 1, 1],
                [1, 1, 0],
                [0, 1, 1],
            ]
        ),
        np.array(
            [
                [0, 1, 1],
                [1, 1, 0],
                [1, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 0, 1],
                [1, 1, 1],
                [1, 1, 1],
            ]
        ),
        np.array(
            [
                [1, 0, 1],
                [1, 1, 1],
                [1, 0, 1],
            ]
        ),
        np.array(
            [
                [1, 1, 1],
                [0, 1, 1],
                [0, 0, 1],
            ]
        ),
        np.array(
            [
                [1, 1, 1],
                [1, 0, 1],
                [1, 0, 1],
            ]
        ),
    ]

    """ Preprocessing
            Calculate:
            A: possible placements
            B: covered positions
            C: collisions between placements
    """

    def unique_rotations(poly):
        """Return a list of unique rotations (0, 90, 180, 270 degrees) for a polyomino."""
        rots = []
        for k in range(4):
            rot = np.rot90(poly, k)
            if not any(np.array_equal(rot, r) for r in rots):
                rots.append(rot)
        return rots

    placements = []
    covered = []
    for p_ind, p in enumerate(polyominos):
        rots = unique_rotations(p)
        for rot_ind, p_rot in enumerate(rots):
            mP, nP = p_rot.shape
            for x in range(M):
                for y in range(N):
                    if x + mP <= M and y + nP <= N:
                        placements.append((p_ind, rot_ind, x, y))
                        cover = np.zeros((M, N), dtype=bool)
                        cover[x : x + mP, y : y + nP] = p_rot
                        covered.append(cover)
    covered = np.array(covered)

    collisions = []
    for m in range(M):
        for n in range(N):
            collision_set = np.flatnonzero(covered[:, m, n])
            collisions.append(collision_set)

    """ Helper-function: Cardinality constraints """
    # K-ARY CONSTRAINT GENERATION
    # ###########################
    # SINZ, Carsten. Towards an optimal CNF encoding of boolean cardinality constraints.
    # CP, 2005, 3709. Jg., S. 827-831.

    def next_var_index(start):
        next_var = start
        while True:
            yield next_var
            next_var += 1

    class s_index:
        def __init__(self, start_index):
            self.firstEnvVar = start_index

        def next(self, i, j, k):
            return self.firstEnvVar + i * k + j

    def gen_seq_circuit(k, input_indices, next_var_index_gen):
        cnf_string = ""
        s_index_gen = s_index(next(next_var_index_gen))

        # write clauses of first partial sum (i.e. i=0)
        cnf_string += (
            str(-input_indices[0]) + " " + str(s_index_gen.next(0, 0, k)) + " 0\n"
        )
        for i in range(1, k):
            cnf_string += str(-s_index_gen.next(0, i, k)) + " 0\n"

        # write clauses for general case (i.e. 0 < i < n-1)
        for i in range(1, len(input_indices) - 1):
            cnf_string += (
                str(-input_indices[i]) + " " + str(s_index_gen.next(i, 0, k)) + " 0\n"
            )
            cnf_string += (
                str(-s_index_gen.next(i - 1, 0, k))
                + " "
                + str(s_index_gen.next(i, 0, k))
                + " 0\n"
            )
            for u in range(1, k):
                cnf_string += (
                    str(-input_indices[i])
                    + " "
                    + str(-s_index_gen.next(i - 1, u - 1, k))
                    + " "
                    + str(s_index_gen.next(i, u, k))
                    + " 0\n"
                )
                cnf_string += (
                    str(-s_index_gen.next(i - 1, u, k))
                    + " "
                    + str(s_index_gen.next(i, u, k))
                    + " 0\n"
                )
            cnf_string += (
                str(-input_indices[i])
                + " "
                + str(-s_index_gen.next(i - 1, k - 1, k))
                + " 0\n"
            )

        # last clause for last variable
        cnf_string += (
            str(-input_indices[-1])
            + " "
            + str(-s_index_gen.next(len(input_indices) - 2, k - 1, k))
            + " 0\n"
        )

        return (
            cnf_string,
            (len(input_indices) - 1) * k,
            2 * len(input_indices) * k + len(input_indices) - 3 * k - 1,
        )

    def gen_at_most_n_constraints(vars, start_var, n):
        constraint_string = ""
        used_clauses = 0
        used_vars = 0
        index_gen = next_var_index(start_var)
        circuit = gen_seq_circuit(n, vars, index_gen)
        constraint_string += circuit[0]
        used_clauses += circuit[2]
        used_vars += circuit[1]
        start_var += circuit[1]

        return [constraint_string, used_clauses, used_vars, start_var]

    def parse_solution(output):
        # assumes there is one
        vars = []
        for line in output.decode().split("\n"):
            if line:
                if line[0] == "v":
                    line_vars = list(map(lambda x: int(x), line.split()[1:]))
                    vars.extend(line_vars)
        return vars

    def solve(CNF):
        p = subprocess.Popen(
            ["cryptominisat5.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        result = p.communicate(input=CNF.encode())[0]
        sat_line = result.decode().find("s SATISFIABLE")
        if sat_line != -1:
            # solution found!
            vars = parse_solution(result)
            return True, vars
        else:
            return False, None

    """ SAT-CNF: BASE """
    X = np.arange(1, len(placements) + 1)  # decision-vars
    # 1-index for CNF
    Y = np.arange(len(placements) + 1, len(placements) + 1 + M * N).reshape(M, N)
    next_var = len(placements) + 1 + M * N  # aux-var gen
    n_clauses = 0

    cnf = ""  # slow string appends
    # # int-based would be better
    # <= 1 for each collision-set
    for cset in collisions:
        constraint_string, used_clauses, used_vars, next_var = (
            gen_at_most_n_constraints(X[cset].tolist(), next_var, 1)
        )
        n_clauses += used_clauses
        cnf += constraint_string

    # Specify required count for each polyomino index (by default 0 means not used, set to desired count)
    required_polyomino_counts = {
        0: 1,  # Example: 0 of polyomino 0
        1: 0,  # Example: 0 of polyomino 1
        2: 1,  # Example: 0 of polyomino 2
        3: 0,  # Example: 0 of polyomino 3
        4: 2,  # Example: 2 of polyomino 4 (as before)
        5: 2,  # Example: 0 of polyomino 5
    }
    required_polyomino_counts = {
        0: 42,  # Example: 0 of polyomino 0
        1: 38,  # Example: 0 of polyomino 1
        2: 49,  # Example: 0 of polyomino 2
        3: 36,  # Example: 0 of polyomino 3
        4: 29,  # Example: 2 of polyomino 4 (as before)
        5: 33,  # Example: 0 of polyomino 5
    }
    # You can edit required_polyomino_counts as needed

    for poly_idx, count in required_polyomino_counts.items():
        if count > 0:
            placement_indices = [
                i
                for i, (p_ind, rot, x, y) in enumerate(placements)
                if p_ind == poly_idx
            ]
            poly_vars = X[placement_indices].tolist()
            if len(poly_vars) < count:
                raise ValueError(
                    f"Not enough placements for polyomino index {poly_idx} (any rotation) to fit {count} times."
                )
            # At least count
            constraint_string, used_clauses, used_vars, next_var = (
                gen_at_most_n_constraints(
                    [-v for v in poly_vars], next_var, len(poly_vars) - count
                )
            )
            n_clauses += used_clauses
            cnf += constraint_string
            # At most count
            constraint_string, used_clauses, used_vars, next_var = (
                gen_at_most_n_constraints(poly_vars, next_var, count)
            )
            n_clauses += used_clauses
            cnf += constraint_string

    print("BASE CNF size")
    print("clauses: ", n_clauses)
    print("vars: ", next_var - 1)

    """ SOLVE in loop -> decrease number of placed-fields until SAT """
    print("CORE LOOP")
    N_FIELD_HIT = M * N
    while True:
        print(" N_FIELDS >= ", N_FIELD_HIT)
        # sum(y) >= N_FIELD_HIT
        # == sum(not y) <= M*N - N_FIELD_HIT
        cnf_final = copy.copy(cnf)
        n_clauses_final = n_clauses

        if N_FIELD_HIT == M * N:  # awkward special case
            constraint_string = "".join([str(y) + " 0\n" for y in Y.ravel()])
            n_clauses_final += N_FIELD_HIT
        else:
            constraint_string, used_clauses, used_vars, next_var = (
                gen_at_most_n_constraints(
                    (-Y).ravel().tolist(), next_var, M * N - N_FIELD_HIT
                )
            )
            n_clauses_final += used_clauses

        n_vars_final = next_var - 1
        cnf_final += constraint_string
        cnf_final = (
            "p cnf " + str(n_vars_final) + " " + str(n_clauses) + " \n" + cnf_final
        )  # header

        status, sol = solve(cnf_final)
        if status:
            print(" SOL found: ", N_FIELD_HIT)

            """ Print sol """
            res = np.zeros((M, N), dtype=int)
            counter = 1
            for v in sol[: X.shape[0]]:
                if v > 0:
                    p, rot, x, y = placements[v - 1]
                    p_rot = unique_rotations(polyominos[p])[rot]
                    pM, pN = p_rot.shape
                    poly_nnz = np.where(p_rot != 0)
                    x_inds, y_inds = x + poly_nnz[0], y + poly_nnz[1]
                    res[x_inds, y_inds] = p + 1
                    counter += 1
            print(res)

            """ Plot """
            # very very ugly code; too lazy
            ax1 = plt.subplot2grid((6, 12), (0, 0), colspan=11, rowspan=6)
            ax_p0 = plt.subplot2grid((6, 12), (0, 11))
            ax_p1 = plt.subplot2grid((6, 12), (1, 11))
            ax_p2 = plt.subplot2grid((6, 12), (2, 11))
            ax_p3 = plt.subplot2grid((6, 12), (3, 11))
            ax_p4 = plt.subplot2grid((6, 12), (4, 11))
            ax_p5 = plt.subplot2grid((6, 12), (5, 11))
            ax_p0.imshow(polyominos[0] * 1, vmin=0, vmax=6)
            ax_p1.imshow(polyominos[1] * 2, vmin=0, vmax=6)
            ax_p2.imshow(polyominos[2] * 3, vmin=0, vmax=6)
            ax_p3.imshow(polyominos[3] * 4, vmin=0, vmax=6)
            ax_p4.imshow(polyominos[4] * 5, vmin=0, vmax=6)
            ax_p5.imshow(polyominos[5] * 5, vmin=0, vmax=6)
            ax_p0.xaxis.set_major_formatter(plt.NullFormatter())
            ax_p1.xaxis.set_major_formatter(plt.NullFormatter())
            ax_p2.xaxis.set_major_formatter(plt.NullFormatter())
            ax_p3.xaxis.set_major_formatter(plt.NullFormatter())
            ax_p4.xaxis.set_major_formatter(plt.NullFormatter())
            ax_p5.xaxis.set_major_formatter(plt.NullFormatter())
            ax_p0.yaxis.set_major_formatter(plt.NullFormatter())
            ax_p1.yaxis.set_major_formatter(plt.NullFormatter())
            ax_p2.yaxis.set_major_formatter(plt.NullFormatter())
            ax_p3.yaxis.set_major_formatter(plt.NullFormatter())
            ax_p4.yaxis.set_major_formatter(plt.NullFormatter())
            ax_p5.yaxis.set_major_formatter(plt.NullFormatter())

            mask = res == 0
            sns.heatmap(
                res,
                cmap="viridis",
                mask=mask,
                cbar=False,
                square=True,
                linewidths=0.1,
                ax=ax1,
            )
            plt.tight_layout()
            plt.show()
            break
        break
        N_FIELD_HIT -= 1  # binary-search could be viable in some cases
        # but beware the empirical asymmetry in SAT-solvers:
        #    finding solution vs. proving there is none!
