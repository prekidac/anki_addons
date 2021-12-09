.PHONEY: all install

all:
	@echo
	@echo "To install type 'make install'"
	@echo

install:
	rm -rf ~/.local/share/Anki2/addons21/my_addons/
	mkdir -p ~/.local/share/Anki2/addons21/
	cp -r my_addons/ ~/.local/share/Anki2/addons21/
