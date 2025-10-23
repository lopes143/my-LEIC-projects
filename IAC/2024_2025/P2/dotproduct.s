.globl dotproduct
.data
# Sample input arrays
# You can change this array to test other values (remember to modify the dimensions in the main)

arr0: .word 1, 2, 3, 4
arr1: .word 10, 20, 30, 40

.text

main:	
    # Set up arguments for dotproduct(arr0, arr1, 4)
    la a0, arr0         # a0 = &arr0
    la a1, arr1         # a1 = &arr1
    li a2, 4            # a2 = number of elements

    jal ra, dotproduct  # Call dotproduct function

    # The result of the dot product is now in a0
    
exit:
    li a7, 10     # Exit syscall code
    ecall         # Terminate the program


# =======================================================
# FUNCTION: Dot product of 2 int arrays
# Arguments:
#   a0 (int*) - Pointer to the start of arr0
#   a1 (int*) - Pointer to the start of arr1
#   a2 (int)  - Number of elements to use	
# Returns:
#   a0 (int)  - The dot product of arr0 and arr1
# Exceptions:
#   - If a2 < 1, exit with error code 38
# =======================================================


# t0:sum , t1:i , t2:*arr0 , t3:*arr1 , t4:curr.value of arr0 , t5:curr.value of arr1
dotproduct:
    li t0, 1              # Used to check for error
    blt a2, t0, error
    li t0, 0              # Initialize i and sum with 0
    li t1, 0
    mv t2, a0             #Copy of array pointers
    mv t3, a1
    
loop:
      
    bge t1, a2, end       # Loop condition: exit if i>=a2
    lw t4, 0(t2)          # For current index, get arrays values
    lw t5, 0(t3)
    addi t2, t2, 4        # Advance array pointers
    addi t3, t3, 4
    addi t1, t1, 1        # j +=1
    mul t6, t4, t5        # Temporary product is in t6
    add t0, t0, t6        # sum += temp. product

    j loop                # Call the lopp again
    
end:
    mv a0, t0             # Put final vlaue into a0
    jr ra                 # Exit function
    
error:
    li a0, 38
    j exit_with_error

# Exits the program with an error 
# Arguments: 
# a0 (int) is the error code 
# You need to load a0 the error to a0 before to jump here
exit_with_error:
  li a7, 93            # Exit system call
  ecall                # Terminate program

