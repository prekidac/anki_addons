.PHONEY: all install

all:
	@echo
	@echo "To install type 'make install'"
	@echo

install:
	@[ -d ~/.local/share/Anki2/addons21/my_addons/ ] \
	&& rm -rf ~/.local/share/Anki2/addons21/my_addons/ \
	|| mkdir -p ~/.local/share/Anki2/addons21/
	@cp -r my_addons/ ~/.local/share/Anki2/addons21/

zip:
	cd my_addons && zip -r ~/anki_addons.ankiaddon *
