# Raspberry Pi remote operated bot

## Fine tunning
in /boot/cmdline.txt:
~~~
loglevel=5 consoleblank=0 smsc95xx.turbo_mode=N
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
