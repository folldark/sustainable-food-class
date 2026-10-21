# 和美高中 115-1 永續小食堂

這是多元選修「永續小食堂」的長期教材 repo。各次上課的投影片、講義原稿與單元素材放在 `lessons/`，由課程首頁集中列出入口；後續單元沿用同一套色票與字型。

目前單元：

- **2026-09-04 課程簡介與緒論**，共 36 張投影片。多元選修怎麼選、升學制度插播、課程規則、分組活動，以及飲食與永續緒論。
- **2026-09-10 地球界限與食物工業化**，共 41 張投影片。第一節玩食物版「誰是臥底」蒐集學生自己的描述，第二節用講述帶工業革命、食品工業化與消費社會，收在兩個真實案例：2018 年美國蘿蔓生菜大腸桿菌疫情，以及墨西哥灣缺氧區。另附教師指南、19 組題庫、30 張遊戲卡、PDF 與離線教材包。原先規劃的 draw.io 食物關係圖活動改為講述，模板與紙本備援保留在資料夾內供後續週次使用。
- **2026-09-17 為什麼跨國企業壓榨小農**，共 20 張投影片。由舊 Keynote 投影片（14 頁 PDF）轉製：從早餐那杯咖啡出發，咖啡產業現況（全球、區域、台灣、生豆價格）換成 2026 年 8 月 ICO 月報與台灣近兩年統計，「來種咖啡好不好？」之後插入志祺七七的咖啡產業影片連結，再進三個咖啡農情境題、資本主義的強制競爭原則與 SDGs。
- **2026-10-08 鹽漬與糖漬**，共 26 張投影片，另附三份長文頁面。第一段針對〈當執行長的一天〉心得，說明「詳答」的五個零件與五段式綜合心得（含法國哲學會考的對照）；第二段分組實作摩洛哥醃檸檬與糖漬檸檬。`salt-lemon.html`（原講義延伸版）、`sugar-lemon.html`（新寫）、`writing-guide.html`（學生用寫作指引，含檢核表與評分規準）。原講義 PDF 逐字轉錄為 `講義原稿.md`。
- **2026-10-22 農村的遠見與 ORID**，共 23 張投影片。老師公差、學生自主上課：登入公視+，《農村的遠見》（台語版）十集任選一集看完，以 ORID（客觀／感受／詮釋／決定）填寫學習單；ORID 四層各一張說明，示範用 10/8 的醃檸檬實作走一次。`styles.css` 末尾新增 `.episode-grid`、`.orid-grid`、`.orid-level`、`.flow-three`／`.flow-four`、`.link-card.light`。

## 目錄結構

```text
sustainable-food-class/
├── index.html                       # 課程首頁與單元列表
├── styles.css                       # 首頁與 2026-09-04 單元共用樣式
├── app.js                           # 2026-09-04 單元的投影片引擎
├── favicon.svg
├── .nojekyll
├── .gitignore
├── README.md
└── lessons/
    ├── 2026-09-04-課程簡介與緒論/
    │   ├── index.html               # 本次投影片
    │   ├── 講義原稿.md               # 保留原始內容，不由程式覆寫
    │   └── assets/
    │       ├── food-system.png
    │       └── hidden-costs.png
    ├── 2026-09-17-為什麼跨國企業壓榨小農/
    │   ├── index.html               # 本次投影片（共用根目錄引擎）
    │   ├── 講義原稿.md               # 舊 PDF 逐頁轉錄
    │   └── assets/                  # 六張圖，來源見下方
    └── 2026-09-10-地球界限與食物工業化/   # 由 build.py 產生，自帶樣式與引擎
        ├── build.py                 # 唯一的編輯入口，改內容後重新執行
        ├── index.html               # 投影片（產生物）
        ├── teacher.html             # 教師指南（產生物）
        ├── student.html             # 學生任務與模板連結（產生物）
        ├── cards.html               # 遊戲卡列印頁（產生物）
        ├── template-print.html      # A3 紙本備援（產生物）
        ├── food-relationships.drawio
        ├── slide-notes.json
        ├── lesson.css / lesson.js / handout.css
        ├── slides.pdf / cards.pdf / template-print.pdf / lesson-pack.zip
        └── assets/planetary-boundaries-2025.jpg
```

投影片引擎分兩種：`2026-09-04-課程簡介與緒論` 與 `2026-09-17-為什麼跨國企業壓榨小農` 使用根目錄的 `styles.css` 與 `app.js`；`2026-09-10-地球界限與食物工業化` 是 `build.py` 產出的自帶樣式版本。共用的是課程首頁、色票與字型。日後新單元一律用根目錄引擎。

根目錄 `app.js` 與 `folldark/research-writing-class` 的版本相同（`data-title`、控制列的「備註」與「全螢幕」按鈕、非當前投影片加 `inert`；2026-10-08 起同步「快速跳頁」：數字＋Enter 跳頁、`G` 或點頁碼開目錄）。頁碼 `#counter` 必須是 `<button>`，三個根目錄引擎單元都已改好；`styles.css` 的 `.goto-*` 規則要保留。

## 本地預覽

在專案根目錄執行：

```bash
python3 -m http.server 8000
```

以瀏覽器開啟 <http://localhost:8000>，從課程首頁進入單元。結束預覽時，在 Terminal 按 `Ctrl+C`。

全站是純靜態 HTML／CSS／JavaScript，不需要套件安裝或建置步驟，不依賴外部 CDN。字型使用 macOS 內建的 PingFang TC、Noto Sans TC，以及其他常見系統字型 Microsoft JhengHei、system-ui。站內檔案採相對路徑，可直接用於 GitHub Pages 的 repository 子路徑。

## 操作方式

`2026-09-04-課程簡介與緒論`、`2026-09-17-為什麼跨國企業壓榨小農`、`2026-10-08-鹽漬與糖漬` 單元：

| 按鍵／操作 | 功能 |
| --- | --- |
| `←`／`→`、`PageUp`／`PageDown` | 上一張／下一張 |
| `Space`／`Enter` | 下一張 |
| `Home`／`End` | 第一張／最後一張 |
| `F` | 進入或離開全螢幕 |
| `N` | 開啟或關閉講者備註 |
| 左右滑動 | 觸控換頁 |
| 數字＋`Enter` | 跳到該頁 |
| `G`／點頁碼 | 開啟目錄 |
| 底部控制列 | 換頁、備註、全螢幕、說明與返回課程首頁 |

`2026-09-10-地球界限與食物工業化` 單元：方向鍵換頁，`N` 開關備註，`F` 全螢幕，底部控制列另有目錄、教師備課與返回課程首頁。遊戲進行時務必關閉備註，備註內含臥底題目。

## 日後新增單元

1. 在 `lessons/` 建立 `YYYY-MM-DD-單元名稱/`，把新原稿存成 `講義原稿.md`，圖片放進該資料夾的 `assets/`。
2. 複製 `2026-09-17-為什麼跨國企業壓榨小農/index.html` 作為骨架（控制列已含備註與全螢幕按鈕，`<main>` 要有 `tabindex="-1"` 與 `data-title`），更改頁面 `<title>`、description、日期與封面資訊，替換 `<main class="deck">` 內的投影片內容。維持 `lang="zh-Hant-TW"`。
3. 每張投影片保留 `class="slide"`、`data-section` 與 `data-theme`；主題色可用 `forest`、`cream`、`paper`、`mango`、`teal`。頁數與進度由 `app.js` 自動計算，不必修改。
4. 依內容選用 `title-slide`、`section-slide`、`statement-slide`、`question-slide`；數據頁用 `stat-slide` 加 `.score-grid` 或 `.data-table`，外部連結用 `.link-card`，多張照片用 `.photo-trio`，整張圖用 `.image-full`（都定義在 `styles.css` 末尾）。講者提示放在 `<aside class="speaker-notes">`，不擴寫原稿正文；沒有實質提示就不要放空泛的罐頭備註。
5. 保留頁面底部控制列、講者備註面板、說明 dialog 與 `class="course-link"` 的返回首頁連結。共用檔案繼續引用 `../../styles.css`、`../../app.js`、`../../favicon.svg`；單元圖片用 `assets/圖片.png`。
6. 在根目錄 `index.html` 的 `.lesson-list` 複製一個 `<li>`，更新入口相對路徑、日期、名稱與一句話說明。
7. 長文講義（可捲動、可列印）用 `<body class="handout">`，骨架複製 `2026-10-08-鹽漬與糖漬/salt-lemon.html`；樣式（`.toc`、`.callout`、`.steps`、`.fig-pair`、`.refs`）在 `styles.css` 末尾。首頁單元下要列講義時，在該 `<li>` 的 `<a>` 後面加 `<p class="entry-extra">`。
8. 本地預覽，檢查正文、投影畫面、手機、換頁與連結，並在 README 補上新增圖片的來源與授權說明。

修改 `2026-09-10-地球界限與食物工業化` 的內容一律改 `build.py` 再重新執行 `python3 build.py`，不要直接改該資料夾的 HTML，否則下次重建會被覆寫。

PDF 與 `lesson-pack.zip` 不由 `build.py` 產生。改完內容後，在 repo 根目錄起本地伺服器，再用 Playwright 重新輸出：

```bash
python3 -m http.server 8765
node pdfs.mjs      # 對 index.html、cards.html、template-print.html 呼叫 page.pdf()
zip -r lesson-pack.zip index.html student.html teacher.html teacher-guide.md \
  cards.html cards.pdf template-print.html template-print.pdf \
  food-relationships.drawio slides.pdf lesson.css lesson.js handout.css \
  slide-notes.json build.py assets
```

`cards.pdf` 一定要跟著題庫重新輸出，否則老師會印到舊的臥底題目。

## 設計與內容說明

- 視覺以字級、字重與配色變化為主，抽象插畫只用於少數章節轉場。
- 升學制度補充以 115 學年度現行規則為基準；學生實際申請時，仍應查閱當年度簡章。
- 原稿中的教室口語與提問盡量保留，講者提示放在備註面板。

## 圖片來源

`lessons/2026-09-04-課程簡介與緒論/assets/` 的 `food-system.png` 與 `hidden-costs.png` 由 OpenAI ImageGen 依本課程需求產生，未使用外部圖片素材。

`lessons/2026-09-10-地球界限與食物工業化/assets/` 的四張圖都是外部來源，非自製：

| 檔案 | 來源 | 授權或狀態 |
| --- | --- | --- |
| `planetary-boundaries-2025.jpg` | Azote for Stockholm Resilience Centre, based on Sakschewski and Caesar et al. 2025 | CC BY-NC-ND 3.0 |
| `romaine-ecoli-2018-cdc-map.jpg` | U.S. CDC，2018 年蘿蔓生菜 E. coli O157:H7 疫情各州病例分布圖 | 美國聯邦政府作品 |
| `gulf-hypoxia-2025-map.jpg` | LSU 與 NOAA，2025 Shelfwide Cruise 底層溶氧圖，裁切自原始雙欄圖上半部 | 教學使用並標示出處 |
| `gulf-hypoxia-1985-2025-chart.jpg` | LSU 與 NOAA，1985–2025 年底層缺氧面積長條圖，裁切自同一張原始圖下半部 | 教學使用並標示出處 |

投影片上都保留了原始出處字樣。

`lessons/2026-10-08-鹽漬與糖漬/assets/` 的九張圖皆取自 Wikimedia Commons，作者與授權也寫在各頁圖說：

| 檔案 | 內容 | 作者／授權 |
| --- | --- | --- |
| `making-preserved-lemons.jpg` | 切十字塞鹽的檸檬 | George M. Groutas，CC BY 2.0 |
| `preserved-lemon-jar.jpg` | 放了四年的醃檸檬 | Michal Klajban，CC BY-SA 4.0 |
| `tagine-preserved-lemon.jpg` | 塔吉燉雞配醃檸檬與橄欖 | Foodista，CC BY 2.0 |
| `salted-lemon-7up.jpg` | 香港茶餐廳鹹檸檬汽水 | King030yu，CC BY-SA 4.0 |
| `lemon-cheong.jpg` | 石榴檸檬「청」 | Jon Sega，CC BY-SA 4.0 |
| `membrillo.jpg` | 西班牙榲桲果糕 | Asturnut，CC BY-SA 3.0 |
| `succade.jpg` | 糖漬香櫞皮丁 | Ich，CC BY-SA 4.0 |
| `frutta-candita.jpg` | 義大利糖漬水果攤 | G.steph.rocket，CC BY-SA 3.0 |
| `chinois-confits.jpg` | 糖漬金桔 | avlxyz，CC BY-SA 2.0 |

`lessons/2026-09-17-為什麼跨國企業壓榨小農/assets/` 的六張圖皆從老師原本的 Keynote 投影片抽出，非自製，來源多數未標示：

| 檔案 | 內容 | 來源或狀態 |
| --- | --- | --- |
| `breakfast-toast.jpg` | 熱壓三明治早午餐 | 部落格「奇奇一起玩樂趣」（浮水印 lotuslin.pixnet.net），教學使用 |
| `lurou-rice.jpg` | 滷肉飯 | 浮水印 cook_draw_eat，來源未查，教學使用 |
| `misua.jpg` | 大腸麵線 | 來源未查，教學使用 |
| `coffee-tea-or-me.jpg` | Rich Amooi《Coffee, Tea or Me》書封 | 出版品封面，投影片上有標示 |
| `coffee-farmers-motorbike.jpg` | 兩位咖啡農騎機車載咖啡豆 | 來源未查，教學使用 |
| `sdgs-17-goals-zh.png` | 聯合國 17 項 SDGs 中文版圖示 | 聯合國 SDGs 識別，教學使用 |

原投影片的 ICO 消費表與今周刊報導截圖未沿用，數據改以 ICO《Coffee Market Report》（2025 年 12 月、2026 年 8 月）、經濟日報、自由時報與未來流通研究所的統計重排，各張投影片下方都有來源列。

## 授權

課程文字與投影片設計保留所有權利。未經授權，請勿重製或另行散布。外部文章及相關內容的權利歸原作者與網站所有。
