// ============================================================
// 重點標記閱讀遊戲 - Code.gs
// 文章內容與標題在 Article.gs；換文章只要改那一檔
// 部署方式：執行身分「我（ht341）」、存取權「網域內使用者」
//   → 學生不需要試算表權限；試算表在第一次有人開啟時自動建立
// ============================================================

const ADMIN_EMAIL = 'ht341@hmjh.chc.edu.tw';

// ── 主要路由 ─────────────────────────────────────────────
function doGet(e) {
  const mode = (e.parameter.mode || '').toLowerCase();
  const email = Session.getActiveUser().getEmail();

  if (mode === 'admin') {
    if (email !== ADMIN_EMAIL) {
      return HtmlService.createHtmlOutput('<h1 style="font-family:sans-serif;padding:2rem">無權限存取管理面板</h1>');
    }
    return HtmlService.createTemplateFromFile('Admin')
      .evaluate()
      .setTitle('教師管理面板｜' + GAME_TITLE)
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
  }

  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('重點標記遊戲｜' + GAME_TITLE)
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

// ── 取得整體狀態（學生端輪詢用）────────────────────────
function getState() {
  const email = Session.getActiveUser().getEmail();
  const ss = openSpreadsheet();
  const settings = getSettingsMap(ss);
  const mySubmissions = getMySubmissions(ss, email);

  const sections = SECTIONS.map(s => {
    const cfg = settings[s.id] || { status: 'closed', charLimit: s.charLimit };
    return {
      id: s.id,
      title: s.title,
      text: s.text,
      charLimit: cfg.charLimit,
      status: cfg.status,
      submitted: !!mySubmissions[s.id],
      mySelection: mySubmissions[s.id] || null
    };
  });

  return { email, sections };
}

// ── 提交選取 ──────────────────────────────────────────────
function submitSelection(payload) {
  const email = Session.getActiveUser().getEmail();
  if (!email) throw new Error('請先登入 Google 帳號');

  const { sectionId, selectedText } = payload;
  // 支援新版多段 ranges，以及舊版單段 startIdx/endIdx
  const ranges = payload.ranges || [{ startIdx: payload.startIdx, endIdx: payload.endIdx }];

  const ss = openSpreadsheet();
  const settings = getSettingsMap(ss);
  const cfg = settings[sectionId];

  if (!cfg || cfg.status !== 'open') throw new Error('此段落目前不開放標記');

  const section = SECTIONS.find(s => s.id === sectionId);
  const visibleLen = ranges.reduce((sum, r) => {
    let count = 0;
    for (let i = r.startIdx; i < r.endIdx && i < section.text.length; i++) {
      if (section.text[i] !== '\n') count++;
    }
    return sum + count;
  }, 0);
  if (visibleLen > cfg.charLimit) throw new Error(`超過字數上限（${cfg.charLimit} 字）`);
  if (visibleLen === 0) throw new Error('請先選取文字');

  // 以第一段 start、最後一段 end 存入欄位（向下相容），完整 ranges 序列化進 selectedText 欄
  const startIdx = ranges[0].startIdx;
  const endIdx = ranges[ranges.length - 1].endIdx;
  const storedText = JSON.stringify({ text: selectedText, ranges: ranges });

  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
  const sheet = ss.getSheetByName('Submissions');
  const rows = sheet.getDataRange().getValues();

  // 找是否已有舊記錄（允許重新標記）
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][1] === email && rows[i][3] === sectionId) {
      sheet.getRange(i + 1, 1, 1, 7).setValues([[
        new Date(), email, displayName(email), sectionId, startIdx, endIdx, storedText
      ]]);
      return { success: true, updated: true };
    }
  }

  sheet.appendRow([new Date(), email, displayName(email), sectionId, startIdx, endIdx, storedText]);
  return { success: true, updated: false };
  } finally {
    lock.releaseLock();
  }
}

// ── 取得結果（熱點圖 + 得分）────────────────────────────
function getResults(sectionId) {
  const email = Session.getActiveUser().getEmail();
  const ss = openSpreadsheet();
  const settings = getSettingsMap(ss);
  const cfg = settings[sectionId];

  if (!cfg || cfg.status !== 'revealed') throw new Error('結果尚未公布');

  const section = SECTIONS.find(s => s.id === sectionId);
  const textLen = section.text.length;
  const heat = new Array(textLen).fill(0);

  const sheet = ss.getSheetByName('Submissions');
  const rows = sheet.getDataRange().getValues().slice(1)
    .filter(r => r[3] === sectionId);

  // 解析 ranges（新格式：JSON；舊格式：startIdx/endIdx 欄位）
  function parseRanges(r) {
    try {
      const parsed = JSON.parse(r[6]);
      if (parsed && parsed.ranges) return parsed.ranges;
    } catch(e) {}
    return [{ startIdx: Number(r[4]), endIdx: Number(r[5]) }];
  }

  rows.forEach(function(r) {
    parseRanges(r).forEach(function(rng) {
      for (let i = rng.startIdx; i < rng.endIdx && i < textLen; i++) heat[i]++;
    });
  });

  let myScore = 0, myRanges = [];
  const mine = rows.find(r => r[1] === email);
  if (mine) {
    myRanges = parseRanges(mine);
    myRanges.forEach(function(rng) {
      for (let i = rng.startIdx; i < rng.endIdx && i < textLen; i++) {
        myScore += Math.max(0, heat[i] - 1); // 扣掉自己
      }
    });
  }

  // 排行榜
  const leaderboard = rows.map(function(r) {
    let score = 0;
    parseRanges(r).forEach(function(rng) {
      for (let i = rng.startIdx; i < rng.endIdx && i < textLen; i++) score += Math.max(0, heat[i] - 1);
    });
    return { name: displayName(r[1]), score };
  }).sort((a, b) => b.score - a.score);

  // 保留 myStart/myEnd 向下相容
  const myStart = myRanges.length > 0 ? myRanges[0].startIdx : -1;
  const myEnd   = myRanges.length > 0 ? myRanges[myRanges.length - 1].endIdx : -1;

  return { heat, myScore, myStart, myEnd, myRanges, leaderboard, total: rows.length };
}

// ── 管理員操作 ────────────────────────────────────────────
function adminAction(action) {
  const email = Session.getActiveUser().getEmail();
  if (email !== ADMIN_EMAIL) throw new Error('無權限');

  const ss = openSpreadsheet();
  const sheet = ss.getSheetByName('Settings');
  const rows = sheet.getDataRange().getValues();

  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] === action.sectionId) {
      if (action.type === 'open')       sheet.getRange(i + 1, 2).setValue('open');
      if (action.type === 'close')      sheet.getRange(i + 1, 2).setValue('closed');
      if (action.type === 'reveal')     sheet.getRange(i + 1, 2).setValue('revealed');
      if (action.type === 'setLimit')   sheet.getRange(i + 1, 3).setValue(action.charLimit);
      if (action.type === 'reset') {
        // 狀態回到 closed，並清除該段所有送出記錄
        sheet.getRange(i + 1, 2).setValue('closed');
        const subSheet = ss.getSheetByName('Submissions');
        const subRows = subSheet.getDataRange().getValues();
        for (let j = subRows.length - 1; j >= 1; j--) {
          if (subRows[j][3] === action.sectionId) subSheet.deleteRow(j + 1);
        }
      }
      break;
    }
  }
  return { success: true };
}

function getAdminData() {
  const email = Session.getActiveUser().getEmail();
  if (email !== ADMIN_EMAIL) throw new Error('無權限');

  const ss = openSpreadsheet();
  const settings = getSettingsMap(ss);
  const subs = ss.getSheetByName('Submissions').getDataRange().getValues().slice(1);

  return SECTIONS.map(s => {
    const cfg = settings[s.id] || { status: 'closed', charLimit: s.charLimit };
    return {
      id: s.id,
      title: s.title,
      status: cfg.status,
      charLimit: cfg.charLimit,
      count: subs.filter(r => r[3] === s.id).length
    };
  });
}

// ── 初始化（只需執行一次）────────────────────────────────
// openSpreadsheet() 找不到試算表時會自動呼叫，也可在編輯器手動執行
function initGame() {
  const ss = SpreadsheetApp.create(GAME_TITLE + '｜閱讀遊戲資料');
  PropertiesService.getScriptProperties().setProperty('SPREADSHEET_ID', ss.getId());

  const settingsSheet = ss.getActiveSheet().setName('Settings');
  settingsSheet.appendRow(['section_id', 'status', 'char_limit']);
  SECTIONS.forEach(s => settingsSheet.appendRow([s.id, 'closed', s.charLimit]));

  const subSheet = ss.insertSheet('Submissions');
  subSheet.appendRow(['timestamp', 'email', 'display_name', 'section_id', 'start_idx', 'end_idx', 'selected_text']);

  return `完成！試算表 ID：${ss.getId()}\n試算表網址：${ss.getUrl()}`;
}

// ── 工具函式 ──────────────────────────────────────────────
function openSpreadsheet() {
  const props = PropertiesService.getScriptProperties();
  let id = props.getProperty('SPREADSHEET_ID');
  if (!id) {
    // 第一次使用：加鎖避免多位學生同時開啟時重複建立
    const lock = LockService.getScriptLock();
    lock.waitLock(30000);
    try {
      id = props.getProperty('SPREADSHEET_ID');
      if (!id) {
        initGame();
        id = props.getProperty('SPREADSHEET_ID');
      }
    } finally {
      lock.releaseLock();
    }
  }
  return SpreadsheetApp.openById(id);
}

function getSettingsMap(ss) {
  const rows = ss.getSheetByName('Settings').getDataRange().getValues().slice(1);
  const map = {};
  rows.forEach(r => { map[r[0]] = { status: r[1], charLimit: r[2] }; });
  return map;
}

function getMySubmissions(ss, email) {
  const rows = ss.getSheetByName('Submissions').getDataRange().getValues().slice(1);
  const map = {};
  rows.filter(r => r[1] === email).forEach(function(r) {
    let text = r[6], ranges = null;
    try {
      const parsed = JSON.parse(r[6]);
      if (parsed && parsed.ranges) { text = parsed.text; ranges = parsed.ranges; }
    } catch(e) {}
    map[r[3]] = { startIdx: Number(r[4]), endIdx: Number(r[5]), text: text, ranges: ranges };
  });
  return map;
}

function displayName(email) {
  return email.split('@')[0];
}
