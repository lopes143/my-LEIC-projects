# ===========================================================
# Identificacao do grupo: T32 [T?? para Tagus ou A?? para Alameda]
#
# Membros [istID, primeiro + ultimo nome]
# 1. ist1113963, Rodrigo Lopes
# 2. ist1114134, Bernardo Lima
# 3. ist1114489, Henrique Santos
#
# ===========================================================
# Requisitos do enunciado que *nao* estao corretamente implementados:
# (indicar um por linha, ou responder "nenhum")
# - O valor final (retorno do classify) nao esta correto
# - Os valores do PGM nao foram convertidos de 8 bits para 32 bits

# ===========================================================
# Top-5 das otimizacoes que a vossa solucao incorpora:
# (maximo 140 caracteres por cada otimizacao)
#
# 1. Otimizacao no matmul para evitar percorrer a matriz inteira, saltando elementos
# ate ao seguinte na mesma coluna
#
# 2.
#
# 3.
#
# 4.
#
# 5.
#
# ===========================================================

.data

# ===========================================================
#Main data structures. These definitions cannot be changed.

m0_path: .string "../iac-project/classifier-files/weight-matrices/m0.bin"
m1_path: .string "../iac-project/classifier-files/weight-matrices/m0.bin"
pgm_path: .string "../iac-project/classifier-files/input-images/ascii-pgm/input1_bin.pgm"


h_m0: .word 128
w_m0: .word 784
m0: .zero 401408                #h_m0 * w_m0 * 4 bytes

h_m1: .word 10
w_m1: .word 128
m1: .zero 5120                  #h_m1 * w_m1 * 4 bytes

h_input: .word 784
w_input: .word 1
input: .zero 3136               #h_input * w_input * 4 bytes

h_h: .word 128
w_h: .word 1
h: .zero 512                    #h_h * w_h * 4 bytes

h_o: .word 10
w_o: .word 1
o: .zero 40                     #h_o * w_o * 4 bytes


# ===========================================================
# Here you can define any additional data structures that your program might need




# ===========================================================
.text

main:
    # Set up arguments for *classify* function
    la a0, m0_path
    lw a1, m1_path
    la a2, pgm_path
    # Call *classify* function
    jal ra, classify
    j exit
    

# ===========================================================
# FUNCTION: abs
#   Computes absolute value of the int stored at a0
# Arguments:
#   a0, a pointer to int
# Returns:
#   Nothing (modifies value in memory)
# ===========================================================

abs:
    lw t0, 0(a0)
    bgez t0, abs_exit
    sub t0, zero, t0        # t0 = -t0
    sw t0, 0(a0)

abs_exit: 
    jr ra                    # Return to the caller



# ============================================================
# FUNCTION: relu
#   Applies ReLU on each element of the array (in-place)
# Arguments:
#   a0 = pointer to int array
#   a1 = array length
# Exceptions:
#   - If the length of the array is less than 1,
#     this function terminates the program with error code 36
# ============================================================
relu:
    blez a1, relu_error
    li t0, 0

relu_loop:
    bge t0, a1, relu_exit    # Exit if end of array reached
    lw t1, 0(a0)
    bgez t1, relu_skip       # If positive, skip changing
    sw zero, 0(a0)

relu_skip:
    addi a0,a0,4             # Advance to next number
    addi t0,t0,1
    j relu_loop

relu_error:
    li a0, 36
    j exit_with_error
    
relu_exit:    
    jr ra                    # Return to the caller



# =================================================================
# FUNCTION: Given an int array, return the index of the largest
#   element. If there are multiple, return the one
#   with the smallest index.
# Arguments:
#   a0 (int*) is the pointer to the start of the array
#   a1 (int)  is the number of elements in the array
# Returns:
#   a0 (int)  is the first index of the largest element
# Exceptions:
#   - If the length of the array is less than 1,
#     this function terminates the program with error code 37
# =================================================================

#t0: array index, t1: array element, t2: biggest number, t3: biggest number index
argmax:
    blez a1, argmax_error
    li t0, 0
    lw t2, 0(a0)            # Load first number

argmax_loop:
    bge t0, a1, argmax_exit # Exit if end reached
    lw t1, 0(a0)            # Load num to analyze
    ble t1, t2, argmax_skip # If num is not bigger, skip
    mv t2, t1               # Change biggest num till now with current one 
    mv t3, t0               # Change biggest num's index till now with current one

argmax_skip:
    addi a0, a0, 4          # Advance to next num
    addi t0, t0, 1
    j argmax_loop

argmax_error:
    li a0, 37
    j exit_with_error
    
argmax_exit:
    mv a0, t3               # Return value          
    jr ra                    # Return to the caller



# =======================================================
# FUNCTION: Dot product of 2 int arrays
# Arguments:
#   a0 (int*) - Pointer to the start of the line of arr0
#   a1 (int*) - Pointer to the start of the column of arr1
#   a2 (int)  - Number of elements to use
#   a3 (int)  - Number of columns of arr1 (steps)
# Returns:
#   a0 (int)  - The dot product of arr0 and arr1
# Exceptions:
#   - If a2 < 1, exit with error code 38
# =======================================================

# t0: sum, t1: i, t2: curr.value of arr0, t3: curr.value of arr1, t4: 
dotproduct:
    li t0, 1                # exif if a2 < 1 (number in t0)
    blt a2, t0, dp_error
    li t0, 0                # Initialize i and sum with 0
    li t1, 0
    slli t4, a3, 2          # Compute how many bytes to jump in column (4 * step)
    
dp_loop: 
    bge t1, a2, dp_exit     # Loop condition: exit if i>=a2
    lw t2, 0(a0)            # For current index, get arrays values
    lw t3, 0(a1)
    addi a0, a0, 4          # Advance to next number in line
    add a1, a1, t4          # Advance to next number in column
    addi t1, t1, 1          # j +=1
    mul t6, t2, t3          # Temporary product is in t6
    add t0, t0, t6          # sum += temp. product
    j dp_loop                  # Call the loop again
    
dp_error:
    li a0, 38
    j exit_with_error

dp_exit:
    mv a0, t0               # Return value
    jr ra                    # Return to the caller


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
#    this function terminates the program with error core 39
#  - If the number of columns in matrix A is not equal to the number 
#    of rows in matrix B, it terminates with error code 40
# =======================================================
matmul:
    li t0, 1                #Check for error 39
    blt a2, t0, matmul_error_1
    blt a3, t0, matmul_error_1
    blt a4, t0, matmul_error_1
    blt a5, t0, matmul_error_1
    bne a3, a4, matmul_error_2
    addi sp, sp, -12        # Save ra,a0,a1 in stack
    sw ra, 8(sp)
    sw a0, 4(sp)
    sw a1, 0(sp)
    li t0, 0                # Initialize line counter (0<=t0<a2)
    li t1, 0                # Initialize column counter (0<=t1<=a5)
    li t2, 0                # Elements written to final matrix (0<=t2<=a2*a5)
    mul t3, a2, a5          # Max number of elements final matrix have (0<=t2<=t3)

line_column_nums:
    bge t2, t3, matmul_exit # If final matrix is full, exit program
    bge t1, a5, next_line   # If last column reached, go to next line
    jal ra, call_dotproduct
    addi t1, t1, 1
    j line_column_nums

next_line:
    li t1, 0
    addi t0, t0, 1
    bge t0, a2, matmul_exit # If last line reached, exit program
    j line_column_nums

call_dotproduct:
    addi sp, sp, -28         
    sw ra, 24(sp)           # Save ra in the stack
    mul t6, t0, a3          # a0 = a0 + 4*(t0 * a3)
    slli t6, t6, 2
    add a0, a0, t6
    slli t6, t1, 2          # a1 = a1 + 4*(t1)
    add a1, a1, t6
    sw a2, 20(sp)           # Save a2,a3,t0,t1,t2,t3 in the stack
    sw a3, 16(sp)
    sw t0, 12(sp)
    sw t1, 8(sp)
    sw t2, 4(sp)
    sw t3, 0(sp)
    mv a2, a3               # Elements to use: nº of line elements on matrixA
    mv a3, a5               # Number of columns of matrixB 
    jal ra, dotproduct      # Final value is in a0
    sw a0, 0(a6)
    addi a6, a6, 4          # Advance pointer
    lw t3, 0(sp)            # Restore stack values
    lw t2, 4(sp)
    lw t1, 8(sp)
    lw t0, 12(sp)
    lw a3, 16(sp)
    lw a2, 20(sp)
    lw ra, 24(sp)
    lw a1, 28(sp)
    lw a0, 32(sp)
    addi sp, sp, 28
    addi t2, t2, 1
    jr ra                   # Go back to line_column_nums

matmul_error_1:
    li a0, 39
    j exit_with_error

matmul_error_2:
    li a0, 40
    j exit_with_error

matmul_exit:
    lw ra, 8(sp)             # Restore ra from outside of matmul
    addi sp, sp, 12          # Close stack
    jr ra                    # Return to the caller


######################################################################
# Function: read_file(char* filename, byte* buffer, int length)
# Input:
#   a0: pointer to null-terminated filename string
#   a1: destination buffer
#   a2: number of bytes to read
# Output:
#   a0: number of bytes read (return value from syscall)
# Exceptions:
#   - Error code 41 if error in the file descriptor
#   - Error code 42 If the length of the bytes to read is less than 1
######################################################################

read_file:
    addi sp, sp, -8                   # Save a0 & a1 in the stack
    sw a0, 4(sp)
    sw a1, 0(sp)
    li t0, 1
    blt a2, t1, read_file_error_2     # Check if input is right

    #open
    li a1, 0                          # Set to 0 to avoid flags
    li a7, 1024
    ecall                             # File descriptor is in a0
    li t1, -1                         # Check for file descriptor error
    beq a0, t1, read_file_error_1
    addi sp, sp, -4
    sw a0, 0(sp)                      # Save descriptor for later

    #read
    lw a1, 4(sp)
    #descriptor is already on a0
    #bytes to read is already on a2
    li a7, 63
    ecall                             # Bytes read is on a0
    addi sp, sp, -4
    sw a0, 0(sp)                      # Store bytes read for later
    beq a0, t1, read_file_error_1     # Check again after reading

    #close
    lw a0, 4(sp)                      # Restore file descriptor to close
    li a7, 57
    ecall

    lw a0, 0(sp)                      # Restore bytes read at a0
    addi sp, sp, 16

    jr ra                             # Return to the caller
    
    # addi sp, sp, -4
    # sw a1,0(sp)                       # Save a0 and a1 in stack 
    # li a1,0                           # Set a0 to 0 to avoid raising flags
    # li t1, 1
    # blt a2, t1, read_file_error_2     # Check if input is right
    # li a7,1024                        # Get file descriptor
    # ecall
    # lw a1,0(sp)
    # addi sp,sp,4
    # sw a0, 4(sp)                      # Save file descriptor for later
    # li t2, -1
    # beq a0, t2, read_file_error_1     # Check for opening errors
    # li a7, 63
    # ecall
    # sw a0, 0(sp)                      # Store bytes read for later
    # beq a0, t2, read_file_error_1     # Check again after reading
    # lw a0, 4(sp)                      # Restore file descriptor to close it
    # li a7, 57
    # ecall
    # lw a0, 0(sp)                      # Restore bytes read to a0
    # addi sp, sp, 8
    # jr ra                    # Return to the caller

read_file_error_1:
    li a0, 41
    j exit_with_error

read_file_error_2:
    li a0, 42
    j exit_with_error



# =======================================================
# FUNCTION: Classify decimal digit from input image
#   d = classify(A, B, input)
#
# Arguments:
#   a0 (string*)  - pathname of file with the weight matrix m0
#   a1 (string*)  - pathname of file with the weight matrix m1
#   a2 (string*)  - pathname of file with the input image in Raw PGM format
#
# Returns:
#   a0 (int) - value of the classified decimal digit
#
# =======================================================

classify:
    addi sp, sp, -16        # Save parent ra, a0, a1, and a2
    sw ra, 12(sp)
    sw a0, 8(sp)            # m0_path
    sw a1, 4(sp)            # m1_path
    sw a2, 0(sp)            # pgm_path


    # read file m0
    # m0_path is already on a0
    la a1, m0
    la t0, h_m0             # Load height number
    lw t0, 0(t0)
    la t1, w_m0             # Load width number
    lw t1, 0(t1)
    mul a2, t0, t1          # Bytes to read
    li t0,4
    mul a2,a2,t0
    jal ra, read_file

    # read file m1
    la a0, m1_path          # Load m1_path
    la a1, m1
    la t0, h_m1             # Load height number
    lw t0, 0(t0)
    la t1, w_m1             # Load width number
    lw t1, 0(t1)
    mul a2, t0, t1          # Bytes to read
    li t0,4
    mul a2,a2,t0
    jal ra, read_file

    # read PGM
    lw a0, 0(sp)            # Load pgm_path
    la a1, input
    la t0, h_input
    lw t0, 0(t0)
    la t1, w_input
    lw t1, 0(t1)
    mul a2, t0, t1
    li t0,4
    mul a2,a2,t0
    jal ra, read_file

    # h = matmul(m0, input)
    la a0, m0
    la a1, input
    addi a1, a1, 12         #advance 12 bytes - ignore PGM header
    la a2, h_m0
    lw a2, 0(a2)
    la a3, w_m0
    lw a3, 0(a3)
    la a4, h_input
    lw a4, 0(a4)
    la a5, w_input
    lw a5 0(a5)
    la a6, h
    jal ra, matmul          # Return is in a6 (written to h)

    # relu(h)
    la a0, h
    la t0, h_h              
    lw t0, 0(t0)
    la t1, w_h
    lw t1, 0(t1)
    mul a1, t0, t1          # Get array length
    jal ra, relu

    # o = matmul(m1, h)
    la a0, m1
    la a1, h
    la a2, h_m1
    lw a2, 0(a2)
    la a3, w_m1
    lw a3, 0(a3)
    la a4, h_h
    lw a4, 0(a4)
    la a5, w_h
    lw a5 0(a5)
    la a6, o
    jal ra, matmul          # Return is in a6 (written to o)

    # argmax(o)
    la a0, o
    la t0, h_o
    lw t0, 0(t0)
    la t1, w_o
    lw t1, 0(t1)
    mul a1, t0, t1
    jal ra, argmax          # It returns the index on a0

    #get index's value
    # val = *(o + index * 4)
    la t0, o
    slli t1, a0, 2          # index * 4
    add t0, t0, t1
    lw a0, 0(t0)            # Number answer is in a0
    lw ra, 12(sp)           # Restore parent ra
    addi sp, sp, 16

classify_exit:
    jr ra                    # Return to the caller




# =======================================================
# Exit procedures
# =======================================================

# Exits the program (with code 0)
exit:
    li a7, 10     # Exit syscall code
    ecall         # Terminate the program

# Exits the program with an error 
# Arguments: 
# a0 (int) is the error code 
# You need to load a0 the error to a0 before to jump here
exit_with_error:
  li a7, 93            # Exit system call
  ecall                # Terminate program

