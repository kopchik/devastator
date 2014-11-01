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


### Real Time Clock
in /etc/systemd/system/rtc.service
~~~
[Unit]
Description=RTC clock
Before=systemd-timesyncd.service

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'echo ds1307 0x68 >/sys/bus/i2c/devices/i2c-1/new_device'
ExecStart=/bin/bash -c 'hwclock --hctosys'

ExecStop=/bin/bash  -c 'hwclock --systohc'

[Install]
WantedBy=multi-user.target
~~~
Then systemctl enable rtc .
