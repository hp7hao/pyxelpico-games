.PHONY: native native-game web web-game clean-native clean-web clean

PYXELPICO_DIR ?= ../pyxelpico
PYTHON ?= $(PYXELPICO_DIR)/.venv/bin/python
GAME ?=
DESTDIR ?=

native:
	@$(PYTHON) scripts/build_native.py $(if $(DESTDIR),--destdir $(DESTDIR),)

native-game:
	@test -n "$(GAME)" || { echo "usage: make native-game GAME=<game-id>" >&2; exit 2; }
	@$(PYTHON) scripts/build_native.py --game $(GAME) $(if $(DESTDIR),--destdir $(DESTDIR),)

web:
	@$(PYTHON) scripts/build_web.py --pyxelpico-dir $(PYXELPICO_DIR)

web-game:
	@test -n "$(GAME)" || { echo "usage: make web-game GAME=<game-id>" >&2; exit 2; }
	@$(PYTHON) scripts/build_web.py --pyxelpico-dir $(PYXELPICO_DIR) --game $(GAME)

clean-web:
	@rm -rf dist/web

clean-native:
	@rm -rf dist/native

clean: clean-native clean-web
