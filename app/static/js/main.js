/**
 * Project: LifeLine Connect (Blood Bank Network)
 * Component: Frontend Interactive Client Script (World-Class UX Engine)
 */

document.addEventListener("DOMContentLoaded", function () {
  // ==========================================================================
  // 1. WEB AUDIO SYNTHESIZER & SOUND FEEDBACK (Zero External Audio Files)
  // ==========================================================================
  let audioCtx = null;
  let soundEnabled = localStorage.getItem("lifeline_sound") === "true";

  function getAudioContext() {
    if (!audioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) {
        audioCtx = new AudioContextClass();
      }
    }
    if (audioCtx && audioCtx.state === "suspended") {
      audioCtx.resume();
    }
    return audioCtx;
  }

  function playSoftClick() {
    if (!soundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(880, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(440, ctx.currentTime + 0.05);
      gain.gain.setValueAtTime(0.04, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.05);
    } catch (e) {}
  }

  function playSuccessChord() {
    if (!soundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      [523.25, 659.25, 783.99].forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.04);
        gain.gain.setValueAtTime(0.03, ctx.currentTime + idx * 0.04);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.04 + 0.35);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(ctx.currentTime + idx * 0.04);
        osc.stop(ctx.currentTime + idx * 0.04 + 0.35);
      });
    } catch (e) {}
  }

  // Sound Toggle Control
  const soundToggleBtn = document.getElementById("btn-sound-toggle");
  function updateSoundIcon() {
    if (soundToggleBtn) {
      soundToggleBtn.innerHTML = soundEnabled ? "🔊" : "🔇";
      soundToggleBtn.title = soundEnabled ? "Clinical Audio Feedback: ON (Click to Mute)" : "Clinical Audio Feedback: MUTED (Click to Enable)";
    }
  }
  updateSoundIcon();

  if (soundToggleBtn) {
    soundToggleBtn.addEventListener("click", function () {
      soundEnabled = !soundEnabled;
      localStorage.setItem("lifeline_sound", soundEnabled ? "true" : "false");
      updateSoundIcon();
      if (soundEnabled) playSuccessChord();
    });
  }

  // ==========================================================================
  // 2. MATERIAL BUTTON RIPPLE EFFECT
  // ==========================================================================
  document.querySelectorAll(".btn").forEach(function (button) {
    button.addEventListener("click", function (e) {
      playSoftClick();
      const rect = this.getBoundingClientRect();
      const ripple = document.createElement("span");
      ripple.classList.add("ripple-wave");
      const size = Math.max(rect.width, rect.height);
      ripple.style.width = ripple.style.height = `${size}px`;
      ripple.style.left = `${e.clientX - rect.left - size / 2}px`;
      ripple.style.top = `${e.clientY - rect.top - size / 2}px`;
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });

  // ==========================================================================
  // 3. COUNT-UP METRIC ANIMATION
  // ==========================================================================
  function animateCountUp(el, target, duration = 1200) {
    let start = 0;
    const startTime = performance.now();

    function step(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(easeProgress * (target - start) + start);
      el.innerText = current.toLocaleString();

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.innerText = target.toLocaleString();
      }
    }
    requestAnimationFrame(step);
  }

  document.querySelectorAll(".stat-value").forEach(function (valEl) {
    const rawText = valEl.innerText.trim().replace(/,/g, "");
    const targetNum = parseInt(rawText, 10);
    if (!isNaN(targetNum) && targetNum > 0) {
      animateCountUp(valEl, targetNum, 1000);
    }
  });

  // ==========================================================================
  // 4. INTERACTIVE BLOOD TRANSFUSION COMPATIBILITY CALCULATOR
  // ==========================================================================
  const compatibilityRules = {
    "O-": {
      name: "O Negative (Universal Donor)",
      give: ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
      receive: ["O-"],
      badge: "⭐ Universal RBC Donor — Can be safely given to ANY emergency patient!"
    },
    "O+": {
      name: "O Positive (Most Common)",
      give: ["O+", "A+", "B+", "AB+"],
      receive: ["O+", "O-"],
      badge: "Vital for all Rh-positive patients (over 80% of regional demand)."
    },
    "A-": {
      name: "A Negative",
      give: ["A-", "A+", "AB-", "AB+"],
      receive: ["A-", "O-"],
      badge: "Rare and essential for surgical cross-matches."
    },
    "A+": {
      name: "A Positive",
      give: ["A+", "AB+"],
      receive: ["A+", "A-", "O+", "O-"],
      badge: "High clinical demand for elective and acute surgeries."
    },
    "B-": {
      name: "B Negative",
      give: ["B-", "B+", "AB-", "AB+"],
      receive: ["B-", "O-"],
      badge: "Very rare donor group (under 2% of population)."
    },
    "B+": {
      name: "B Positive",
      give: ["B+", "AB+"],
      receive: ["B+", "B-", "O+", "O-"],
      badge: "Essential support for trauma care and chronic transfusion."
    },
    "AB-": {
      name: "AB Negative",
      give: ["AB-", "AB+"],
      receive: ["AB-", "A-", "B-", "O-"],
      badge: "Rarest regular blood group in clinical reserves."
    },
    "AB+": {
      name: "AB Positive (Universal Recipient)",
      give: ["AB+"],
      receive: ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
      badge: "🌟 Universal RBC Recipient — Can safely receive red blood cells from ANY donor!"
    }
  };

  const compatBtns = document.querySelectorAll(".compat-btn");
  const givePillsContainer = document.getElementById("compat-give-pills");
  const receivePillsContainer = document.getElementById("compat-receive-pills");
  const compatNoteEl = document.getElementById("compat-note");
  const compatTitleEl = document.getElementById("compat-title");

  function selectBloodGroup(group) {
    const data = compatibilityRules[group];
    if (!data) return;

    compatBtns.forEach(btn => {
      btn.classList.toggle("active", btn.dataset.group === group);
    });

    if (compatTitleEl) compatTitleEl.innerText = data.name;
    if (compatNoteEl) compatNoteEl.innerText = data.badge;

    if (givePillsContainer) {
      givePillsContainer.innerHTML = data.give
        .map(g => `<span class="compat-pill give">${g}</span>`)
        .join("");
    }

    if (receivePillsContainer) {
      receivePillsContainer.innerHTML = data.receive
        .map(g => `<span class="compat-pill receive">${g}</span>`)
        .join("");
    }

    document.querySelectorAll(".blood-badge-card").forEach(card => {
      const sym = card.querySelector(".blood-type-symbol");
      if (sym && data.give.includes(sym.innerText.trim())) {
        card.classList.add("active-compat");
      } else {
        card.classList.remove("active-compat");
      }
    });
  }

  compatBtns.forEach(btn => {
    btn.addEventListener("click", function () {
      playSoftClick();
      selectBloodGroup(this.dataset.group);
    });
  });

  if (compatBtns.length > 0) {
    selectBloodGroup("O-");
  }

  document.querySelectorAll(".blood-badge-card").forEach(card => {
    card.addEventListener("click", function () {
      const sym = this.querySelector(".blood-type-symbol");
      if (sym) {
        selectBloodGroup(sym.innerText.trim());
        const compatSection = document.getElementById("interactive-compat-matrix");
        if (compatSection) {
          compatSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
      }
    });
  });

  // ==========================================================================
  // 5. UNIVERSAL COMMAND PALETTE (CTRL+K / ⌘K)
  // ==========================================================================
  const palette = document.getElementById("command-palette");
  const paletteInput = document.getElementById("palette-input");
  const paletteItemsContainer = document.getElementById("palette-items");
  const triggerBtn = document.getElementById("btn-trigger-palette");

  const navigationCommands = [
    { title: "Command Center Dashboard", category: "Navigation", icon: "📊", url: "/" },
    { title: "Geospatial Logistics & GPS Radar Map", category: "Logistics", icon: "🗺️", url: "/logistics/" },
    { title: "IoT Cold-Chain Storage & Sensor Telemetry", category: "Logistics", icon: "❄️", url: "/logistics/" },
    { title: "AI Blood Shortage Forecaster & Smart Donor Dispatch", category: "AI & Analytics", icon: "🤖", url: "/analytics/forecaster" },
    { title: "Donor Registry & History", category: "Donors", icon: "👥", url: "/donors/" },
    { title: "Register New Donor Intake", category: "Donors", icon: "➕", url: "/donors/register" },
    { title: "Camps Catalogue & Venue Map", category: "Camps", icon: "⛺", url: "/camps/" },
    { title: "Top-Rated Camps Leaderboard", category: "Camps", icon: "⭐", url: "/camps/top-rated" },
    { title: "Inventory Component Matrix", category: "Inventory", icon: "🩸", url: "/inventory/" },
    { title: "Expiring Blood Alert (FEFO)", category: "Inventory", icon: "⚠️", url: "/inventory/expiring?days=7" },
    { title: "Record Donation & Intake", category: "Inventory", icon: "💉", url: "/inventory/donate" },
    { title: "Hospital Requisitions", category: "Hospitals", icon: "🏥", url: "/hospitals/requests" },
    { title: "New Blood Order Requisition", category: "Hospitals", icon: "📝", url: "/hospitals/requests/new" },
    { title: "Dispatch & Logistics Audit Trail", category: "Hospitals", icon: "🚚", url: "/hospitals/dispatches" },
    { title: "Emergency Appeals Broadcast Board", category: "Emergency", icon: "🚨", url: "/appeals/" },
    { title: "Broadcast Urgent Appeal", category: "Emergency", icon: "📢", url: "/appeals/new" },
    { title: "PL/SQL Business Reports Hub", category: "Reports", icon: "📈", url: "/reports/" },
    { title: "Report 1: Blood Collection by Camp", category: "Reports", icon: "📊", url: "/reports/1" },
    { title: "Report 2: Inventory & Expiry Forecast", category: "Reports", icon: "⏰", url: "/reports/2?days=7" },
    { title: "Report 3: Donor Eligibility Dossier", category: "Reports", icon: "📋", url: "/reports/3?donor_id=1001" },
    { title: "Report 4: Hospital Turnaround & FEFO", category: "Reports", icon: "⚡", url: "/reports/4" },
    { title: "Report 5: Staff Deployment Workload", category: "Reports", icon: "🧑‍⚕️", url: "/reports/5" },
    { title: "Sign In / Switch Profile", category: "Auth", icon: "🔑", url: "/auth/login" },
    { title: "Register New User Account", category: "Auth", icon: "👤", url: "/auth/register" }
  ];

  function openPalette() {
    if (!palette) return;
    palette.classList.add("open");
    playSoftClick();
    if (paletteInput) {
      paletteInput.value = "";
      renderPaletteItems(navigationCommands);
      setTimeout(() => paletteInput.focus(), 50);
    }
  }

  function closePalette() {
    if (!palette) return;
    palette.classList.remove("open");
  }

  function renderPaletteItems(items) {
    if (!paletteItemsContainer) return;
    if (items.length === 0) {
      paletteItemsContainer.innerHTML = `<div style="padding:1.5rem; text-align:center; color:var(--text-muted);">No matching commands or pages found.</div>`;
      return;
    }

    paletteItemsContainer.innerHTML = items
      .map(
        (item, idx) => `
        <a href="${item.url}" class="palette-item ${idx === 0 ? "active" : ""}" data-index="${idx}">
          <div style="display:flex; align-items:center;">
            <span class="palette-item-icon">${item.icon}</span>
            <div>
              <div style="font-weight:600;">${item.title}</div>
              <div style="font-size:0.75rem; color:var(--text-secondary);">${item.category}</div>
            </div>
          </div>
          <span style="font-size:0.75rem; color:var(--text-muted);">&rarr;</span>
        </a>
      `
      )
      .join("");
  }

  if (triggerBtn) {
    triggerBtn.addEventListener("click", openPalette);
  }

  window.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (palette && palette.classList.contains("open")) {
        closePalette();
      } else {
        openPalette();
      }
    } else if (e.key === "Escape") {
      closePalette();
    }
  });

  if (palette) {
    palette.addEventListener("click", function (e) {
      if (e.target === palette) closePalette();
    });
  }

  if (paletteInput) {
    paletteInput.addEventListener("input", function () {
      const q = this.value.toLowerCase().trim();
      const filtered = navigationCommands.filter(
        item => item.title.toLowerCase().includes(q) || item.category.toLowerCase().includes(q)
      );
      renderPaletteItems(filtered);
    });

    paletteInput.addEventListener("keydown", function (e) {
      const items = paletteItemsContainer.querySelectorAll(".palette-item");
      let activeIdx = -1;
      items.forEach((item, idx) => {
        if (item.classList.contains("active")) activeIdx = idx;
      });

      if (e.key === "ArrowDown") {
        e.preventDefault();
        if (items.length > 0) {
          const nextIdx = (activeIdx + 1) % items.length;
          items.forEach(i => i.classList.remove("active"));
          items[nextIdx].classList.add("active");
          items[nextIdx].scrollIntoView({ block: "nearest" });
        }
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        if (items.length > 0) {
          const prevIdx = (activeIdx - 1 + items.length) % items.length;
          items.forEach(i => i.classList.remove("active"));
          items[prevIdx].classList.add("active");
          items[prevIdx].scrollIntoView({ block: "nearest" });
        }
      } else if (e.key === "Enter") {
        e.preventDefault();
        if (activeIdx >= 0 && items[activeIdx]) {
          items[activeIdx].click();
        }
      }
    });
  }

  // ==========================================================================
  // 6. INSTANT CLIENT-SIDE DATA TABLE FILTER
  // ==========================================================================
  document.querySelectorAll("[data-table-filter]").forEach(input => {
    const targetTableSelector = input.dataset.tableFilter;
    const targetTable = document.querySelector(targetTableSelector);
    if (!targetTable) return;

    input.addEventListener("input", function () {
      const term = this.value.toLowerCase().trim();
      const rows = targetTable.querySelectorAll("tbody tr");
      let matchCount = 0;

      rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        const match = text.includes(term);
        row.style.display = match ? "" : "none";
        if (match) matchCount++;
      });

      const counterEl = document.getElementById(this.dataset.countTarget);
      if (counterEl) {
        counterEl.innerText = matchCount;
      }
    });
  });

  // ==========================================================================
  // 7. FLOATING ACTION BUTTON (FAB) SPEED DIAL
  // ==========================================================================
  const fabContainer = document.getElementById("fab-container");
  const fabMain = document.getElementById("fab-main");
  const fabScrollTop = document.getElementById("fab-scroll-top");

  if (fabMain && fabContainer) {
    fabMain.addEventListener("click", function (e) {
      e.stopPropagation();
      playSoftClick();
      fabContainer.classList.toggle("open");
    });
  }

  if (fabScrollTop) {
    fabScrollTop.addEventListener("click", function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
      if (fabContainer) fabContainer.classList.remove("open");
    });
  }

  document.addEventListener("click", function (e) {
    if (fabContainer && !fabContainer.contains(e.target)) {
      fabContainer.classList.remove("open");
    }
  });

  // ==========================================================================
  // 8. AUTO-DISMISS FLASH ALERTS
  // ==========================================================================
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.opacity = "0";
      alert.style.transition = "opacity 0.5s ease";
      setTimeout(() => alert.remove(), 500);
    }, 6000);
  });

  // ==========================================================================
  // 9. DYNAMIC DONOR ELIGIBILITY CHECK VIA AJAX
  // ==========================================================================
  const checkBtn = document.getElementById("btn-check-eligibility");
  if (checkBtn) {
    checkBtn.addEventListener("click", function () {
      const donorId = this.dataset.donorId;
      const statusBadge = document.getElementById("eligibility-status-badge");
      const msgBox = document.getElementById("eligibility-msg-box");

      checkBtn.innerText = "Evaluating...";
      checkBtn.disabled = true;

      fetch(`/donors/${donorId}/check-eligibility`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      })
        .then(response => response.json())
        .then(data => {
          checkBtn.innerText = "Re-check Eligibility";
          checkBtn.disabled = false;

          if (data.eligible) {
            playSuccessChord();
          }

          if (msgBox) {
            msgBox.innerText = data.message;
            msgBox.style.display = "block";
          }

          if (statusBadge) {
            if (data.eligible) {
              statusBadge.className = "badge badge-eligible";
              statusBadge.innerText = "ELIGIBLE";
            } else {
              statusBadge.className = "badge badge-deferred";
              statusBadge.innerText = "DEFERRED";
            }
          }
        })
        .catch(err => {
          checkBtn.innerText = "Check Eligibility";
          checkBtn.disabled = false;
          console.error("Eligibility check error:", err);
        });
    });
  }

  // ==========================================================================
  // 12. ENTERPRISE NAVBAR DROPDOWNS & MOBILE ACCORDION
  // ==========================================================================
  const appNavbar = document.getElementById("app-navbar");
  const navMobileToggle = document.getElementById("nav-mobile-toggle");

  if (navMobileToggle && appNavbar) {
    navMobileToggle.addEventListener("click", function (e) {
      e.stopPropagation();
      appNavbar.classList.toggle("mobile-menu-open");
    });
  }

  // Toggle dropdowns on click for touch / accessibility
  document.querySelectorAll(".nav-has-dropdown").forEach(function (dropdown) {
    const trigger = dropdown.querySelector(".nav-link-btn, .nav-user-chip");
    if (trigger) {
      trigger.addEventListener("click", function (e) {
        const isMobile = window.innerWidth <= 980;
        if (isMobile) {
          e.preventDefault();
          dropdown.classList.toggle("mobile-open");
        }
      });
    }
  });

  // Close menus when clicking outside
  document.addEventListener("click", function (e) {
    if (appNavbar && !appNavbar.contains(e.target)) {
      appNavbar.classList.remove("mobile-menu-open");
      document.querySelectorAll(".nav-has-dropdown.mobile-open").forEach(function (d) {
        d.classList.remove("mobile-open");
      });
    }
  });

  // Close on Escape key
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      if (appNavbar) appNavbar.classList.remove("mobile-menu-open");
      document.querySelectorAll(".nav-has-dropdown.mobile-open").forEach(function (d) {
        d.classList.remove("mobile-open");
      });
    }
  });

  // ==========================================================================
  // 12. LIVE TELEMETRY CLOCK, DUAL-PERSONA SWITCHER & HOTKEYS
  // ==========================================================================

  // Live Telemetry Ribbon Clock (Sri Lanka UTC+5:30)
  const hudClock = document.getElementById("live-hud-clock");
  function updateHudClock() {
    if (!hudClock) return;
    try {
      const now = new Date();
      const options = { timeZone: "Asia/Colombo", hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" };
      hudClock.textContent = new Intl.DateTimeFormat("en-GB", options).format(now) + " IST";
    } catch (e) {
      hudClock.textContent = new Date().toLocaleTimeString();
    }
  }
  updateHudClock();
  setInterval(updateHudClock, 1000);

  // Dual-Persona Switcher (Admin HUD vs Donor View)
  const btnAdmin = document.getElementById("btn-mode-admin");
  const btnDonor = document.getElementById("btn-mode-donor");
  const savedPersona = localStorage.getItem("lifeline_persona") || "admin";

  function setPersona(persona) {
    document.body.setAttribute("data-persona", persona);
    localStorage.setItem("lifeline_persona", persona);
    if (btnAdmin && btnDonor) {
      if (persona === "admin") {
        btnAdmin.classList.add("active");
        btnDonor.classList.remove("active", "donor-mode");
      } else {
        btnDonor.classList.add("active", "donor-mode");
        btnAdmin.classList.remove("active");
      }
    }
  }

  setPersona(savedPersona);

  if (btnAdmin) {
    btnAdmin.addEventListener("click", function () {
      playSoftClick();
      setPersona("admin");
    });
  }
  if (btnDonor) {
    btnDonor.addEventListener("click", function () {
      playSoftClick();
      setPersona("donor");
    });
  }

  // Number Counter Animation for KPI Cards
  document.querySelectorAll(".counter-anim").forEach(function (counter) {
    const target = parseInt(counter.getAttribute("data-count") || counter.textContent.trim(), 10);
    if (isNaN(target)) return;
    let current = 0;
    const duration = 1000; // ms
    const stepTime = 20;
    const totalSteps = duration / stepTime;
    const increment = Math.max(1, target / totalSteps);

    const timer = setInterval(function () {
      current += increment;
      if (current >= target) {
        counter.textContent = target;
        clearInterval(timer);
      } else {
        counter.textContent = Math.floor(current);
      }
    }, stepTime);
  });

  // Global Operational Keyboard Shortcuts (When not typing in inputs)
  document.addEventListener("keydown", function (e) {
    const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : "";
    if (activeTag === "input" || activeTag === "textarea" || activeTag === "select") return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;

    const key = e.key.toUpperCase();
    if (key === "I") {
      playSoftClick();
      window.location.href = "/inventory/donate";
    } else if (key === "D") {
      playSoftClick();
      window.location.href = "/hospitals/requests";
    } else if (key === "A") {
      playSoftClick();
      window.location.href = "/appeals/new";
    } else if (key === "R") {
      playSoftClick();
      window.location.href = "/logistics/";
    } else if (key === "S") {
      playSoftClick();
      window.location.href = "/database/";
    }
  });
});


