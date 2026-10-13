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

- **Jiao Jiao the Schnauzer** walks, sits, naps (with floating `zZ`), and digs when bored. Sometimes she digs something up
- She's directionally challenged: she second-guesses herself mid-walk (`Huh?` / `Where am I?`), and when you call her she sometimes runs the wrong way first
- **Expressions**: blinks, heart eyes `(♥''♥)` when she's happy, `(^''^)` when she's pleased, droopy eyes when she's hungry or lonely
- **Mood ♥ and food ● meters**: they drop slowly over time, so keep her fed and play with her
- **Bird** flies past. She looks up and sometimes barks it away
- **Butterfly** flutters around. She chases it, and sometimes it lands on her head while she sits or sleeps
- Hearts, sparkles, crumbs and dirt particles, plus speech bubbles that follow her around
- She gets sleepy late at night
- Auto-redraws on terminal resize. Practically zero CPU and memory

## Requirements

- Python 3.6+
- Windows Terminal or any ANSI-capable terminal

## Usage

```bash
python buddy.py
```

Press `q` or `Ctrl+C` to quit. She tells you how many pets, treats, fetches and tricks you shared.

**Tip:** In Windows Terminal press `Alt+Shift++` to split a pane,  
run Jiao Jiao there, and keep your main pane for work.

## Controls

| Key | What happens |
|-----|--------------|
| `p` | Pet her: hearts, heart eyes, tail wags. Pet her 3 times quickly and she rolls over for belly rubs |
| `f` | Drop a treat: she runs over and eats it (`nom nom`) |
| `b` | Throw the ball: she fetches it and brings it back (`Again? Again!`) |
| `t` | Ask for a trick: roll over, spin, beg or hop. She won't do tricks when she's too hungry |
| `c` | Call her: she comes to you, if she doesn't get lost on the way |
| `s` | Sit |
| `space` | Say hi: she hops and greets you. If she's asleep, she asks for 5 more minutes |
| `h` | Show or hide the help bar |
| **click her** | Pet her (in terminals with mouse support) |
| **click anywhere else** | She runs over to that spot |

## Things she does on her own

| Trigger | Jiao Jiao's reaction |
|---------|----------------------|
| Butterfly nearby | Chases it (`Got it!!` or `aww...`) |
| Butterfly lands on her head | `!! ...don't move` |
| Bird flies overhead | Looks up, sometimes barks |
| Standing still too long | Sits, then digs, naps, or looks at you |
| Hungry or lonely | Asks for a treat or a pat |
| Very happy | Hops around humming `♪` |
| Just walking | May randomly spin around (`Where am I?`) |

## License

MIT
