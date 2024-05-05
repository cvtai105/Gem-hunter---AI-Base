import CNFsSolvers as CNFsSolvers
import in_out
import sys
import runtime



def main():
    
    INPUT_DIR = 'testcases/input/'
    OUTPUT_DIR = 'testcases/output/'
    files = ['5x5.txt', '9x9.txt','11x11.txt', '15x15.txt', '20x20.txt']
    if(len(sys.argv) < 2):
        sys.argv.append("-compare")
    if(sys.argv[1] == "-compare"):
        dpll_runtime = []
        backtracking_runtime = []
        bruteforce_runtime = []
        pysat_runtime = []
        cnf_count = []
        literals_count = []
        matrix_size = []
        for filename in files:
            
            matrix = in_out.readAndPadMatrix(INPUT_DIR + filename)
            cnf = CNFsSolvers.GenerateCNFsFromMatrix(matrix)
            cnf1 = [clause[:] for clause in cnf]
            cnf2 = [clause[:] for clause in cnf]
            cnf3 = [clause[:] for clause in cnf]
            cnf4 = [clause[:] for clause in cnf]
            print()
            print('Matrix size:', len(matrix) -2, 'x', len(matrix[0]) -2)
            print('CNF count:', len(cnf))
            print('Variable count:', len({abs(literal) for clause in cnf for literal in clause}))

            matrix_size.append([len(matrix) - 2, len(matrix[0]) - 2])
            literals_count.append(len({abs(literal) for clause in cnf for literal in clause}))
            cnf_count.append(len(cnf))
            # backtracking_runtime.append(runtime.getBacktrackingRuntime(cnf1))
            # bruteforce_runtime.append(runtime.getBruteforceRuntime(cnf2))
            backtracking_runtime.append(0)
            bruteforce_runtime.append(0)
            pysat_runtime.append(runtime.getPysatRuntimme(cnf3))
            dpll_runtime.append(runtime.getDpllRuntime(cnf4))

        with open('analysis.txt', 'w') as file:
            file.write("Matrix size, CNF count, Literals count, Backtracking runtime, Bruteforce runtime, Pysat runtime, DPLL runtime,\n")
            for i in range(len(files)):
                file.write(str(matrix_size[i]) + ", " + str(cnf_count[i]) + ", " + str(literals_count[i]) + ", " + str(backtracking_runtime[i]) + ", " + str(bruteforce_runtime[i]) + ", " + str(pysat_runtime[i]) + ", " + str(dpll_runtime[i]) + "\n")
            
    elif(sys.argv[1] != "-bruteforce" and sys.argv[1] != "-backtracking" and sys.argv[1] != "-pysat" and sys.argv[1] != "-dpll"):
        print("Invalid argument")
    else:
        alg = sys.argv[1]
        alg = alg[1:]
        for filename in files:
            matrix = in_out.readAndPadMatrix(INPUT_DIR + filename)
            cnf = CNFsSolvers.GenerateCNFsFromMatrix(matrix)
            solution = CNFsSolvers.GetRevealedMatrix(matrix, cnf, alg)
            in_out.unpadAndWriteMatrix(OUTPUT_DIR + filename, solution)

main()