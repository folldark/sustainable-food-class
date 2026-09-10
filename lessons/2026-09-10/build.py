"""Build the self-contained lesson and editable draw.io template. Python stdlib only."""
from pathlib import Path
from html import escape
import base64, json, urllib.parse, zlib
import xml.etree.ElementTree as ET

HERE = Path(__file__).parent
BASE = 'https://folldark.github.io/sustainable-food-class/lessons/2026-09-10/'
PB = 'https://www.stockholmresilience.org/research/planetary-boundaries.html'
FOOD = 'https://www.nature.com/articles/s43016-025-01252-6'
CDCE = 'https://archive.cdc.gov/www_cdc_gov/ecoli/2018/o157h7-04-18/index.html'
FDAE = 'https://www.fda.gov/food/outbreaks-foodborne-illness/environmental-assessment-factors-potentially-contributing-contamination-romaine-lettuce-implicated'
GULF = 'https://coastalscience.noaa.gov/news/below-average-summer-2025-dead-zone-measured-in-gulf/'
PAIRS = [
 ('咖啡','紅茶','第一輪','早餐店、便利商店、提神印象、品牌、產地','兩者都靠進口。先收生活描述；產地與分工留到第二節講述時再接。'),
 ('麻糬','蜂蜜蛋糕','第二輪','伴手禮、包裝、保存期限、店家、甜度','加工程度都高，手工與工廠都可能。不要把包裝精美直接當成工廠製造。'),
 ('泡麵','冷凍水餃','第三輪','方便、保存、煮食時間、超市、包裝','加工帶來保存與便利，也可能使用能源與包材。不要把加工直接等同有害。'),
 ('冰淇淋','優格','備用','冷藏或冷凍、乳製品、點心、營養宣稱','同樣用牛奶做，加工方向不同。健康印象常來自廣告而非成分。'),
 ('火腿','魚板','備用','早餐、火鍋、切片、保存、超市','都是重組加工食品，適合追問「原形食物」的界線在哪裡。'),
 ('果汁','汽水','備用','便利商店、瓶罐、甜度、廣告、宣稱','還原果汁也是加工品。適合談健康宣稱與創造需求。'),
 ('洋芋片','爆米花','備用','零食、看電影、包裝、口味、超商','同樣是澱粉類零食，加工與調味程度不同。'),
 ('巧克力','牛軋糖','備用','禮盒、節日、品牌、進口、甜度','可可要進口且分工很細；節日也會創造需求。'),
 ('罐頭玉米','冷凍毛豆','備用','超市、保存、料理、包裝、產地','兩種不同的保存技術，適合接「為什麼可以放這麼久」。'),
 ('鮮奶','豆漿','備用','早餐、紙盒、冰箱、營養印象、品牌','兩者都有不同加工與包裝。健康不能只憑品名或廣告判斷。'),
 ('奇異果','蘋果','備用','水果、買的地方、產地標籤、價格印象','進口、昂貴都是待查的描述。不要把某一種水果直接等同進口。'),
 ('白吐司','饅頭','備用','早餐、保存、超市或店家、大量製作','工廠與小店都可能使用機械和分工。'),
 ('漢堡','三明治','備用','連鎖店、早餐、外帶、價格、規格','適合追問不同店家如何維持相似口味。'),
 ('雞塊','雞排','備用','外帶、油炸、冷凍、連鎖店、大小','可談規格與加工，不把店型當成食品安全證據。'),
 ('布丁','奶酪','備用','杯裝、冷藏、點心、甜點店或超商','外觀相近、原料不同，適合練習描述而不是猜名稱。'),
 ('葡萄','草莓','備用','季節、禮盒、價格、清洗、產地','季節與價格會變，先保留學生的生活經驗。'),
 ('礦泉水','運動飲料','備用','瓶裝、便利商店、運動、價格、宣傳','可談包裝、品牌與需求。'),
 ('餅乾','洋芋片','備用','零食、包裝、口味、廣告、超商','廣告可能讓人認識產品，也可能影響購買慾望。'),
 ('冰淇淋','冰棒','備用','冷凍、超商、口味、季節、包裝','冷鏈與全年供應的關係，比猜成分更適合收束。'),
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

slide('吃一口，<br>牽動什麼？',p('永續小食堂　2026.09.10','date')+p('先玩一場，再看看食物背後發生了什麼事。','lead'),
      '兩節各 50 分鐘，中間休息不計入。第一節玩誰是臥底，第二節用講述帶食品工業化與消費社會，收在兩個真實案例。情意目標：願意留意食物細節、看見背後的人、對自己的選擇產生好奇。今天不要求背九項界限。', 'forest',cls='cover')
slide('你喜歡的食物，<br>明年還能一樣嗎？',p('一樣容易買到？一樣的價格？一樣的味道？','lead'),
      '0–2 分鐘。請兩位學生說喜歡的食物。接受生活回答，不要求環境術語。不要讓開場變災難測驗。','cream')
slide('地球也有安全範圍',f'<div class="pb-layout"><div><p class="big-number">7<span>／9</span></p><p>2025 年評估<br>七項界限已越界</p><p class="small">壓力持續累積，<br>生活更難維持穩定。<br>減少壓力，仍然有意義。</p></div><figure><img src="assets/planetary-boundaries-2025.jpg" alt="2025 年九項地球界限原圖，七項已越界"><figcaption>Azote for Stockholm Resilience Centre, based on Sakschewski and Caesar et al. 2025 · CC BY-NC-ND 3.0</figcaption></figure></div>',
      f'2–5 分鐘。這是一張全球健檢圖，不是末日倒數。只指土地、水、生態、氣候幾個學生認得的面向。越界不等於跨線當下全部崩潰，2025 評估年也不等於首次越界年。來源：{PB}',cls='pb-slide')
slide('一份食物，會用到什麼？',rows(['種植與飼養：土地、水、肥料與飼料','加工與運送：設備、能源與包裝','生態也受影響：棲地、土壤與水中的生命']),
      f'5–7 分鐘。請學生把剛才說的食物放進來。研究指出食物系統在土地、淡水、生態與氮磷等壓力中扮演重要角色。避免宣稱所有不永續都由食物造成。來源：{FOOD}')
slide('今天的玩法',rows(['第一節：食物版「誰是臥底」','把遊戲中說出的描述留下來','第二節：從工業革命看食物背後的代價']),
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
slide('剛才那些描述，<br>是怎麼變成理所當然的？',p('「一年四季都有」「每次味道差不多」「很方便」。','lead')+p('這些都不是自然發生的。'),
      '第二節 0–2 分鐘。先把上一節留下的原話唸一句出來再開始。這一節主要用講述，讓學生先有基本概念；下週起才回到操作。','forest','第二節')
slide('工業革命，是一場劇變',rows(['想到工業革命，通常想到蒸汽機、工廠與都市化','但社會的每一個層面都要跟著改變，例如家庭','農業也是其中之一']),
      '2–5 分鐘。社會學把工業革命理解為整個社會結構的劇變，不只是技術更新。可問學生：家庭為什麼會跟著變？','cream','第二節')
slide('在那之前，<br>大多數人是自己食物的<span class="accent">生產者</span>',p('自己種、自己養、自己吃。','lead'),
      '5–7 分鐘。這是概略描述，各地差異很大，市集與長距離貿易也一直存在。重點是自給比例遠高於今天。','paper','第二節')
slide('然後，農業被要求做一件難事',cols('<h3>種田的人變少</h3><p>大量人口離開農村，<br>進入工廠與城市</p>','<h3>要餵的人變多</h3><p>有限的農業人力，<br>要養活大量人口</p>'),
      '7–10 分鐘。這個壓力就是後來機械、化肥、育種與集中化的動力。不要把它講成有人刻意設計的陰謀。','cream','第二節')
slide('這是一種<span class="accent">巨大的進步</span>',p('人類第一次有能力，生產出足以餵養全球人口的食物。','lead'),
      '10–12 分鐘。先把成就講清楚，再談代價；否則後面的討論會變成單純的批判。','forest','第二節')
slide('但是很諷刺',cols('<h3>有人丟掉</h3><p>食物是拿來賣的商品。<br>賣不掉、不好看的，<br>可能被丟掉</p>','<h3>有人吃不飽</h3><p>同一個時間，<br>地球上仍有很多人<br>營養不良</p>'),
      '12–14 分鐘。糧食總量夠，不等於每個人分配得到。飢餓的成因包含所得、戰爭、運輸與政策，不是只有浪費。','teal','第二節')
slide('工業化的食物體系，<br>也付出代價',rows(['環境：土地、水、能源與生態','健康：誰在承擔看不見的風險','公平：誰得到好處，誰多付出']),
      '14–16 分鐘。這三項就是開學第一堂說的三大環節。等一下兩個故事分別對應健康與環境。','forest','第二節')
slide('還有一件事：<br>工業革命帶來<span class="accent">消費社會</span>',cols('<h3>過去</h3><p>需求帶動生產。<br>有人要，才做。</p>','<h3>工業化之後</h3><p>為了讓生產線不停，<br>必須創造需求。</p>'),
      '16–19 分鐘。廣告、品牌、節日與新款式都是創造需求的手段。這不等於消費者被騙，而是需求本身也會被塑造。','cream','第二節')
slide('回到剛才的遊戲',p('你們說出口的特徵裡，<br>就有工業化生產與消費社會的痕跡。','lead'),
      '19–20 分鐘。挑一句上一節記下的原話當引子，例如「便利商店就有」「一年四季都喝得到」。','forest','第二節')
slide('例如，咖啡',rows(['台灣的消費量遠大於生產量，幾乎都靠進口','從栽種、採集、發酵、烘焙到沖煮，是高度分工的體系','台灣很晚才引入咖啡，而你們正好在「學喝咖啡」的年紀']),
      '20–23 分鐘。第一輪題目就是咖啡／紅茶，直接接學生剛才的描述。分工體系下週會再回來談誰分到多少。','cream','第二節')
slide('為什麼要「<span class="accent">學</span>」喝咖啡？',p('沒有人需要學著喝水。','lead')+p('一樣東西要先被學會欣賞，才會有人持續買它。'),
      '23–25 分鐘。可停 30 秒讓學生轉頭跟旁邊的人說：你最近開始喜歡上什麼？是誰讓你知道的？喜歡咖啡不是壞事，重點是留意習慣怎麼被建立。','teal','第二節')

slide('故事一<br>2018 年，美國的生菜',p('健康的代價，會落在誰身上？','lead'),
      '25–26 分鐘。以下是真實事件，數字以 CDC 與 FDA 的公開報告為準。','forest','故事一')
slide('那年春天，<br>有人吃了生菜之後生病','<div class="chain"><span>生菜田</span><b>→</b><span>集中清洗切分</span><b>→</b><span>混合包裝</span><b>→</b><span>全國餐廳與超市</span></div>'+p('生菜在中央工廠清洗、切分、混合包裝，再送往全國各地。'),
      '26–28 分鐘。這是簡化示意。重點是原料在中途被混合，一批貨已經不是一塊田的收成。','cream','故事一')
slide('210 個人，36 個州','<div class="pb-layout"><div><p class="big-number">210<span>人</span></p><p>感染同一株<br>大腸桿菌 O157:H7</p><p class="small">分布在 36 個州。<br>96 人住院，其中 27 人<br>出現腎衰竭。<br>5 人死亡。</p></div><figure><img src="assets/romaine-ecoli-2018-cdc-map.jpg" alt="美國地圖，顯示 2018 年蘿蔓生菜大腸桿菌疫情的各州病例數分布"><figcaption>U.S. CDC，2018 年蘿蔓生菜 E. coli O157:H7 疫情各州病例分布 · 美國聯邦政府作品</figcaption></figure></div>',
      f'28–31 分鐘。數字是 CDC 於 2018 年 6 月 28 日宣布疫情結束時的最終統計：210 例、36 州、96 人住院、27 人出現溶血性尿毒症候群、5 人死亡。發病日期從 3 月 13 日到 8 月 22 日。來源：{CDCE}','cream','故事一',cls='pb-slide')
slide('源頭指向一條灌溉渠道',cols('<h3>驗出病菌的地方</h3><p>亞利桑那州 Yuma 一段<br>約 3.5 英里的灌溉渠道</p>','<h3>渠道旁邊</h3><p>一座可容納<br>超過 10 萬頭牛的<br>大型飼養場</p>'),
      f'31–34 分鐘。務必說清楚證據強度：FDA 在飼養場的有限採樣中「沒有」驗到本次疫情的菌株，只驗到其他致病性大腸桿菌，但也沒有找到其他來源的證據。所以「飼養場是源頭」是合理推測，不是已證實的結論。牛是大腸桿菌的天然宿主。來源：{FDAE}','cream','故事一')
slide('為什麼一塊田，<br>會變成 36 個州？',rows(['一塊田的收成，會和其他農場的生菜混在一起','集中清洗、切分、包裝，一次處理大量原料','再由物流送到全國的餐廳與超市']),
      '34–36 分鐘。集中化讓成本降低、供應穩定，也讓一個污染點的影響被放大。這是同一件事的兩面。','teal','故事一')
slide('而且，追不太回來',p('FDA 追到 23 個農場、36 塊田，卻指不出唯一的那一塊。','lead')+p('出貨紀錄不完整，讓追溯變得非常困難。'),
      f'36–38 分鐘。紀錄不完整是整個供應鏈的制度問題，不是某個農民的疏忽。這也說明為什麼後來會推動可追溯性規範。來源：{FDAE}','cream','故事一')
slide('你有辦法自己檢驗嗎？',p('你買一包生菜，看不出水源，也看不出前一手是誰。','lead')+p('而在現在的社會裡，<br>你也很難不從這個體系買東西。'),
      '38–40 分鐘。本節最重要的一頁，可停 30 秒讓學生想。體系把成本壓低、效率做高，但驗證的責任落到最沒有能力驗證的人身上。不要推論成「企業都在害人」，而是問這樣的責任分配合不合理。','forest','故事一')

slide('故事二<br>密西西比河的出海口',p('環境的代價，會落在哪裡？','lead'),
      '40–41 分鐘。同樣是真實、每年都在量測的事件。','forest','故事二')
slide('每年夏天，墨西哥灣會出現一片「死區」','<div class="case-wide"><p class="facts"><b>4,402</b><span>平方英里，2025 年 7 月實測的底層缺氧範圍。<br>約 11,400 平方公里，接近台灣本島面積的三分之一。</span></p><figure><img src="assets/gulf-hypoxia-2025-map.jpg" alt="2025 年墨西哥灣底層溶氧分布圖，紅色區域為缺氧最嚴重的範圍"><figcaption>紅色代表底層溶氧低於每公升 2 毫克。圖：LSU 與 NOAA，2025 Shelfwide Cruise，2025 年 7 月 20–25 日實測</figcaption></figure></div>',
      f'41–44 分鐘。缺氧的定義是底層溶氧低於每公升 2 毫克。4,402 平方英里約 11,400 平方公里，台灣本島約 36,000 平方公里。圖上的字母是採樣測線編號，不必解釋。來源：{GULF}','cream','故事二',cls='case-slide')
slide('它是怎麼來的？','<div class="chain"><span>農田與畜牧施肥</span><b>→</b><span>河流帶走氮與磷</span><b>→</b><span>藻類大量繁殖</span><b>→</b><span>死亡分解耗盡氧氣</span></div>'+p('魚和蝦會離開這片海域。2025 年相當於 280 萬英畝的棲地暫時消失。'),
      '44–46 分鐘。營養鹽來自整個密西西比河流域的農地與都市，不是單一農場。玉米與大豆很大一部分是拿去餵牲畜的，和上一個故事的飼養場是同一套體系。','teal','故事二')
slide('這不是今年才發生','<div class="pb-layout"><div><p class="big-number">40<span>年</span></p><p>1985 年開始<br>每年夏天量測</p><p class="small">五年平均 4,755 平方英里。<br>目標是 2035 年<br>降到 1,900 以下。</p></div><figure><img src="assets/gulf-hypoxia-1985-2025-chart.jpg" alt="1985 至 2025 年墨西哥灣缺氧區面積長條圖，多數年份高於管理目標"><figcaption>LSU 與 NOAA，1985–2025 年底層缺氧面積</figcaption></figure></div>',
      f'46–48 分鐘。最大一次是 2017 年的 8,776 平方英里，約三分之二個台灣。2025 年比前一年小約 30%，主要受河川流量與當年氣象影響，不代表農業污染已經解決。來源：{GULF}','cream','故事二',cls='pb-slide')
slide('兩個故事，同一套體系',cols('<h3>健康</h3><p>風險落在<br>沒有能力檢驗的人身上</p>','<h3>環境</h3><p>成本落在<br>沒有參與決定的地方</p>'),
      '48–49 分鐘。回扣開學說的三大環節；公平那一環下週用咖啡小農接。','forest','收尾')
slide('所以要問的不是<br>「工業化好不好」',p('而是：便利是誰做出來的？<br>代價由誰承擔？','lead'),
      '49–50 分鐘。不要求學生反對加工食品，也不要求表態反對資本主義。今天先建立追問的習慣。','cream','收尾')
slide('今天，我開始注意到……',p('一位以前沒注意到的人，<br>或一件以前沒想過的事。','lead')+p('還有，我想再問……'),
      '下課前。一人一句，口頭或寫在聯絡簿都可以。情意目標是看見人、產生好奇，不要求學生宣誓改吃某種食物。','cream','收尾')
slide('下週：一杯咖啡，<br>誰分到多少？',p('9/17　咖啡小農的生活','lead'),
      '依使用者 Word 大綱銜接 9/17 的公平問題。不是今天就要講完的內容。','forest','下週')

def htmlpage(title,body,extra='',style='lesson.css'):
    return f'<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><link rel="stylesheet" href="{style}"><link rel="icon" href="../../favicon.svg">{extra}</head><body>{body}</body></html>'
sections=[]
for i,s in enumerate(slides):
    sections.append(f'<section class="slide {s["theme"]} {s["cls"]}" data-section="{s["section"]}" aria-hidden="{str(i!=0).lower()}"><div class="slide-inner"><h{1 if i==0 else 2}>{s["title"]}</h{1 if i==0 else 2}>{s["body"]}</div><aside class="speaker-notes">{s["notes"]}</aside></section>')
deck='''<main id="deck" aria-label="永續小食堂投影片">'''+''.join(sections)+'''</main>
<nav class="controls" aria-label="投影片導覽"><a href="../../index.html">課程首頁</a><a href="teacher.html" target="_blank" rel="noopener">教師備課</a><button id="prev" aria-label="上一張">←</button><span id="counter"></span><button id="next" aria-label="下一張">→</button><button id="notes-button">備註 N</button><button id="fullscreen">全螢幕 F</button><button id="overview">目錄</button></nav>
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

本課依 115-1 課程大綱第二週設計。兩節各 50 分鐘，以高一學生的觀察、好奇與理解他人為目標。第一節玩食物版「誰是臥底」蒐集學生自己的描述，第二節改用講述帶食品工業化與消費社會，收在兩個真實案例。9/17 的咖啡小農與公平問題留作下一週銜接。

## 明天課前五分鐘

1. 開啟投影片 index.html，先測全螢幕及方向鍵。按 N 會顯示含遊戲答案的備註，投影遊戲時務必關閉。
2. 列印 cards.pdf 的三頁卡片，剪成每輪十張，依 1–10 號發放。卡上不寫身分，老師保留對照表。
3. 五組各準備一張紙記錄原話。第二節是講述，學生不需要電腦。
4. 第二節有三張圖（CDC 疫情地圖、墨西哥灣缺氧地圖與 40 年趨勢圖），先確認投影機顏色能分辨紅、黃、綠。
5. 投影片可完全離線開啟，圖片都在 assets 資料夾內，不依賴網路。

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

## 第二節 50 分鐘（講述）

| 分鐘 | 流程 | 教師工作 |
|---|---|---|
| 0–2 | 接回上一節的原話 | 唸一句學生說過的話當引子 |
| 2–16 | 工業革命與農業的劇變 | 自給生產、人力減少、進步與諷刺、三種代價 |
| 16–19 | 消費社會 | 需求帶動生產，變成為了生產創造需求 |
| 19–25 | 回到遊戲：咖啡 | 進口、分工、為什麼要「學」喝咖啡 |
| 25–40 | 故事一：2018 年美國生菜 | 事件、數字、源頭、追溯困難、誰承擔風險 |
| 40–48 | 故事二：墨西哥灣缺氧區 | 成因鏈、面積、40 年趨勢 |
| 48–50 | 收束與離堂回應 | 「今天我開始注意到……」一人一句 |

整節都是講述，對高一學生偏長。建議在第 26 張「為什麼要學喝咖啡」與第 33 張「你有辦法自己檢驗嗎」各停 30 秒，讓學生轉頭跟旁邊的人講一句，再繼續。這兩處的講者備註也寫了同樣提醒。

原本規劃的 draw.io 食物關係圖活動本次不使用，模板與紙本備援仍保留在教材資料夾，可留待後續週次。

## 概念講到這個程度即可

- **工業化**：透過機械、分工、標準流程、加工與物流，大量而穩定地供應食物。可能帶來便利、保存和成本效益，也可能伴隨資源使用與生態壓力。
- **資本主義下的供應**：企業投入資金、透過市場販售並追求利潤，成本、定價、銷量及競爭會影響生產和採購。工業化與資本主義常交織，但不是同義詞。
- **外部成本的生活說法**：有些代價沒寫在標價上，卻由環境、工作者或社會承擔。不要預設每種情況都一樣。
- 進口未必一定比本地不永續，加工未必不健康，小店也可能有不公平勞動。以具體做法與證據比較。

## 兩個案例的講法與證據強度

兩個案例都是真實事件，數字取自官方報告。講的時候請把「已確認」與「推測」分開說，這本身就是這堂課要教的東西。

### 故事一：2018 年美國蘿蔓生菜 E. coli O157:H7 疫情

| 陳述 | 證據強度 | 依據 |
|---|---|---|
| 210 人感染、36 州、96 人住院、27 人出現溶血性尿毒症候群、5 人死亡 | 已確認 | CDC 於 2018-06-28 宣布疫情結束時的最終統計 |
| 發病日期為 2018-03-13 至 2018-08-22 | 已確認 | 同上 |
| 追溯到 Yuma 地區 23 個農場、36 塊田，無法指出唯一一塊 | 已確認 | FDA 環境評估 |
| 唯一驗出本次疫情菌株的環境樣本，是 Wellton 附近一段約 3.5 英里的灌溉渠道水 | 已確認 | FDA 環境評估 |
| 渠道旁有一座可容納超過 10 萬頭牛的大型飼養場 | 已確認 | FDA 環境評估 |
| 飼養場就是污染源 | **推測，未證實** | FDA 在飼養場的有限採樣中並未驗到本次菌株，只驗到其他致病性大腸桿菌；但也沒有找到其他來源的證據 |
| 出貨紀錄不完整使追溯困難 | 已確認 | FDA 報告與相關報導 |

講述重點不是指控某一座牧場，而是：責任分散在整條供應鏈之後，沒有人能單獨負責，最後由沒有檢驗能力的消費者承擔。避免推論成「企業都在害人」。

### 故事二：墨西哥灣缺氧區（dead zone）

| 陳述 | 證據強度 | 依據 |
|---|---|---|
| 2025 年 7 月 20–25 日實測面積 4,402 平方英里 | 已確認 | NOAA／LSU 2025 Shelfwide Cruise |
| 五年平均 4,755 平方英里；管理目標為 2035 年降到 1,900 以下 | 已確認 | 同上 |
| 1985 年起每年夏天量測，最大一次為 2017 年的 8,776 平方英里 | 已確認 | NOAA |
| 成因為密西西比—阿查法拉亞河流域的過量營養鹽，刺激藻類大量繁殖，死亡分解時耗盡底層氧氣 | 已確認 | NOAA |
| 2025 年比前一年小約 30%，代表農業污染已改善 | **不成立** | 年度變化主要受河川流量與氣象影響，不能單獨當成政策成效 |

換算給學生的比例：4,402 平方英里約 11,400 平方公里，台灣本島約 36,000 平方公里，所以接近三分之一；2017 年的 8,776 平方英里約 22,700 平方公里，約三分之二個台灣。

## 評量建議

本次沒有繳交的作品，評量以課堂觀察為主。若需給分，可採三項各 0–2 分：

1. 觀察：遊戲中說得出具體的食物描述或生活例子。
2. 連結：離堂回應能用自己的話說出一件以前沒想過的事。
3. 好奇與理解：看見一位供應鏈中的人，或提出真正在意、想再查的問題。

不把術語數量或立場一致當成情意目標。

## 保留備用：draw.io 食物關係圖

本次改為講述，這套材料沒有使用，但檔案都留著，之後任何一週想做關係圖都可以直接拿來用：

- `student.html`：學生任務頁與一鍵開啟模板的連結。
- `food-relationships.drawio`：16 張未連線的概念卡模板。
- `template-print.pdf`：A3 橫式紙本備援。

當初選 draw.io 的理由是免費、免註冊，且多對多連線比樹狀心智圖更適合呈現不同詮釋。Excalidraw 與 Coggle 都評估過：前者協作好但自動排版不是重點，後者免費方案偏樹狀發想。

## 資源與事實依據

- 課程日期與主題：使用者提供的《115-1永續小食堂課程大綱.docx》。僅讀取，未修改未規劃週次。
- 地球界限與原圖：https://www.stockholmresilience.org/research/planetary-boundaries.html 。採 2025 評估，圖為 CC BY-NC-ND 3.0，保留原圖與署名。
- 食物系統與環境壓力：https://www.nature.com/articles/s43016-025-01252-6 。注意 food system boundaries 與全球 planetary boundaries 不同，投影片不混用九項食物部門界限的數字。
- 2018 年蘿蔓生菜疫情最終統計與各州病例地圖：https://archive.cdc.gov/www_cdc_gov/ecoli/2018/o157h7-04-18/index.html 。地圖為美國聯邦政府作品。
- FDA 環境評估（渠道、飼養場、追溯困難）：https://www.fda.gov/food/outbreaks-foodborne-illness/environmental-assessment-factors-potentially-contributing-contamination-romaine-lettuce-implicated 。
- 2025 年墨西哥灣缺氧區實測與歷年趨勢：https://coastalscience.noaa.gov/news/below-average-summer-2025-dead-zone-measured-in-gulf/ 。圖為 LSU 與 NOAA 2025 Shelfwide Cruise。
- draw.io（本次未使用，保留備用）：https://www.drawio.com/ 。

已在桌面瀏覽器逐張檢查 41 張投影片，全部無溢出、圖片皆可載入；PDF 為投影片 41 頁、A4 食物卡 3 頁、A3 關係圖 1 頁。

教材為教師備課草稿，請依班級情況調整。由 Codex 協助製作，2026-09-09；第二節改為講述、題庫擴充為 19 組、新增兩個真實案例與官方圖，由 Claude Code 協助修改，2026-09-10。
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
links='<div class="actions"><a class="primary" href="index.html">上課投影片</a><a href="student.html">學生任務（本次未使用）</a><a href="cards.pdf" download>遊戲卡 PDF（A4 三頁）</a><a href="template-print.pdf" download>紙本關係圖 PDF（A3）</a><a href="slides.pdf" download>投影片 PDF</a><a href="lesson-pack.zip" download>離線教材包 ZIP</a></div>'
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
