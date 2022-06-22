.cpu cortex-a53
.global _start

GRF_GPIO4_ADDR = 0xff77e024 
GRF_GPIO4_VALUE = 0x00f000a0

.section .text
.word 0x33334b52

_start:
        # move from coprocessor register to arm register
        mrs x9, mpidr_el1
        # test it
        tst x9, 0b11
        b.eq . + 0x0c
        # 
        wfe
        b.al . - 0x04
        # move to x9 register bits 
        movz x9, :abs_g0_nc:GRF_GPIO4_ADDR
        movk x9, :abs_g1:GRF_GPIO4_ADDR
        movz w10, :abs_g0_nc:GRF_GPIO4_VALUE
        movk w10, :abs_g1:GRF_GPIO4_VALUE
        str w10, [x9]
        b.al .
