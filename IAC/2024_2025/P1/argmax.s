.data
# You can change this array to test other values
array: .word 5, 4, 3, 9, 2   # Initial array values

.text

main:
    la a0, array           # Load address of the array
    li a1, 5               # Number of elements in the array

    jal ra, argmax         # Call the argmax function

    # Result: the index of the largest element is now in a0

exit:
    li a7, 10              # Exit syscall code
    ecall                  # Terminate the program


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
#     this function terminates the program with error code 36
# =================================================================

# t0: index of current number to analyze
# t1: current number to analyze
# t2: biggest number (starts with 1st number)
# t3: biggest index

argmax:
    blez a1,exit_with_error
    li t0,0 #t0 is the curent array value's index
    lw t2,0(a0) #load first number of the array
loop:
    bge t0,a1,loop_end  #loop condition - exit if end reached
    lw t1,0(a0)  #load num to analyze
    ble t1,t2,skip  #if number is not bigger, skip to next one
    add t2,t1,zero  #change biggest number till now with current one
    add t3,t0,zero  #change biggest number's index till now with current one
skip:
    addi a0,a0,4  #step forward 4 bytes (next number)
    addi t0,t0,1
    j loop
    
loop_end:
    add a0,t3,zero
    jr ra                        # Return to the caller

load_error:
    addi a0,zero,36

# Exits the program with an error 
# Arguments: 
# a0 (int) is the error code 
# You need to load a0 the error to a0 before to jump here
exit_with_error:
    li a7, 93                    # Exit system call
    ecall                        # Terminate program
