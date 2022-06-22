.cpu cortex-a35
.global _start

GRF_GPIO2_ADDR = 0xff000034
GRF_GPIO2_VALUE = 0x0ff00440

.section .text
.word 0x33334b52

_start:
        # move from coprocessor register to arm register
        mrs x9, mpidr_el1
        # test it
        tst x9, 0b11
        # if ... branch
        b.eq . + 0x0c
        # 
        wfe
        # alway branch to
        b.al . - 0x04
        # move to x9 register bits 
        movz x9, :abs_g1:GRF_GPIO2_ADDR
        mov w10, GRF_GPIO2_VALUE
        str w10, [x9]
        b.al .
