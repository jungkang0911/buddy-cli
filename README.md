# buddy-cli 🐾

> *In memory of 嬌嬌 (Jiao Jiao) — a Schnauzer with a terrible sense of direction,  
> who wandered everywhere for 15 years and always found her way back.*

A lightweight ASCII animal companion that lives in your terminal.  
Zero dependencies — pure Python 3.

```
|\  /|
(o''o)   ← Jiao Jiao
\_ww_/->
```

## Features

- **Jiao Jiao the Schnauzer** walks, sits, sleeps, and digs when bored
- She's directionally challenged — randomly second-guesses herself mid-walk with `Huh?` / `Where am I?`
- **Bird** flies across the sky occasionally — Jiao Jiao looks up
- **Butterfly** flutters around — Jiao Jiao chases it
- Speech bubbles pop up at random
- Auto-redraws on terminal resize
- Practically zero CPU / memory

## Requirements

- Python 3.6+
- Windows Terminal or any ANSI-capable terminal

## Usage

```bash
python buddy.py
```

Press `Ctrl+C` to quit.

**Tip:** In Windows Terminal press `Alt+Shift++` to split a pane,  
run Jiao Jiao there, and keep your main pane for work.

## Interactions

| Trigger | Jiao Jiao's reaction |
|---------|----------------------|
| Butterfly nearby | Chases it |
| Catches butterfly | `Got it!!` |
| Bird flies overhead | Looks up |
| Standing still too long | Sits → digs or sleeps |
| Just walking | May randomly spin around (`Where am I?`) |

## License

MIT
