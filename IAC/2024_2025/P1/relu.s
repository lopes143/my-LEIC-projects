.data
# You can change this array to test other values
array: .word -3, 2, -1, 7, -2   # Initial array values				 

.text
main:
  la a0, array      # a0 = pointer to array
  li a1, 5          # a1 = number of elements in the array

  jal ra, relu      # Call relu function

  # Result: the array now has its negative values replaced by zero

exit:
  li a7, 10              # Exit syscall code
  ecall                  # Terminate the program


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
    blez a1,load_error
    li t0,0
loop:
    bge t0,a1,loop_end #loop condition
    lw t1,0(a0) #load num to analyse
    bge t1,zero,skip #number changing is inside the loop
    sw x0,0(a0)
skip:
    addi a0,a0,4
    addi t0,t0,1
    j loop

loop_end:
    jr ra                  # normal return

load_error:
    li a0,36

# Exits the program with an error 
# Arguments: 
# a0 (int) is the error code 
# You need to load a0 the error to a0 before to jump here
exit_with_error:
  li a7, 93            # Exit system call
  ecall                # Terminate program

