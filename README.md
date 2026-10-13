# buddy-cli 🐾

> *In memory of 嬌嬌 (Jiao Jiao) — a Schnauzer with a terrible sense of direction,  
> who wandered everywhere for 15 years and always found her way back.*

A lightweight ASCII animal companion that lives in your terminal.  
Zero dependencies — pure Python 3.

```
|\  /|
(o''o)   ← Jiao Jiao
\_ww_/>
```

## Preview

```
 Jiao Jiao ♥♥♥♥♡  ●●●●○ is so happy
    *   ·    ·     ·                  *    *         ( )*             .
                    ·            ·.              *   (_)    *.    · ·
                              (~~~)
     (~~~)
     (8)
      |
                                          ♥ ♥♥
       ^            ^           ^       ╭────────────╮
      /^\          /^\         /^\      │ more pats! │
     / \          / \         / \       ╰───v────────╯
       |            |           |         |\  /|
  v,v  |vv          |           |v,vvv  v,(^''^),;,       v,v ,;,
____..__.._._.______..____.__.________._..\_ww_/~...____._.___.___...__
    p pet · f feed · b ball · t trick · c call · s sit · ␣ hi · q quit
```

### Her many faces

```
 |\  /|     |\  /|     |\  /|     /'ww'\     |\  /|      _|\  /|
 (o''o)     (♥''♥)     (^ww^)     (^''^)     (^''^)/    (_(-..-)  zZ
 \_ww_/~    \_ww_/~   ~\_ww_/     |/  \|     /_ww_\
 curious    petted     munching   belly up   waving      napping
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
- Mouse clicks are optional. They work in terminals with xterm mouse support (most Linux and macOS terminals; Windows Terminal support is experimental). The keyboard always works

## Usage

```bash
git clone https://github.com/jungkang0911/buddy-cli.git
cd buddy-cli
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

## 中文說明

嬌嬌是一隻住在終端機裡的雪納瑞，紀念那隻超級路痴、到處亂跑了 15 年，卻總能自己找到路回家的嬌嬌。

執行 `python buddy.py` 之後可以這樣跟她玩：

- `p` 摸摸她，連摸三下她會翻肚討摸
- `f` 餵零食
- `b` 丟球，她會撿回來
- `t` 表演才藝
- `c` 叫她過來，她可能會先走錯路
- `s` 坐下
- 空白鍵 打招呼
- 用滑鼠點她也是摸摸，點其他地方她會跑過去

左上角的 ♥ 是心情，● 是飽足度，放著不管會慢慢下降。她也會自己追蝴蝶、對小鳥叫、挖洞、睡午覺，深夜還會叫你早點睡。

## License

MIT
