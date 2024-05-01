import CNFsSolvers as CNFsSolvers
import in_out
import os
import sys



def main():
    if(sys.argv[1] == "-compare"):
        in_out.logComparision()
    else:
        alg = sys.argv[1]
        INPUT_DIR = 'testcases/input/'
        OUTPUT_DIR = 'testcases/output/'
        inputs = os.listdir(INPUT_DIR)
        for filename in inputs:
            matrix = in_out.readAndPadMatrix(INPUT_DIR + filename)
            cnf = CNFsSolvers.GenerateCNFsFromMatrix(matrix)
            solution = CNFsSolvers.GetRevealedMatrix(matrix, cnf, alg)
            in_out.unpadAndWriteMatrix(OUTPUT_DIR + filename.replace('input', 'output'), solution)

main()