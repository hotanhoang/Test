

'''
    solution 1 : using temporary matrix
'''
def rotate_using_temporary_matrix(matrix):
    #create temporary matrix to save result
    rotated = [[] for _ in range(len(matrix[0]))]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            rotated[len(matrix) - j - 1].append(matrix[i][j])
    return rotated


'''
    solution 2: without using temporary matrix
'''
def rotate_wihout_using_temporary_matrix(matrix):
    #chuyển vị ma trận
    for i in range(len(matrix)):
        for j in range(i,len(matrix)):
            tmp = matrix[i][j]
            matrix[i][j] = matrix[j][i]
            matrix[j][i] = tmp
    #đảo ngược các phần tử theo cột
    for i in range(len(matrix)):
        j = 0
        k = len(matrix) - 1
        while j < k:
            tmp = matrix[j][i]
            matrix[j][i] = matrix[k][i]
            matrix[k][i] = tmp
            j += 1
            k -= 1
    return matrix
if __name__ == '__main__':
    image = [
        [1, 2, 3, 5, 6],
        [9, 2, 7, 5, 0],
        [6, 5, 3, 2, 10],
        [5, 2, 8, 7, 4],
        [3, 1, 3, 4, 1]
    ]
    print(rotate_using_temporary_matrix(image))
    print(rotate_wihout_using_temporary_matrix(image))
