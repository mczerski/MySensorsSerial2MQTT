
PREFIX ?= /usr/local
INITDIR_SYSTEMD = /etc/systemd/system
BINDIR = $(PREFIX)/bin

RM = rm
INSTALL = install -p
INSTALL_PROGRAM = $(INSTALL) -m755
INSTALL_SCRIPT = $(INSTALL) -m755
INSTALL_DATA = $(INSTALL) -m644
INSTALL_DIR = $(INSTALL) -d

Q = @

help:
	$(Q)echo "install - install scripts"
	$(Q)echo "uninstall - uninstall scripts"

install:
	$(Q)echo -e '\033[1;32mInstalling main scripts...\033[0m'
	$(INSTALL_DIR) "$(BINDIR)"
	$(INSTALL_PROGRAM) serial2mqtt.py "$(BINDIR)/serial2mqtt"
	$(Q)echo -e '\033[1;32mInstalling systemd files...\033[0m'
	$(INSTALL_DIR) "$(INITDIR_SYSTEMD)"
	$(INSTALL_DATA) mySerial2mqtt.service "$(INITDIR_SYSTEMD)/mySerial2mqtt.service"

uninstall:
	$(RM) "$(INITDIR_SYSTEMD)/mySerial2mqtt.service"
	$(RM) "$(BINDIR)/serial2mqtt"

.PHONY: install uninstall
