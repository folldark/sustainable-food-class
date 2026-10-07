/* 以 sustainable-food-class 的原生投影片引擎為基礎，供所有單元共用。 */
(() => {
  "use strict";
  const deck = document.querySelector(".deck");
  const slides = Array.from(deck?.querySelectorAll(".slide") || []);
  if (!slides.length) return;
  const byId = (id) => document.getElementById(id);
  const counter = byId("counter");
  const progress = byId("progress");
  const previousButton = byId("prev");
  const nextButton = byId("next");
  const helpDialog = byId("help-dialog");
  const notesPanel = byId("notes-panel");
  const notesButton = byId("notes");
  const fullscreenButton = byId("fullscreen");
  const deckTitle = deck.dataset.title || document.title;
  let current = 0;
  // 快速跳頁：直接打數字＋Enter，或按 G／點頁碼開啟目錄。目錄由投影片自動生成，不必手寫。
  let typed = "";
  let typedTimer = 0;
  const clamp = (value) => Math.min(Math.max(value, 0), slides.length - 1);
  const format = (value) => String(value).padStart(2, "0");
  const gotoDialog = buildGotoDialog();

  function indexFromHash() {
    const match = location.hash.match(/^#slide-(\d+)$/);
    return match ? clamp(Number(match[1]) - 1) : 0;
  }
  function showSlide(index, updateHash = true) {
    const next = clamp(index);
    // 換頁前把焦點從即將隱藏的連結移回投影片區域。
    if (slides[current].contains(document.activeElement) && current !== next) deck.focus({ preventScroll: true });
    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === next;
      slide.classList.toggle("is-active", active);
      slide.classList.toggle("was-active", slideIndex < next);
      slide.setAttribute("aria-hidden", String(!active));
      slide.inert = !active;
      if (active && current !== next) slide.scrollTop = 0;
    });
    current = next;
    counter.textContent = `${format(current + 1)} / ${format(slides.length)}`;
    progress.style.width = `${((current + 1) / slides.length) * 100}%`;
    previousButton.disabled = current === 0;
    nextButton.disabled = current === slides.length - 1;
    document.title = `${slides[current].dataset.section}｜${deckTitle}`;
    byId("notes-copy").textContent = slides[current].querySelector(".speaker-notes")?.textContent.trim() || "這張沒有額外備註。";
    if (updateHash) history.replaceState(null, "", `#slide-${current + 1}`);
    gotoDialog.querySelectorAll("[data-index]").forEach((item) => item.toggleAttribute("aria-current", Number(item.dataset.index) === current));
  }
  function slideLabel(slide) {
    const heading = slide.querySelector("h1, h2");
    const text = (heading?.textContent || slide.querySelector("p")?.textContent || "").replace(/\s+/g, " ").trim();
    return text.length > 42 ? `${text.slice(0, 42)}…` : text;
  }
  function buildGotoDialog() {
    const dialog = document.createElement("dialog");
    dialog.id = "goto-dialog";
    dialog.className = "goto-dialog";
    dialog.setAttribute("aria-labelledby", "goto-title");
    const items = slides.map((slide, index) => `<li><button type="button" data-index="${index}"><span class="goto-num">${format(index + 1)}</span><span class="goto-section">${slide.dataset.section || ""}</span><span class="goto-heading">${slideLabel(slide)}</span></button></li>`).join("");
    // 「前往」必須是表單裡第一個 submit，輸入框按 Enter 才會走它；關閉鈕放最後。
    dialog.innerHTML = `<form method="dialog"><h2 id="goto-title">跳到</h2><p class="goto-row"><label for="goto-input">頁碼</label><input id="goto-input" type="number" min="1" max="${slides.length}" inputmode="numeric" autocomplete="off" /><button type="submit" value="go">前往</button><span class="goto-hint">或直接在投影片上打數字再按 Enter</span></p><ol class="goto-list">${items}</ol><button class="dialog-close" type="submit" value="cancel" aria-label="關閉目錄">×</button></form>`;
    dialog.addEventListener("click", (event) => {
      const item = event.target.closest("[data-index]");
      if (!item) return;
      dialog.close("cancel");
      showSlide(Number(item.dataset.index));
    });
    dialog.addEventListener("close", () => {
      const input = dialog.querySelector("#goto-input");
      if (dialog.returnValue === "go" && input.value) showSlide(Number(input.value) - 1);
      input.value = "";
      deck.focus({ preventScroll: true });
    });
    document.body.append(dialog);
    return dialog;
  }
  function openGoto() {
    if (gotoDialog.open) return;
    clearTyped();
    gotoDialog.returnValue = "";
    gotoDialog.showModal();
    const input = gotoDialog.querySelector("#goto-input");
    input.value = "";
    input.focus();
    gotoDialog.querySelector("[aria-current]")?.scrollIntoView({ block: "center" });
  }
  function clearTyped() {
    typed = "";
    clearTimeout(typedTimer);
    counter.textContent = `${format(current + 1)} / ${format(slides.length)}`;
  }
  function typeDigit(digit) {
    typed = (typed + digit).slice(-3);
    counter.textContent = `→ ${typed}_`;
    clearTimeout(typedTimer);
    typedTimer = setTimeout(clearTyped, 4000);
  }
  function toggleNotes(force) {
    const open = typeof force === "boolean" ? force : !notesPanel.classList.contains("is-open");
    if (!open && notesPanel.contains(document.activeElement)) notesButton.focus();
    notesPanel.classList.toggle("is-open", open);
    notesPanel.setAttribute("aria-hidden", String(!open));
    notesPanel.inert = !open;
    notesButton.setAttribute("aria-expanded", String(open));
    notesButton.setAttribute("aria-label", open ? "關閉講者備註" : "開啟講者備註");
  }
  async function toggleFullscreen() {
    try {
      const root = document.documentElement;
      if (document.fullscreenElement || document.webkitFullscreenElement) {
        await (document.exitFullscreen?.() ?? document.webkitExitFullscreen?.());
      } else if (root.requestFullscreen) await root.requestFullscreen();
      else if (root.webkitRequestFullscreen) await root.webkitRequestFullscreen();
      else throw new Error("瀏覽器未提供全螢幕功能");
    } catch (error) {
      fullscreenButton.textContent = "全螢幕無法使用";
      fullscreenButton.setAttribute("aria-label", "此瀏覽器目前無法開啟全螢幕，請使用瀏覽器的全螢幕功能");
      console.warn("無法切換全螢幕：", error);
    }
  }
  function syncFullscreen() {
    const active = Boolean(document.fullscreenElement || document.webkitFullscreenElement);
    fullscreenButton.textContent = active ? "離開全螢幕" : "全螢幕";
    fullscreenButton.setAttribute("aria-label", active ? "離開全螢幕" : "進入全螢幕");
  }
  document.addEventListener("keydown", (event) => {
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.isComposing || helpDialog.open || gotoDialog.open) return;
    const target = event.target;
    if (target.closest("input, textarea, select, [contenteditable]:not([contenteditable='false'])")) return;
    // 焦點在按鈕／連結上時，Enter、Space 保留原生啟用行為；方向鍵仍可換頁。
    if (["Enter", " "].includes(event.key) && target.closest("a, button, summary")) return;
    if (/^[0-9]$/.test(event.key)) { event.preventDefault(); typeDigit(event.key); return; }
    if (typed && event.key === "Enter") { event.preventDefault(); const wanted = Number(typed); clearTyped(); showSlide(wanted - 1); return; }
    if (typed && event.key === "Escape") { event.preventDefault(); clearTyped(); return; }
    const actions = {
      ArrowRight: () => showSlide(current + 1), ArrowDown: () => showSlide(current + 1),
      PageDown: () => showSlide(current + 1), Enter: () => showSlide(current + 1), " ": () => showSlide(current + 1),
      ArrowLeft: () => showSlide(current - 1), ArrowUp: () => showSlide(current - 1), PageUp: () => showSlide(current - 1),
      Home: () => showSlide(0), End: () => showSlide(slides.length - 1),
      f: toggleFullscreen, F: toggleFullscreen,
      n: () => toggleNotes(), N: () => toggleNotes(), Escape: () => toggleNotes(false),
      g: openGoto, G: openGoto,
    };
    if (actions[event.key]) { event.preventDefault(); actions[event.key](); }
  });
  previousButton.addEventListener("click", () => showSlide(current - 1));
  nextButton.addEventListener("click", () => showSlide(current + 1));
  byId("help").addEventListener("click", () => helpDialog.showModal());
  notesButton.addEventListener("click", () => toggleNotes());
  byId("close-notes").addEventListener("click", () => toggleNotes(false));
  fullscreenButton.addEventListener("click", toggleFullscreen);
  counter.addEventListener("click", openGoto);
  counter.title = "跳到指定頁（G）";
  window.addEventListener("hashchange", () => showSlide(indexFromHash(), false));
  document.addEventListener("fullscreenchange", syncFullscreen);
  document.addEventListener("webkitfullscreenchange", syncFullscreen);

  let touchStart = null;
  deck.addEventListener("touchstart", (event) => {
    touchStart = null;
    if (helpDialog.open || event.touches.length !== 1 || event.target.closest("a, button")) return;
    const touch = event.touches[0];
    touchStart = { x: touch.clientX, y: touch.clientY, id: touch.identifier };
  }, { passive: true });
  deck.addEventListener("touchend", (event) => {
    if (!touchStart) return;
    const start = touchStart;
    touchStart = null;
    const touch = Array.from(event.changedTouches).find((item) => item.identifier === start.id);
    if (!touch || helpDialog.open) return;
    const dx = touch.clientX - start.x;
    const dy = touch.clientY - start.y;
    if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.4) showSlide(current + (dx < 0 ? 1 : -1));
  }, { passive: true });
  deck.addEventListener("touchcancel", () => { touchStart = null; }, { passive: true });

  showSlide(indexFromHash(), false);
  document.body.classList.add("deck-ready");
})();
