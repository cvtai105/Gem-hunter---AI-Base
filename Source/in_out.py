def readAndPadMatrix(filepath):
    
    with open(filepath, "r") as file:
        input_matrix = []
        for line in file:
            row = line.strip().split(", ")
            row = [int(cell) if cell != "_" else None for cell in row]
            input_matrix.append(row)
    padded_input_matrix = padMatrix(input_matrix)
    return padded_input_matrix

def padMatrix(matrix):
    padded_matrix = [["x"] * (len(matrix[0]) + 2)]
    for row in matrix:
        padded_row = ["x"] + row + ["x"]
        padded_matrix.append(padded_row)
    padded_matrix.append(["x"] * (len(matrix[0]) + 2))
    return padded_matrix

def unpadAndWriteMatrix(filepath, matrix):
    with open(filepath, "w") as file:
        for row in matrix[1:-1]:
            row = [str(cell) for cell in row[1:-1]]
            file.write(", ".join(row) + "\n")

def logComparision():
    return