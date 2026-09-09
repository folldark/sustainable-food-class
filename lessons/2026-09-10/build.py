"""Build the self-contained lesson and editable draw.io template. Python stdlib only."""
from pathlib import Path
from html import escape
import base64, json, urllib.parse, zlib
import xml.etree.ElementTree as ET

HERE = Path(__file__).parent
BASE = 'https://folldark.github.io/sustainable-food-class/lessons/2026-09-10/'
PB = 'https://www.stockholmresilience.org/research/planetary-boundaries.html'
FOOD = 'https://www.nature.com/articles/s43016-025-01252-6'
PAIRS = [
 ('奇異果','蘋果','暖身','水果、買的地方、產地標籤、價格印象','進口、昂貴都是待查的描述。不要把某一種水果直接等同進口。'),
 ('鮮奶','豆漿','第二輪','早餐、紙盒、冰箱、營養印象、品牌','兩者都有不同加工與包裝。健康不能只憑品名或廣告判斷。'),
 ('泡麵','冷凍水餃','第三輪','方便、保存、煮食時間、超市、包裝','加工帶來保存與便利，也可能使用能源與包材。不要把加工直接等同有害。'),
 ('漢堡','三明治','備用','連鎖店、早餐、外帶、價格、規格','適合追問不同店家如何維持相似口味。'),
 ('優格','布丁','備用','杯裝、冷藏、點心、營養宣稱','只記錄健康印象，回到成分、份量與整體飲食再討論。'),
 ('餅乾','洋芋片','備用','零食、包裝、口味、廣告、超商','廣告可能讓人認識產品，也可能影響購買慾望。'),
 ('咖啡','紅茶','銜接下週','飲料店、提神印象、品牌、產地','可接 9/17 咖啡小農，但本節不展開全球貿易史。'),
 ('雞塊','雞排','備用','外帶、油炸、冷凍、連鎖店、大小','可談規格與加工，不把店型當成食品安全證據。'),
 ('葡萄','草莓','備用','季節、禮盒、價格、清洗、產地','季節與價格會變，先保留學生的生活經驗。'),
 ('礦泉水','運動飲料','備用','瓶裝、便利商店、運動、價格、宣傳','可談包裝、品牌與需求。'),
 ('白吐司','饅頭','備用','早餐、保存、超市或店家、大量製作','可談工廠與小店都可能使用機械和分工。'),
 ('冰淇淋','冰棒','備用','冷凍、超商、口味、季節、包裝','冷鏈與全年供應的關係比猜成分更適合收束。'),
]

# All concept cards start without connectors; positions do not encode a correct answer.
LABELS = ['大量生產','全年容易買到','品牌與廣告','耗用能源與資源',
          '規格一致','農民與工人\n收入受到影響','加工與包裝','價格與選擇\n受到影響',
          '跨國採購','保存更久','機械與分工','我們習慣的口味',
          '追求利潤','外觀不合格的食物\n可能被挑掉','冷藏與運輸','單位成本\n可能降低']
mx = ET.Element('mxGraphModel', dx='1400', dy='1000', grid='1', gridSize='10', guides='1',
                tooltips='1', connect='1', arrows='1', fold='1', page='0', pageScale='1',
                pageWidth='1600', pageHeight='1100', background='#fffdf6')
root = ET.SubElement(mx,'root'); ET.SubElement(root,'mxCell',id='0'); ET.SubElement(root,'mxCell',id='1',parent='0')
def cell(id, text, x,y,w,h, style):
    c=ET.SubElement(root,'mxCell',id=id,value=text,style=style,vertex='1',parent='1')
    ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
plain='text;html=0;strokeColor=none;fillColor=none;fontFamily=Arial;fontColor=#183f36;whiteSpace=wrap;'
cell('title','食物關係圖：我們這一組的解釋',50,20,1400,55,plain+'fontSize=34;fontStyle=1;align=left;')
cell('identity','班級：＿＿＿＿　組別：＿＿＿＿　日期：＿＿＿＿',50,80,1400,40,plain+'fontSize=20;align=left;')
cell('instructions','選至少 8 張卡，連至少 6 條線。在線上寫「如何影響」。補一張自己的卡，並標出一條「可能／待查」的關係。',50,130,1420,65,plain+'fontSize=21;align=left;')
for i,label in enumerate(LABELS):
    x=60+(i%4)*370; y=230+(i//4)*175
    cell(f'concept-{i+1}',label,x,y,265,100,'rounded=1;whiteSpace=wrap;html=0;fillColor=#f4eddd;strokeColor=#3c8176;strokeWidth=2;fontColor=#183f36;fontFamily=Arial;fontSize=24;spacing=12;')
for i in range(2):
    cell(f'own-{i+1}','我們補充的卡\n（雙擊改寫）',60+i*370,955,265,100,'rounded=1;whiteSpace=wrap;html=0;fillColor=#fff1da;strokeColor=#c88023;dashed=1;fontSize=22;fontColor=#183f36;fontFamily=Arial;')
cell('reflection','這張圖讓我們開始注意到：\n（可以寫一位以前沒注意到的人）',810,945,620,125,plain+'fontSize=22;align=left;verticalAlign=top;')
model=ET.tostring(mx,encoding='unicode')
file=ET.Element('mxfile',host='app.diagrams.net',type='device',version='29.0.0')
diagram=ET.SubElement(file,'diagram',id='food-relationships',name='學生關係圖'); diagram.append(mx)
xml=ET.tostring(file,encoding='unicode')
(HERE/'food-relationships.drawio').write_text(xml)
compressor=zlib.compressobj(wbits=-15)
compressed=compressor.compress(urllib.parse.quote(model,safe="~()*!.'-").encode())+compressor.flush()
raw=urllib.parse.quote(base64.b64encode(compressed).decode(),safe='')
EDIT='https://app.diagrams.net/?lang=zh-tw&mode=device&tr=0&title=永續小食堂_第__組.drawio#R'+raw

slides=[]
def slide(title,body='',notes='',theme='cream',section='第一節',cls=''):
    slides.append(dict(title=title,body=body,notes=notes,theme=theme,section=section,cls=cls))
def p(t,cls=''): return f'<p class="{cls}">{t}</p>'
def rows(items): return '<ul class="rows">'+''.join(f'<li>{x}</li>' for x in items)+'</ul>'
def cols(a,b): return f'<div class="columns"><div>{a}</div><div>{b}</div></div>'
def timer(seconds,label): return f'<div class="timer" data-seconds="{seconds}"><output>{seconds//60:02d}:00</output><button data-timer="toggle">開始計時</button><button data-timer="reset">重設</button><span>{label}</span></div>'

slide('吃一口，<br>牽動什麼？',p('永續小食堂　2026.09.10','date')+p('先玩一場，再把食物背後的關係連起來。','lead'),
      '兩節各 50 分鐘，中間休息不計入。情意目標：願意留意食物細節、看見背後的人、對自己的選擇產生好奇。今天不要求背九項界限。', 'forest',cls='cover')
slide('你喜歡的食物，<br>明年還能一樣嗎？',p('一樣容易買到？一樣的價格？一樣的味道？','lead'),
      '0–2 分鐘。請兩位學生說喜歡的食物。接受生活回答，不要求環境術語。不要讓開場變災難測驗。','cream')
slide('地球也有安全範圍',f'<div class="pb-layout"><div><p class="big-number">7<span>／9</span></p><p>2025 年評估<br>七項界限已越界</p><p class="small">壓力持續累積，<br>生活更難維持穩定。<br>減少壓力，仍然有意義。</p></div><figure><img src="assets/planetary-boundaries-2025.jpg" alt="2025 年九項地球界限原圖，七項已越界"><figcaption>Azote for Stockholm Resilience Centre, based on Sakschewski and Caesar et al. 2025 · CC BY-NC-ND 3.0</figcaption></figure></div>',
      f'2–5 分鐘。這是一張全球健檢圖，不是末日倒數。只指土地、水、生態、氣候幾個學生認得的面向。越界不等於跨線當下全部崩潰，2025 評估年也不等於首次越界年。來源：{PB}',cls='pb-slide')
slide('一份食物，會用到什麼？',rows(['種植與飼養：土地、水、肥料與飼料','加工與運送：設備、能源與包裝','生態也受影響：棲地、土壤與水中的生命']),
      f'5–7 分鐘。請學生把剛才說的食物放進來。研究指出食物系統在土地、淡水、生態與氮磷等壓力中扮演重要角色。避免宣稱所有不永續都由食物造成。來源：{FOOD}')
slide('今天的玩法',rows(['第一節：食物版「誰是臥底」','把遊戲中說出的描述留下來','第二節：做出我們自己的食物關係圖']),
      '7 分鐘，約 30 秒。把學術詞留到學生已有生活線索之後。','forest')
slide('誰是臥底',cols('<p class="big-number">10<span>人</span></p><p>五組各派兩人<br>每輪換人上場</p>','<p class="big-number">8<span>＋</span>2</p><p>八人拿相同食物<br>兩人拿另一種食物</p>'),
      '7–9 分鐘。每人只看自己的卡，不知道自己是平民或臥底。老師發紙卡，參賽者依 1–10 號就座。教師用卡在 teacher.html，切勿投影。每組兩人不必相鄰。')
slide('每個人說一句',rows(['輪流描述，不能直接說出名稱或諧音','先想在哪裡遇到它、怎麼吃、誰會買','聽完一圈，參賽者同時指認可疑的人']),
      '9–11 分鐘。建議第一圈先講生活情境，第二圈再談外觀口感；不是禁說特徵。每人約 10 秒，不重複。最高票出局並公布身分，不公布食物。平票只讓平票者各補一句再重投；再平票本次無人出局。')
slide('台下也有任務',rows(['記下兩句參賽者的原話','圈一句你想追問的描述','想一想：這句話來自觀察，還是印象？']),
      '11–12 分鐘。每組選記錄員與追問員，其餘同學協助聽。觀眾不提示答案、不投票。沒上場的人下一輪優先，不淘汰整個小組。')
slide('先試一圈',p('老師示範：描述「鉛筆」','lead')+rows(['我通常在學校遇到它。','用一段時間後，長度會改變。']),
      '12–15 分鐘。用文具示範「描述而不報答案」，不提前暴露正式食物題目。確認 10 秒節奏及同時投票。')
for i in range(3):
    slide(f'第 {i+1} 輪',p('五組各派兩位新參賽者','lead')+p('一句描述，留下線索。')+timer(480,'每人約 10 秒；每輪最多兩次票決'),
          f'{15+i*8}–{23+i*8} 分鐘。建議題目：{PAIRS[i][0]}／{PAIRS[i][1]}。發卡約 1 分鐘，第一圈描述與投票約 3 分鐘，第二圈約 3 分鐘，揭曉與收卡 1 分鐘。兩次票決內兩名臥底都出局，平民勝；第二次票決後仍有臥底留場，臥底勝。這是配合課堂節奏的限時版。', 'teal')
slide('剛才，大家怎麼描述食物？','<div class="live-board">'+''.join(f'<label>第 {i} 組<textarea data-save="group-{i}" placeholder="記下一句原話……" aria-label="第 {i} 組原話"></textarea></label>' for i in range(1,6))+'</div>',
      '39–43 分鐘。每組報一句，教師直接輸入或寫黑板。本頁在同一台瀏覽器自動保留，不會上傳。只收錄真的出現的話。若詞彙都停在顏色口感，補問「在哪買、全年都有嗎、為什麼這樣包裝」，不要假裝是學生自己說過。',cls='board-slide')
slide('這些描述，藏著新的問題',rows(['「一年四季都有」：是怎麼做到的？','「每次味道差不多」：誰在維持？','「我覺得很健康」：這個印象從哪裡來？']),
      '43–48 分鐘。這三句是備用例句，不代表學生剛才真的說過。優先使用上一張的實際原話。只挑兩句往下追，不急著做資本主義的結論。')
slide('等一下，我們來找<br>食物背後的人與做法',p('留下你最想追問的一句話。','lead'),
      '48–50 分鐘。請各組留下一個問題。休息後再進入基本概念。','forest')
slide('一份雞塊，<br>很多人的工作', '<div class="chain"><span>飼養</span><b>→</b><span>加工</span><b>→</b><span>運送</span><b>→</b><span>販售</span></div>'+p('每個環節，都有人決定怎麼做。','lead'),
      '第二節 0–3 分鐘。這是簡化示意，非特定品牌的供應鏈調查。問誰在飼養、誰在工廠、誰開車、誰站櫃台。讓人先出場，再命名制度。','cream','第二節')
slide('食品工業化',p('把食物大量、穩定地做出來。','lead')+rows(['機械與分工','規格與流程','加工、保存與運輸']),
      '3–5 分鐘。工業化是生產組織與技術的變化，工廠之外也可能有機械化與分工。它不等於有毒、不自然或一定不好。這是課堂簡化定義。','forest','第二節')
slide('為什麼長得這麼像？',cols('<h3>一致的規格</h3><p>大小、外觀、份量<br>比較容易包裝與販售</p>','<h3>接著想</h3><p>不符合規格的食物，<br>會到哪裡去？</p>'),
      '5–7 分鐘。可能被加工、轉售、捐贈或丟棄，不能預設全都浪費。問學生是否看過外型不好看但能吃的食物。','cream','第二節')
slide('為什麼可以放這麼久？',cols('<h3>加工與保存</h3><p>冷藏、冷凍、乾燥、包裝<br>讓食物比較方便保存</p>','<h3>接著想</h3><p>它省下什麼？<br>又需要什麼？</p>'),
      '7–9 分鐘。保存可能減少腐敗，也會耗能或使用包材。效益與成本依食品和做法不同。豆漿、優格也是加工食品。請避免加工＝不健康的二分。','cream','第二節')
slide('資本主義下的食物供應',p('企業投入資金，透過市場販售，並追求利潤。','lead')+p('成本、售價、銷量，都會影響決定。'),
      '9–11 分鐘。這是本節使用的簡化描述。工業化著重怎麼大量生產；資本主義的討論著重資金、所有權、市場與利潤如何影響決定。兩者常交織，卻不是同義詞。','forest','第二節')
slide('賣得出去，會影響怎麼做',rows(['廣告與品牌，讓商品被看見','採購與定價，影響成本和收入','消費者的預算與習慣，也會回頭影響市場']),
      '11–13 分鐘。問學生有沒有因包裝、品牌或促銷選過食物，不點名羞辱。企業追求利潤能帶來創新與供應，也可能形成壓低成本的壓力；具體後果需看制度與案例。','cream','第二節')
slide('方便的同時，還有什麼？',cols('<h3>我們得到的</h3><p>容易買到<br>保存更久<br>有時比較便宜</p>','<h3>值得追問的</h3><p>用了多少資源？<br>工作的人過得如何？<br>哪些成本沒寫在標價上？</p>'),
      '13–15 分鐘。不要要學生反對所有便利，而是看見便利依靠什麼。進口不必然比較不永續、加工不必然不健康、本地不保證勞動公平。今天先建立追問的習慣。','paper','第二節')
slide('一條線，也是一句解釋', '<div class="example-link"><span>下雨</span><div><small>雨水落在地面</small><b>→</b></div><span>地面潮濕</span></div>'+p('箭頭指向影響；線上的字說明理由。'),
      '15–17 分鐘。用生活例子示範操作，避免先畫完學生的食物答案。這只是可能因果：地面濕也可能來自清洗，遮雨處則未必濕。示範可寫「可能」或加條件。','cream','連線活動')
slide('我們這一組的食物關係圖',rows(['選至少 8 張卡，連出至少 6 條線','每條線寫一句「如何影響」','補一張自己的卡，標一條「可能／待查」']),
      '17–18 分鐘。16 張預置卡不必全用，也不要求唯一正解。允許移動、改寫、刪除卡片。作品含至少一個便利與一個代價，透過文字說明而非正負符號競賽。','forest','連線活動')
slide('卡片已放好，關係由你們決定',p('一組一台電腦，先輪流說，再動手連。','lead')+f'<p><a class="action-link" href="student.html" target="_blank" rel="noopener">開啟學生任務與模板 ↗</a></p>'+p('連線的人、解釋的人、追問的人，都要參與。'),
      '18–19 分鐘。student.html 是可給學生的連結，沒有遊戲答案。各組自行開模板就是各自的副本。這次採一組一台，避免首次授權與協作設定耗掉課堂時間。','cream','連線活動')
slide('draw.io 三個動作',rows(['拖曳卡片，安排你們的想法','從卡片邊緣的小箭頭，拖到另一張卡','雙擊連線，寫上原因或「可能／待查」']),
      '19–20 分鐘。使用繁中介面。先做一條再刪除給學生看。誤操作可 Ctrl+Z（Mac 為 Command+Z）。滑鼠移到圖形邊緣才會出現連線箭頭。','paper','連線活動')
slide('開始連線',p('每畫一條，先問組員：<br>「你覺得這條線說得通嗎？」','lead')+timer(1200,'完成後，挑一條最想分享的線'),
      '20–40 分鐘。第 8 分鐘巡視：至少先完成兩條。時間落後可先用 6 張卡、4 條線，再補到作業要求。教師問理由與證據，不給整張標準答案。','teal','連線活動')
slide('卡住的時候',rows(['它讓什麼變得比較容易？','誰可能受益？誰可能多付出？','這一定會發生嗎？還要哪些條件？']),
      '活動中備用提示頁，可不播放。可用的連線語：讓……比較容易、需要、可能增加、可能減少、取決於。不要要求背術語。','cream','連線活動')
slide('看看別組的一條線',p('「我理解你們的意思是……」','lead')+p('「我還想問的是……」','lead'),
      '40–47 分鐘。五組各用約 45 秒說一條線，另一組留一句追問，或採相鄰組互看。提問不以抓錯為目的。','cream','分享')
slide('今天的作業',rows(['圖上填班級、組別與日期','下載 .drawio 原檔，再匯出 PNG 圖片','兩個檔案一起交到老師指定的作業']),
      '47–48 分鐘。檔名建議：班級_第X組_食物關係圖。學生頁有完整存檔步驟。使用者尚未提供 Classroom 作業連結，不捏造繳交位置或截止時間。成果以本組解釋為主，評量依觀察、連結與提問。','forest','收尾')
slide('今天，我開始注意到……',p('一位以前沒注意到的人，<br>或一件以前沒想過的事。','lead')+p('還有，我想再問……'),
      '48–50 分鐘。一人一句，可口頭或寫在關係圖旁。情意目標看見人、產生好奇，不要求學生宣誓改吃某種食物。','cream','收尾')
slide('下週：一杯咖啡，<br>誰分到多少？',p('9/17　咖啡小農的生活','lead'),
      '依使用者 Word 大綱銜接 9/17 的公平問題。不是今天就要講完的內容。','forest','下週')

def htmlpage(title,body,extra='',style='lesson.css'):
    return f'<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><link rel="stylesheet" href="{style}"><link rel="icon" href="../../favicon.svg">{extra}</head><body>{body}</body></html>'
sections=[]
for i,s in enumerate(slides):
    sections.append(f'<section class="slide {s["theme"]} {s["cls"]}" data-section="{s["section"]}" aria-hidden="{str(i!=0).lower()}"><div class="slide-inner"><h{1 if i==0 else 2}>{s["title"]}</h{1 if i==0 else 2}>{s["body"]}</div><aside class="speaker-notes">{s["notes"]}</aside></section>')
deck='''<main id="deck" aria-label="永續小食堂投影片">'''+''.join(sections)+'''</main>
<nav class="controls" aria-label="投影片導覽"><a href="teacher.html" target="_blank" rel="noopener">教師備課</a><button id="prev" aria-label="上一張">←</button><span id="counter"></span><button id="next" aria-label="下一張">→</button><button id="notes-button">備註 N</button><button id="fullscreen">全螢幕 F</button><button id="overview">目錄</button></nav>
<aside id="notes-panel" hidden><button id="close-notes">關閉</button><h3>講者備註</h3><p id="notes-copy"></p><p class="small">本面板會出現在投影畫面，遊戲時請先關閉。</p></aside>
<dialog id="toc"><h2>投影片目錄</h2><div id="toc-links"></div><button id="close-toc">關閉</button></dialog><script src="lesson.js"></script>'''
(HERE/'index.html').write_text(htmlpage('食物背後的關係｜永續小食堂',deck))

student=f'''<main class="document"><p class="eyebrow">永續小食堂　9/10</p><h1>我們這一組的食物關係圖</h1><p class="intro">卡片已經放好。你們決定哪些有關、如何影響，也可以改寫或補充。</p>
<div class="actions"><a class="primary" href="{escape(EDIT,quote=True)}" target="_blank" rel="noopener">開啟我們的模板 ↗</a><a href="food-relationships.drawio" download>下載模板檔</a><button onclick="window.print()">列印任務單</button></div>
<p>免費，不必登入。一組一台電腦，每組開啟的是自己的副本。</p>
<h2>今天要完成什麼</h2><ol><li>從 16 張卡裡選至少 <strong>8 張</strong>，連至少 <strong>6 條線</strong>。</li><li>每條線寫一句說明，讓別人知道你們認為它們如何相關。</li><li>至少呈現一個便利與一個可能的代價，補一張你們自己的卡。</li><li>標出一條「可能／待查」的關係。可以改寫卡片，沒有唯一的排法。</li></ol>
<h2>三個動作就能開始</h2><ol><li>拖曳卡片，安排位置。</li><li>把滑鼠移到卡片邊緣，從小箭頭拖到另一張卡。</li><li>雙擊連線，輸入「可能增加……」「讓……比較容易」等說明。</li></ol><p>卡片文字也可以雙擊改寫。誤操作用 Ctrl＋Z，Mac 用 Command＋Z。畫面太大或太小，用左上角的百分比調整縮放。</p>
<h2>我們可以這樣分工</h2><p>操作的人畫線，解釋的人先說理由，追問的人問「一定會這樣嗎」。其他組員提供例子與補充。每完成兩條線，換人操作。</p>
<h2>存好再繳交</h2><ol><li>在圖上填班級、組別與日期。</li><li>選「檔案」→「另存新檔」，把「位置」改成<strong>「下載」</strong>，再按「儲存」。檔名用 <strong>班級_第X組_食物關係圖.drawio</strong>。「裝置」也可使用；不要保留預設的 Google 雲端硬碟，除非你打算登入。</li><li>再選「檔案」→「匯出為」→「PNG」。保留整張圖，匯出到裝置。</li><li>把 <strong>.drawio 與 PNG 兩個檔案</strong>交到老師指定的作業。截止時間依老師課堂說明。</li></ol>
<p>關掉分頁前，先確認下載資料夾裡真的有檔案。重新開啟原本的模板連結會得到空白副本；繼續編輯請開自己存好的 .drawio 檔。</p>
<h2>完成後，互相聽一條線</h2><p>「我理解你們的意思是……」<br>「我還想問的是……」</p><h2>今天，我開始注意到</h2><div class="writing-space">一位以前沒注意到的人，或一件以前沒想過的事：</div>
<h2>如果模板沒有自動開啟</h2><p>先下載模板，再到 <a href="https://app.diagrams.net/?lang=zh-tw&mode=device" target="_blank" rel="noopener">draw.io 繁中編輯器</a>，選「檔案」→「從...開啟」→「裝置」，選剛下載的 .drawio。也可以把檔案拖進畫布。</p>
<footer><a href="https://www.drawio.com/docs/manual/connectors/">連線官方說明</a>　<a href="https://www.drawio.com/docs/manual/export/export-diagram/">匯出官方說明</a></footer></main>'''
(HERE/'student.html').write_text(htmlpage('食物關係圖｜學生任務',student,style='handout.css'))

guide='''# 9/10 永續小食堂教師指南

本課依 115-1 課程大綱第二週設計。兩節各 50 分鐘，以高一學生的觀察、好奇與理解他人為目標。9/17 的咖啡小農與公平問題留作下一週銜接。

## 明天課前五分鐘

1. 開啟投影片 index.html，先測全螢幕及方向鍵。按 N 會顯示含遊戲答案的備註，投影遊戲時務必關閉。
2. 列印 cards.pdf 的三頁卡片，剪成每輪十張，依 1–10 號發放。卡上不寫身分，老師保留對照表。
3. 五組各準備一張紙記錄原話，第二節一組一台 Chromebook 或電腦。
4. 把 student.html 的連結貼到學生取得教材的位置；設定原有 Classroom 的作業，收 .drawio 與 PNG。此教材沒有替老師建立或發布 Classroom 作業。
5. 網路臨時不通時，投影片可離線開啟；把 template-print.pdf 以 A3 橫式印給五組，用筆連線，拍照繳交。

## 情意目標與觀察

- 願意仔細描述熟悉食物，留意原本忽略的特徵。
- 開始關心食物背後的人及他們付出的工作。
- 容許不同解釋，願意提出一個還想查證的問題。

不以背出九項界限、反對加工食品或表態反對資本主義作為達標條件。

## 第一節 50 分鐘

| 分鐘 | 流程 | 教師工作 |
|---|---|---|
| 0–7 | 喜歡的食物、地球界限、食物的環境壓力 | 只用一張官方圖，不逐項講授或災難倒數 |
| 7–12 | 遊戲規則與旁觀任務 | 五組各派兩人，觀眾記原話 |
| 12–15 | 文具示範 | 示範一句描述與同時投票，不洩漏食物題目 |
| 15–39 | 三輪各 8 分鐘 | 主題依序奇異果／蘋果、鮮奶／豆漿、泡麵／冷凍水餃 |
| 39–48 | 收集原話與追問 | 原話先記錄，再區分觀察、印象與待查問題 |
| 48–50 | 留下一個問題 | 下節接生產與供應的做法 |

## 遊戲的課堂時間版

- 每輪 10 人，8 張同一食物、2 張另一食物。參賽者只看自己的詞，不知道自己的身分。
- 五組各派兩人，按號碼發卡；下一輪換人，未上場者優先。若班級超過 30 人，未輪到者下次優先。
- 一圈每人約 10 秒，說一句不重複的描述。不報名稱、諧音，也不直接指認兩個候選詞。
- 建議第一圈生活情境，第二圈外觀口感，避免第一句過度具體就讓遊戲結束；這是引導，不是禁止觀察特徵。
- 每圈描述後，存活參賽者同時投票，最高票出局。公布出局者的身分，不公布食物。觀眾與出局者不提示。
- 平票者各補一句，再投一次；仍平票本次無人出局。
- 兩次票決內兩名臥底皆出局，平民勝；第二次票決後仍有臥底留場，臥底勝。8 分鐘到即完成當次投票並揭曉。這是課堂限時版，先把勝負說清楚。
- 不做跨組輸贏積分，避免兩名臥底落在哪組影響公平。鼓勵描述與記錄貢獻即可。
- 一輪約：發卡 1 分鐘、首圈描述與投票 3 分鐘、第二圈 3 分鐘、揭曉與換人 1 分鐘。

## 題庫與收束方向

題目可交換哪一詞為多數。主題卡目前使用下表前三組。最後一欄是教師提問方向，不保證學生自然說出。

| 食物 A／食物 B | 使用時機 | 可能描述 | 教師留意 |
|---|---|---|---|
'''
guide+='\n'.join(f'| {a}／{b} | {stage} | {clues} | {note} |' for a,b,stage,clues,note in PAIRS)
guide+='''

## 用學生的話搭橋，而不是替學生發言

先問「你在哪裡遇到它、怎麼知道」，再把線索往供應方式連。不把「進口、昂貴、健康」直接當成工業化或資本主義的證據。

| 若真的聽到這句話 | 可追問 | 可連到的概念 |
|---|---|---|
| 一年四季都有 | 誰種、在哪種、如何保存運送？ | 採購、保存、運輸 |
| 每次吃都差不多 | 誰訂大小、配方與製程？ | 規格與分工 |
| 很方便、很快 | 哪些工作先由別人做了？ | 加工、備餐時間與勞動 |
| 很便宜／很貴 | 跟誰比、在哪買、是什麼時候？ | 成本、定價與預算 |
| 感覺很健康 | 來自包裝、家人、廣告，還是讀過資料？ | 健康印象與品牌 |

如果大家只說顏色、形狀，肯定其觀察，再補問購買與食用情境。不必強迫每一句都推到資本主義。

## 第二節 50 分鐘

| 分鐘 | 流程 | 教師工作 |
|---|---|---|
| 0–15 | 供應鏈、工業化、企業與利潤、便利與代價 | 生活案例配短講，講到能連線就停 |
| 15–20 | 示範「下雨影響地面潮濕」、開模板 | 示範拖卡片、連線、線上加字 |
| 20–40 | 小組做關係圖 | 至少 8 張卡、6 條有說明的線、一張自增卡、一條可能／待查關係 |
| 40–47 | 分享或相鄰組互看 | 每組說一條，其他組回應一個問題 |
| 47–50 | 存檔與離堂回應 | 收原檔與 PNG；關注看見了誰、想問什麼 |

活動中每完成兩條線換人操作。時間不足先做 6 張卡與 4 條線，下課後補到完整要求，繳交時間由老師決定。

## 概念講到這個程度即可

- **工業化**：透過機械、分工、標準流程、加工與物流，大量而穩定地供應食物。可能帶來便利、保存和成本效益，也可能伴隨資源使用與生態壓力。
- **資本主義下的供應**：企業投入資金、透過市場販售並追求利潤，成本、定價、銷量及競爭會影響生產和採購。工業化與資本主義常交織，但不是同義詞。
- **外部成本的生活說法**：有些代價沒寫在標價上，卻由環境、工作者或社會承擔。不要預設每種情況都一樣。
- 進口未必一定比本地不永續，加工未必不健康，小店也可能有不公平勞動。以具體做法與證據比較。

## 教師可接受的連線例子

以下只作巡組追問，沒有唯一標準答案，不放進學生模板。

- 機械與分工 → 大量生產：「同一段工作可以重複完成」。
- 加工與包裝 → 保存更久：「某些做法能減少腐敗」。再問需要什麼能源或材料。
- 冷藏與運輸 → 全年容易買到：「食物可以保存或從不同地方送來」。再問產季與成本。
- 規格一致 → 外觀不合格可能被挑掉：「如果通路按外觀驗收」。強調有條件，不一定丟掉。
- 品牌與廣告 → 我們習慣的口味：「可能讓某些口味被更多人認識」。再問家人、文化也有影響嗎。
- 追求利潤 → 農民與工人收入受到影響：「可能形成壓低採購與工資的壓力，也可能因銷量而增加工作」。要看議價、制度與個案。

## 評量建議

以完成／持續發展的回饋為主。若需給分，可採三項各 0–2 分：

1. 觀察：有具體食物描述或生活例子。
2. 連結：能用自己的話解釋關係，知道有些需要條件。
3. 好奇與理解：看見一位供應鏈中的人，或提出真正在意、想再查的問題。

連線數與檔案只是作業格式檢查，不把術語數、圖面美觀或立場一致當成情意目標。

## 免費網頁工具的選擇

- **draw.io／diagrams.net：本次主選。** 官方列免費、不用註冊；自由節點與連線、.drawio 原檔、PNG 匯出適合本作業。這次採裝置存檔，一組一台，避免雲端授權設定。若之後要多人同步，另評估 Google Drive／OneDrive 整合。
- **Excalidraw：備選。** 開源網頁白板適合自由連線與協作，但自動排版不是本次重點。官方專案：https://github.com/excalidraw/excalidraw 。本次未實測多人協作。
- **Coggle：備選。** 免費方案有私有圖數量等限制，較適合樹狀發想；本次需要多對多關係，因此不作首選。官方：https://coggle.it/ 。

## 資源與事實依據

- 課程日期與主題：使用者提供的《115-1永續小食堂課程大綱.docx》。僅讀取，未修改未規劃週次。
- 地球界限與原圖：https://www.stockholmresilience.org/research/planetary-boundaries.html 。採 2025 評估，圖為 CC BY-NC-ND 3.0，保留原圖與署名。
- 食物系統與環境壓力：https://www.nature.com/articles/s43016-025-01252-6 。注意 food system boundaries 與全球 planetary boundaries 不同，投影片不混用九項食物部門界限的數字。
- draw.io 免費使用：https://www.drawio.com/ 。
- 連線與加字：https://www.drawio.com/docs/manual/connectors/ 。
- 儲存與匯出：https://www.drawio.com/docs/manual/export/export-diagram/ 。
- 模板網址格式：https://www.drawio.com/docs/reference/supported-location-hash-properties/ 。

已在桌面瀏覽器檢查 32 張投影片與互動；PDF 為投影片 32 頁、A4 食物卡 3 頁、A3 關係圖 1 頁。學生模板以 draw.io 繁中介面實測載入、連線加字與原檔下載。

教材為教師備課草稿，請依班級情況調整。由 Codex 協助製作，2026-09-09。
'''
(HERE/'teacher-guide.md').write_text(guide)

# Minimal Markdown conversion for this controlled guide, not a general parser.
def render_md(s):
    def inline(t):
        import re
        t=escape(t); t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
        return t
    result=[]; table=False
    for line in s.splitlines():
        if line.startswith('|'):
            if set(line.replace('|','').replace('-','').replace(' ',''))==set(): continue
            cells=line.strip('|').split('|')
            if not table: result.append('<div class="table-scroll"><table>'); table=True
            result.append('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in cells)+'</tr>'); continue
        if table: result.append('</table></div>'); table=False
        if line.startswith('# '): result.append('<h1>'+inline(line[2:])+'</h1>')
        elif line.startswith('## '): result.append('<h2>'+inline(line[3:])+'</h2>')
        elif line: result.append('<p>'+inline(line)+'</p>')
    if table: result.append('</table></div>')
    return ''.join(result)
links='<div class="actions"><a class="primary" href="index.html">上課投影片</a><a href="student.html">學生任務</a><a href="cards.pdf" download>遊戲卡 PDF（A4 三頁）</a><a href="template-print.pdf" download>紙本關係圖 PDF（A3）</a><a href="slides.pdf" download>投影片 PDF</a><a href="lesson-pack.zip" download>離線教材包 ZIP</a></div>'
(HERE/'teacher.html').write_text(htmlpage('9/10 教師備課｜永續小食堂','<main class="document">'+links+render_md(guide)+'</main>',style='handout.css'))

# Seat numbers are for distribution, not a public identity cue.
spy_seats=[{3,8},{2,7},{4,9}]
cards='<div class="print-toolbar"><h1>教師用食物卡</h1><p>只印本頁三張 A4，剪成三輪各十張。卡片不顯示身分，請勿投影。</p><p>教師對照：第一輪 3、8 號臥底；第二輪 2、7 號；第三輪 4、9 號。每輪換人上場。</p><button onclick="window.print()">列印三輪卡片</button><a href="teacher.html">回教師指南</a></div>'
for r,(a,b,*_) in enumerate(PAIRS[:3]):
    cards+='<section class="card-sheet">'
    for seat in range(1,11):
        word=b if seat in spy_seats[r] else a
        cards+=f'<article class="word-card"><small>第 {r+1} 輪　{seat} 號</small><strong>{word}</strong><p>只看自己的卡<br>不要讓別人看見</p></article>'
    cards+='</section>'
(HERE/'cards.html').write_text(htmlpage('食物版誰是臥底｜教師列印卡',cards,style='handout.css'))
paper='<main class="map-paper"><h1>我們這一組的食物關係圖</h1><p>班級：＿＿＿＿　組別：＿＿＿＿　日期：＿＿＿＿</p><p>選至少 8 張卡，連至少 6 條線。每條線寫解釋。補一張自己的卡，標出一條「可能／待查」。</p><div class="paper-canvas">'
for i,label in enumerate(LABELS):
    paper+=f'<div class="paper-node" style="left:{3+(i%4)*25}%;top:{3+(i//4)*22}%">{escape(label).replace(chr(10),"<br>")}</div>'
paper+='</div><p>我們補充的卡：＿＿＿＿＿＿＿＿　今天開始注意到的人或事：＿＿＿＿＿＿＿＿</p></main>'
(HERE/'template-print.html').write_text(htmlpage('食物關係圖｜紙本備援',paper,'<style>@page{size:A3 landscape;margin:12mm}</style>',style='handout.css'))
(HERE/'slide-notes.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2))
print(f'Built {len(slides)} slides, {len(PAIRS)} question pairs, 30 word cards, and 16 unconnected concept cards.')
