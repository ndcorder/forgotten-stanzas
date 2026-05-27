"""
game.py — Main game loop for Crisis At T-Minus Nothing.

Curses-based terminal interface. Mission control aesthetic.
The display lies. The prose encodes the truth.

Run: python game.py
Requires: Python 3.6+, curses (standard on Unix; windows-curses on Windows)
"""

import curses
import time
import textwrap
import sys
from typing import List, Optional

from state import MissionState, GameStateManager
from narrative import NarrativeEngine
from encoder import analyze_text, format_layer_hint


# ─── Display Constants ──────────────────────────────────

COLOR_BG = curses.COLOR_BLACK
COLOR_GREEN = 1
COLOR_AMBER = 2
COLOR_RED = 3
COLOR_DIM = 4
COLOR_WHITE = 5
COLOR_CYAN = 6

ACTIONS = {
    'r': ('repair <system>', 'Repair a subsystem'),
    'c': ('check <system>', 'Check system status'),
    'd': ('diagnose <system>', 'Deep system scan'),
    'o': ('override', 'Attempt launch override'),
    'w': ('wait', 'Hold position'),
    'a': ('analyze', 'Analyze last log entry'),
    '?': ('help', 'Show commands'),
    'q': ('quit', 'Abort session'),
}

SYSTEMS = ['life_support', 'comms', 'propulsion', 'navigation']


# ─── UI Helpers ─────────────────────────────────────────

def init_colors():
    curses.init_pair(COLOR_GREEN, curses.COLOR_GREEN, COLOR_BG)
    curses.init_pair(COLOR_AMBER, curses.COLOR_YELLOW, COLOR_BG)
    curses.init_pair(COLOR_RED, curses.COLOR_RED, COLOR_BG)
    curses.init_pair(COLOR_DIM, 8, COLOR_BG)  # dark gray
    curses.init_pair(COLOR_WHITE, curses.COLOR_WHITE, COLOR_BG)
    curses.init_pair(COLOR_CYAN, curses.COLOR_CYAN, COLOR_BG)

def status_color(stability: float) -> int:
    if stability >= 0.8: return COLOR_GREEN
    if stability >= 0.5: return COLOR_AMBER
    if stability >= 0.2: return COLOR_RED
    return COLOR_RED

def wrap(text: str, width: int) -> List[str]:
    return textwrap.wrap(text, width=width)


# ─── Main Game ──────────────────────────────────────────

class CrisisGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.manager = GameStateManager()
        self.state = MissionState(self.manager.completion_count)
        self.engine = NarrativeEngine(self.state)
        self.last_log = ""
        self.log_scroll: List[str] = []
        self.input_buffer = ""
        self.running = True
        self.show_analysis = False
        self.analysis_text = ""

    def run(self):
        """Main game loop."""
        self.stdscr.nodelay(True)
        curses.curs_set(1)
        init_colors()

        # Show opening
        opening = self.engine.generate_opening_text(self.manager.completion_count)
        hint = self.manager.replay_hint()
        if hint:
            opening += "\n\n" + hint
        self.log_scroll = wrap(opening, 70)

        while self.running:
            self._handle_input()
            self._draw()
            time.sleep(0.05)

    def _handle_input(self):
        """Process user input."""
        try:
            ch = self.stdscr.getch()
        except curses.error:
            return

        if ch == -1:
            return

        if ch == curses.KEY_RESIZE:
            return

        # Show analysis mode overlay
        if self.show_analysis:
            if ch in (ord('q'), ord('Q'), 27):  # q or ESC
                self.show_analysis = False
                self.analysis_text = ""
            return

        # Handle backspace
        if ch in (curses.KEY_BACKSPACE, 127, 8):
            self.input_buffer = self.input_buffer[:-1]
            return

        # Handle enter
        if ch in (10, 13):
            self._execute_command(self.input_buffer.strip())
            self.input_buffer = ""
            return

        # Handle printable characters
        if 32 <= ch <= 126:
            self.input_buffer += chr(ch)

    def _execute_command(self, cmd: str):
        """Parse and execute a player command."""
        if not cmd:
            return

        parts = cmd.lower().split()
        action = parts[0]
        target = parts[1] if len(parts) > 1 else ""

        if action in ('q', 'quit', 'exit'):
            self.running = False
            return

        if action in ('?', 'help'):
            self._show_help()
            return

        if action == 'a' or action == 'analyze':
            self._do_analysis()
            return

        # Map single-letter shortcuts
        action_map = {
            'r': 'repair', 'repair': 'repair',
            'c': 'check', 'check': 'check',
            'd': 'diagnose', 'diagnose': 'diagnose',
            'o': 'override', 'override': 'override',
            'w': 'wait', 'wait': 'wait',
        }

        mapped = action_map.get(action)
        if not mapped:
            self._add_log("Unknown command: {}".format(cmd))
            return

        if mapped in ('repair', 'check', 'diagnose') and target not in SYSTEMS:
            self._add_log("Specify a system: {}".format(", ".join(SYSTEMS)))
            return

        # Execute action on game state
        result = self.state.execute_action(mapped, target)

        # Generate and add log entry
        log_entry = self.engine.generate_log_entry()
        self.last_log = log_entry
        for line in log_entry.split('\n'):
            for wrapped in wrap(line, 70):
                self._add_log(wrapped)

        # Add official response
        if result.get('official'):
            for line in wrap(result['official'], 70):
                self._add_log("  > " + line)

        # Tick the clock
        official, true = self.state.tick()

        # Check for catastrophe
        if self.state.catastrophe_triggered:
            self._add_log("")
            cat_text = self.engine.generate_catastrophe_text()
            self.last_log = cat_text
            for line in cat_text.split('\n'):
                for wrapped in wrap(line, 70):
                    self._add_log(wrapped)
            self._add_log("")
            self._add_log("CONTINGENCY. The mission has concluded.")
            self._end_game()
            return

        if self.state.is_terminal():
            self._add_log("")
            self._add_log("Mission clock has reached zero. Sequence complete.")
            self._add_log("All events have been logged per standard procedure.")
            self._end_game()
            return

    def _do_analysis(self):
        """Run analysis mode on the last log entry."""
        if not self.last_log:
            self._add_log("No log entry to analyze.")
            return

        if not self.manager.is_analysis_available():
            self._add_log("Analysis mode not yet available. Complete a session first.")
            return

        level = self.manager.get_analysis_level()
        self.analysis_text = analyze_text(self.last_log, level)
        self.show_analysis = True

    def _show_help(self):
        """Show available commands."""
        self._add_log("─── AVAILABLE COMMANDS ───")
        for key, (cmd, desc) in ACTIONS.items():
            self._add_log("  {} — {}".format(cmd, desc))
        self._add_log("Systems: {}".format(", ".join(SYSTEMS)))
        self._add_log("──────────────────────────")

    def _add_log(self, text: str):
        """Add a line to the scroll buffer."""
        self.log_scroll.append(text)
        # Keep buffer manageable
        if len(self.log_scroll) > 500:
            self.log_scroll = self.log_scroll[-300:]

    def _end_game(self):
        """Record completion and show end state."""
        self.manager.record_completion(self.state)
        self._add_log("")
        self._add_log("Session recorded. Completion #{}".format(
            self.manager.completion_count
        ))
        hint = format_layer_hint(self.manager.completion_count)
        if hint:
            self._add_log(hint)
        self._add_log("Press q to exit. Run again to begin a new session.")

    def _draw(self):
        """Render the full display."""
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        # ── Header: Mission Clock ──
        countdown = self.state.format_official()
        self.stdscr.addstr(0, 2, "MERIDIAN-7 MISSION CONTROL", curses.color_pair(COLOR_CYAN))
        self.stdscr.addstr(0, w - 20, countdown, curses.color_pair(COLOR_GREEN) | curses.A_BOLD)

        # ── Status Bar: Systems ──
        y = 1
        self.stdscr.addstr(y, 0, "─" * w, curses.color_pair(COLOR_DIM))
        y = 2
        for name, sys in self.state.systems.items():
            label = name.upper().replace('_', ' ')
            stability = sys.display_stability
            color = status_color(stability)
            bar_len = 12
            filled = int(stability * bar_len)
            bar = "█" * filled + "░" * (bar_len - filled)
            text = "{} [{:>4.0%}] {}".format(label[:6], stability, bar)
            self.stdscr.addstr(y, 2, text, curses.color_pair(color))
            y += 1

        # Override status
        ov_color = COLOR_GREEN if self.state.override_official else COLOR_RED
        ov_text = "OVERRIDE: AVAIL" if self.state.override_official else "OVERRIDE: ----"
        self.stdscr.addstr(2, w - 22, ov_text, curses.color_pair(ov_color))

        # Turn counter
        self.stdscr.addstr(3, w - 22, "TURN: {:03d}".format(self.state.turn_number),
                          curses.color_pair(COLOR_DIM))

        # ── Separator ──
        y = 6
        self.stdscr.addstr(y, 0, "─" * w, curses.color_pair(COLOR_DIM))

        # ── Log Area ──
        y = 7
        log_area_height = h - 10
        visible = self.log_scroll[-log_area_height:]

        for i, line in enumerate(visible):
            if y + i >= h - 3:
                break
            if line.startswith("───") or line.startswith("══"):
                self.stdscr.addstr(y + i, 1, line[:w-2], curses.color_pair(COLOR_CYAN))
            elif line.startswith("  > "):
                self.stdscr.addstr(y + i, 1, line[:w-2], curses.color_pair(COLOR_GREEN))
            elif "CONTINGENCY" in line or "EMERGENCY" in line:
                self.stdscr.addstr(y + i, 1, line[:w-2], curses.color_pair(COLOR_RED) | curses.A_BOLD)
            elif line.startswith("[NOTICE"):
                self.stdscr.addstr(y + i, 1, line[:w-2], curses.color_pair(COLOR_AMBER))
            else:
                self.stdscr.addstr(y + i, 1, line[:w-2], curses.color_pair(COLOR_WHITE))

        # ── Analysis Overlay ──
        if self.show_analysis and self.analysis_text:
            self._draw_analysis(h, w)
            return

        # ── Input Bar ──
        self.stdscr.addstr(h - 2, 0, "─" * w, curses.color_pair(COLOR_DIM))
        prompt = "> " + self.input_buffer
        self.stdscr.addstr(h - 1, 1, prompt[:w-3], curses.color_pair(COLOR_GREEN))
        curses.curs_set(1)

        self.stdscr.refresh()

    def _draw_analysis(self, h: int, w: int):
        """Draw analysis mode overlay."""
        # Dim background
        self.stdscr.bkgd(' ', curses.color_pair(COLOR_DIM))

        lines = self.analysis_text.split('\n')
        start_y = max(0, (h - len(lines)) // 2)
        start_x = max(0, (w - 70) // 2)

        for i, line in enumerate(lines):
            if start_y + i >= h - 1:
                break
            display_line = line[:w - 2]
            if line.startswith("═"):
                self.stdscr.addstr(start_y + i, start_x, display_line,
                                  curses.color_pair(COLOR_CYAN))
            elif line.startswith("─"):
                self.stdscr.addstr(start_y + i, start_x, display_line,
                                  curses.color_pair(COLOR_CYAN))
            elif line.startswith("  ▸"):
                self.stdscr.addstr(start_y + i, start_x, display_line,
                                  curses.color_pair(COLOR_AMBER) | curses.A_BOLD)
            elif "LAYER" in line:
                self.stdscr.addstr(start_y + i, start_x, display_line,
                                  curses.color_pair(COLOR_GREEN) | curses.A_BOLD)
            elif line.startswith("  S") or line.startswith("  P"):
                self.stdscr.addstr(start_y + i, start_x, display_line,
                                  curses.color_pair(COLOR_WHITE))
            else:
                self.stdscr.addstr(start_y + i, start_x, display_line,
                                  curses.color_pair(COLOR_DIM))

        self.stdscr.addstr(h - 1, 1, "[Press q or ESC to close]",
                          curses.color_pair(COLOR_AMBER))
        self.stdscr.refresh()


# ─── Entry Point ────────────────────────────────────────

def main(stdscr):
    game = CrisisGame(stdscr)
    game.run()

if __name__ == '__main__':
    curses.wrapper(main)
