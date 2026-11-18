# Music-learning：人聲節奏聽感練習

用耳朵先聽、再看答案的人聲節奏練習頁。人聲是瀏覽器裡用 Web Audio 合成的「母音人聲」，鼓也是合成的，歌詞都是原創。

## 怎麼用
直接用瀏覽器打開 `index.html`，或開啟 GitHub Pages 後瀏覽網站根目錄。最上方的分頁可以切換不同的練習：

| 分頁 | 檔案 | 內容 |
|---|---|---|
| 流行 13 種 | `pages/pop.html` | 正拍、弱起、反拍、3-3-2、搶拍、16 分、三連音……流行歌常見的人聲節奏型 |
| 完整歌曲《夜風》 | `pages/full-song.html` | 把 10 種節奏型組成一首完整的歌，播放時即時說明每段用了哪種節奏型 |
| 饒舌流派 | `pages/rap.html` | Old School、Boom Bap、Trap、旋律饒舌、快嘴、Drill、Jazz Rap |
| J-POP | `pages/jpop.html` | 促音、長音、弱起、裏拍、搶拍、キメ、VOCALOID 高速 16 分、City Pop 跳ね（日文歌詞＋羅馬拼音） |
| 《浪子回頭》 | `pages/langzi.html` | 茄子蛋〈浪子回頭〉照樂譜整理的人聲節奏：一句一句練、整段練（🔗 接龍）、這首歌用到的 10 種節奏型（只顯示每句開頭兩個字當提示） |
| R&B | `pages/rnb.html` | 90s 切分、New Jack Swing、Neo-Soul、Trap Soul、6/8、轉音、Ad-lib、和聲應答 |

每個節奏型都可以切換「人聲＋鼓／只人聲／只鼓」、調速度，按「揭曉答案」看格子譜，也有盲聽和隨機測驗。

## 其他
- `docs/suno-prompts.md`：把歌詞貼進 Suno 生成真人感人聲用的提示詞。
- `tools/generator/`：饒舌、J-POP、R&B 三頁的產生器；`langzi.py`＋`template_song.html` 產生《浪子回頭》頁（樂譜節奏記在 `langzi.py` 開頭）。修改 `rap.py`、`jpop.py`、`rnb.py` 裡的節奏與歌詞後，在該資料夾執行 `pip install pypinyin` 和 `python3 rap.py`（或另外兩個）即可重新產生頁面。
