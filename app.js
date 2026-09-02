(() => {
  const slides = Array.from(document.querySelectorAll(".slide"));
  const counter = document.querySelector("#counter");
  const progress = document.querySelector("#progress");
  const previousButton = document.querySelector("#prev");
  const nextButton = document.querySelector("#next");
  const helpButton = document.querySelector("#help");
  const helpDialog = document.querySelector("#help-dialog");
  const notesPanel = document.querySelector("#notes-panel");
  const notesCopy = document.querySelector("#notes-copy");
  const closeNotesButton = document.querySelector("#close-notes");
  let current = 0;

  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
  const format = (value) => String(value).padStart(2, "0");

  function indexFromHash() {
    const match = window.location.hash.match(/^#slide-(\d+)$/);
    return match ? clamp(Number(match[1]) - 1, 0, slides.length - 1) : 0;
  }

  function updateNotes() {
    const note = slides[current].querySelector(".speaker-notes");
    notesCopy.textContent = note?.textContent.trim() || "這張沒有額外備註。";
  }

  function showSlide(index, updateHash = true) {
    const next = clamp(index, 0, slides.length - 1);
    slides.forEach((slide, slideIndex) => {
      slide.classList.toggle("is-active", slideIndex === next);
      slide.classList.toggle("was-active", slideIndex < next);
      slide.setAttribute("aria-hidden", slideIndex === next ? "false" : "true");
    });
    current = next;
    counter.textContent = `${format(current + 1)} / ${format(slides.length)}`;
    progress.style.width = `${((current + 1) / slides.length) * 100}%`;
    previousButton.disabled = current === 0;
    nextButton.disabled = current === slides.length - 1;
    document.title = `${slides[current].dataset.section}｜永續小食堂`;
    updateNotes();

    if (updateHash) {
      history.replaceState(null, "", `#slide-${current + 1}`);
    }
  }

  function toggleNotes(force) {
    const shouldOpen = typeof force === "boolean" ? force : !notesPanel.classList.contains("is-open");
    notesPanel.classList.toggle("is-open", shouldOpen);
    notesPanel.setAttribute("aria-hidden", shouldOpen ? "false" : "true");
  }

  async function toggleFullscreen() {
    try {
      if (!document.fullscreenElement) await document.documentElement.requestFullscreen();
      else await document.exitFullscreen();
    } catch (error) {
      console.warn("無法切換全螢幕：", error);
    }
  }

  function shouldIgnoreKey(event) {
    const tag = event.target.tagName;
    return ["INPUT", "TEXTAREA", "SELECT", "BUTTON", "A"].includes(tag) || helpDialog.open;
  }

  document.addEventListener("keydown", (event) => {
    if (shouldIgnoreKey(event)) return;
    const actions = {
      ArrowRight: () => showSlide(current + 1),
      ArrowDown: () => showSlide(current + 1),
      PageDown: () => showSlide(current + 1),
      Enter: () => showSlide(current + 1),
      " ": () => showSlide(current + 1),
      ArrowLeft: () => showSlide(current - 1),
      ArrowUp: () => showSlide(current - 1),
      PageUp: () => showSlide(current - 1),
      Home: () => showSlide(0),
      End: () => showSlide(slides.length - 1),
      f: toggleFullscreen,
      F: toggleFullscreen,
      n: () => toggleNotes(),
      N: () => toggleNotes(),
      Escape: () => toggleNotes(false),
    };
    if (actions[event.key]) {
      event.preventDefault();
      actions[event.key]();
    }
  });

  previousButton.addEventListener("click", () => showSlide(current - 1));
  nextButton.addEventListener("click", () => showSlide(current + 1));
  helpButton.addEventListener("click", () => helpDialog.showModal());
  closeNotesButton.addEventListener("click", () => toggleNotes(false));
  window.addEventListener("hashchange", () => showSlide(indexFromHash(), false));

  let touchStartX = null;
  document.addEventListener("touchstart", (event) => {
    touchStartX = event.changedTouches[0].clientX;
  }, { passive: true });
  document.addEventListener("touchend", (event) => {
    if (touchStartX === null) return;
    const distance = event.changedTouches[0].clientX - touchStartX;
    if (Math.abs(distance) > 55) showSlide(current + (distance < 0 ? 1 : -1));
    touchStartX = null;
  }, { passive: true });

  showSlide(indexFromHash(), false);
})();
