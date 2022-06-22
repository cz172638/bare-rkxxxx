TARCH=aarch64-linux-gnu-
AS=$(TARCH)as
LD=$(TARCH)ld
OBJCOPY=$(TARCH)objcopy

binary:
	$(AS) -o app.o code-$(TARGET).S
	$(LD) -o app app.o
	$(OBJCOPY) -S -O binary app app.bin
	python3 pack.py
	mv loader.bin loader-rk3399.bin

load:
	rkdeveloptool db loader-rk3399.bin &
	sleep 2 && pkill rkdeveloptool

clean:
	rm -f app.o app app.bin loader-rk3399.bin
