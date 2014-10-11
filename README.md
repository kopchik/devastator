# Raspberry Pi remote operated bot

## Fine tunning
in /boot/cmdline.txt:
~~~
loglevel=5 consoleblank=0 smsc95xx.turbo_mode=N
~~~

### Camera stuff
in /boot/config.txt
~~~
gpu_mem_512=128
start_file=start_x.elf
fixup_file=fixup_x.dat
~~~
### Console
~~~
systemctl start getty@ttyAMA0
systemctl enable getty@ttyAMA0.service
ln -s /usr/lib/systemd/system/serial-getty@.service \
  /etc/systemd/system/getty.target.wants/serial-getty@ttyAMA0.service
~~~

### Rng
Setup as here: https://wiki.archlinux.org/index.php/Raspberry_Pi
