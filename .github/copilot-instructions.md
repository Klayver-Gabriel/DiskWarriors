<!-- .github/copilot-instructions.md - guidance for AI coding agents -->
# Project-specific guidance for AI coding agents

This repository is a small Pygame Zero (pgzero) game project. Keep suggestions tightly scoped to the files in `bin/` and the `resources/` folders. Follow these specific rules when editing or adding code.

- Important files and purpose
  - `bin/Screen.py` — main game script. Exposes pgzero hooks (`draw`, `update`, `on_key_down`) and a `GameStateManager` controlling `MENU` and `JOGANDO` states.
  - `bin/KeyHandler.py` — currently empty placeholder intended for input handling logic. If you add code, keep the interface minimal (functions or a class that accept pgzero `key` values).
  - `resources/images/`, `resources/sounds/` — asset folders. Refer to assets by filename (no absolute paths). Keep image sizes modest (<= 1024px) and sound lengths short.

- How to run and test changes
  - Run the game using pgzero from the repository root or `bin/`:
    - Preferred: `pgzrun bin/Screen.py` (pgzero will call `draw`, `update`, and `on_key_down` hooks)
    - Alternative for IDEs that embed pgzero: keep `pgzrun.go()` commented or uncommented depending on environment.

- Code style & idioms specific to this repo
  - Use simple, imperative functions and small classes. `GameStateManager` is the canonical pattern for switching screens/states — follow its design when adding menu or gameplay screens.
  - Prefer explicit string states (e.g., `"MENU"`, `"JOGANDO"`) rather than booleans or enums unless a clear need arises. When adding states, update `draw` and `on_key_down` to handle them.
  - Keep global constants for `WIDTH`, `HEIGHT`, and `TITLE` in the main `Screen.py` file; other modules should import them if necessary.

- Tests, linting, and build
  - There are no automated tests or build pipeline in the repo. Focus on manual runs with `pgzrun` for verification. Keep changes minimal and run the script locally after edits.

- Patterns and examples to follow
  - When adding input handling, place shared logic in `bin/KeyHandler.py` and call it from `Screen.py`'s `on_key_down`. Example pattern:

    def on_key_down(key):
        if game_manager.state == "MENU":
            KeyHandler.handle_menu_key(key, game_manager)

  - When introducing new screens, add `draw_<screenname>` methods on `GameStateManager` and dispatch from `draw()`.

- Integration and external dependencies
  - This project depends on Pygame Zero (pgzero) and the `pgzrun` runtime. Do not add heavy external dependencies. If needed, document them in a new `requirements.txt` and notify the maintainer.

- Safety and non-goals
  - Do not refactor the project into a different engine or framework (e.g., pure Pygame, Unity). Keep the pgzero hook model intact.

If anything in this summary is incorrect or you'd like more details (input mapping, planned game states, or asset naming conventions), tell me what to clarify and I will update the instructions.
