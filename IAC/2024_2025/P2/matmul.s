.data

# You can change this array to test other values (remember to modify the dimentions in the main)
m0: .word 1, 2, 3, 4, 5, 6        # Matrix A (2x3) in row-major order
m1: .word 7, 8, 9, 10, 11, 12     # Matrix B (3x2) in row-major order
d:  .word 0, 0, 0, 0              # Output matrix C (2x2), initialized to 0
v0: .word 0,0,0
v1: .word 0,0,0
.text
main:
  # Load pointers to matrices
  la a0, m0                     # a0 = address of matrix A
  la a1, m1                     # a1 = address of matrix B
  la a6, d                      # a6 = address of output matrix C

  # Load matrix dimensions
  li a2, 2                      # a2 = rows of A = 2
  li a3, 3                      # a3 = cols of A = 3
  li a4, 3                      # a4 = rows of B = 3
  li a5, 2                      # a5 = cols of B = 2
  #load adress of vectors
  la t6,v0
  la t5,v1
  # Load input type 
  jal ra, matmul                # Call matrix multiplication function

  # The contents of matrix d now have the result of matmul(m0,m1)

exit:
  li a7, 10              # Exit syscall code
  ecall                  # Terminate the program

# =======================================================
# FUNCTION: Matrix Multiplication of 2 integer matrices
#   d = matmul(m0, m1)
#
# Arguments:
#   a0 (int*)  - pointer to the start of m0     (Matrix A)
#   a1 (int*)  - pointer to the start of m1     (Matrix B)
#   a2 (int)   - number of rows in m0 (A)             [rows_A]
#   a3 (int)   - number of columns in m0 (A)          [cols_A]
#   a4 (int)   - number of rows in m1 (B)             [rows_B]
#   a5 (int)   - number of columns in m1 (B)          [cols_B]
#   a6 (int*)  - pointer to the start of d            (Matrix C = A x B)
#
# Returns:
#   None (void); result is stored in memory pointed to by a6 (d)
#
# Exceptions:
#  - If the height or width of any of the matrices is less than 1, 
#    this function terminates the program with error core 38
#  - If the number of columns in matrix A is not equal to the number 
#    of rows in matrix B, it terminates with error code 38
# =======================================================

#t0 will be used as a counter that is saved on the stack
matmul:
    addi sp,sp,-4 #save ra, a2, a3 in the stack
    sw ra,0(sp)
    addi sp,sp,-4
    sw a2,0(sp)
    addi sp,sp,-4
    sw a3,0(sp)
    add a2,a3,x0 #make a2 the size of the vectors
    slli a3,a5,2 #multiply by 4, to get byte size of each jump
    li t0,0      #save counter on stack
    addi sp,sp,-4
    sw t0,0(sp)
samerow:
    #call dotproduct 
    li t0,4
    mul t0,a3,t0 #get number of bytes per row
    sub a0,a0,t0
    j between
difrow:
    sub t0,t0,a5
    addi sp,sp,-4
    sw t0,0(sp)
    #calldotproduct
between:
    lw t0,0(sp)
    addi sp,sp,4
    beq a5,t0,difrow
end:
    ret






invalid_mul:
    li a0,38                        
    j exit_with_error


# Exits the program with an error 
# Arguments: 
# a0 (int) is the error code 
# You need to load a0 the error to a0 before to jump here
exit_with_error:
  li a7, 93            # Exit system call
  ecall                # Terminate program

