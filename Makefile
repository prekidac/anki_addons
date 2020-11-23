.PHONY: all install

all:
	@echo
	@echo "To install type 'make install'"
	@echo
install:
	@mkdir -p ~/.local/share/Anki2/addons21/ 2>/dev/null
	@cp -r my_addons/ ~/.local/share/Anki2/addons21/