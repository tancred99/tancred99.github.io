// Accounts + cloud-saved progress (Firebase Auth + Firestore). Loaded as an ES module.
const SDK = "https://www.gstatic.com/firebasejs/13.2.0/";
const LSC = "ruDrills.cloud.v1", GUEST = "ruDrills.guest";
const $ = (id) => document.getElementById(id);
const App = window.RuApp;
const cfg = window.RU_FIREBASE_CONFIG;
const ov = $("authOv");
let fb = null, auth = null, db = null, user = null, pendingName = "";
let docExists = null, pushTimer = null, gen = 0, ackGen = 0, live = false, offlineNote = false;

function lj(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }
function sj(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
function meta() { return lj(LSC) || {}; }
function setMeta(m) { sj(LSC, Object.assign(meta(), m)); }

// ---------- UI ----------
function showOv(view) {
  ov.classList.remove("hidden"); document.body.classList.add("locked");
  ["avLoading", "avForm", "avFail"].forEach((v) => $(v).classList.toggle("hidden", v !== view));
}
function hideOv() { ov.classList.add("hidden"); document.body.classList.remove("locked"); }
function msg(t, kind) { const m = $("aMsg"); m.textContent = t || ""; m.className = "amsg" + (kind ? " " + kind : ""); }
function busy(b) { ["aGo", "aForgot", "aSwitch"].forEach((id) => { $(id).disabled = b; }); $("aGo").textContent = b ? "Please wait…" : (mode === "up" ? "Create account" : "Sign in"); }
let mode = "in";
function setMode(m) {
  mode = m; msg("");
  $("aTitle").textContent = m === "up" ? "Создать аккаунт · Create account" : "Войти · Sign in";
  $("aNameBox").classList.toggle("hidden", m !== "up");
  $("aPass").autocomplete = m === "up" ? "new-password" : "current-password";
  $("aGo").textContent = m === "up" ? "Create account" : "Sign in";
  $("aSwitch").textContent = m === "up" ? "I already have an account · Sign in" : "New here? Create an account";
  $("aForgot").classList.toggle("hidden", m === "up");
  $("aPassHint").classList.toggle("hidden", m !== "up");
}
function sync(t, kind) { const s = $("uSync"); s.textContent = t; s.className = "usync " + (kind || ""); }
function bar() {
  const b = $("userbar"); b.classList.remove("hidden");
  if (user) {
    $("uName").textContent = "👤 " + (user.displayName || pendingName || user.email);
    $("uName").title = user.email || "";
    $("uOut").textContent = "Sign out";
  } else {
    $("uName").textContent = "Not signed in";
    sync("· saved on this device only", "");
    $("uOut").textContent = fb ? "Sign in" : "";
    $("uOut").classList.toggle("hidden", !fb);
  }
}
const ERR = {
  "auth/invalid-credential": "Wrong email or password.",
  "auth/wrong-password": "Wrong email or password.",
  "auth/user-not-found": "Wrong email or password.",
  "auth/invalid-email": "That email address doesn't look right.",
  "auth/missing-email": "Type your email address first.",
  "auth/missing-password": "Type your password.",
  "auth/email-already-in-use": "There's already an account with that email. Sign in instead, or tap “Forgot password?”.",
  "auth/weak-password": "Please use a password with at least 6 characters.",
  "auth/network-request-failed": "No connection. Check your internet and try again.",
  "auth/too-many-requests": "Too many tries. Wait a few minutes and try again.",
  "auth/operation-not-allowed": "Email sign-in isn't switched on for this site yet.",
  "auth/unauthorized-domain": "This web address isn't allowed to sign in yet.",
  "auth/user-disabled": "This account has been disabled."
};
const errText = (e) => ERR[e && e.code] || ("Something went wrong" + (e && e.code ? " (" + e.code + ")" : "") + ". Please try again.");

// ---------- merging (first sign-in on a device, or offline changes) ----------
function mergeDrills(l, c) {
  const out = Object.assign({}, c || {});
  l = l || {}; c = c || {};
  ["tab", "level", "cat", "mode", "vtheme", "vdrill"].forEach((k) => { if (l[k] != null) out[k] = l[k]; });
  out.best = Math.max(l.best || 0, c.best || 0);
  const items = Object.assign({}, c.items || {});
  Object.keys(l.items || {}).forEach((k) => {
    const a = l.items[k] || {}, b = items[k] || {};
    items[k] = { seen: Math.max(a.seen || 0, b.seen || 0), right: Math.max(a.right || 0, b.right || 0) };
  });
  out.items = items;
  return out;
}
function mergeLessons(l, c) {
  const out = { version: 1, lessons: Object.assign({}, (c && c.lessons) || {}) };
  const ll = (l && l.lessons) || {};
  Object.keys(ll).forEach((id) => {
    const a = ll[id] || {}, b = out.lessons[id];
    if (!b) { out.lessons[id] = a; return; }
    const newer = String(a.lastDate || "") > String(b.lastDate || "") ? a : b;
    out.lessons[id] = Object.assign({}, newer, {
      completed: !!(a.completed || b.completed),
      attempts: Math.max(a.attempts || 0, b.attempts || 0),
      best: Math.max(a.best || 0, b.best || 0),
      of: Math.max(a.of || 0, b.of || 0)
    });
  });
  return out;
}
function mergeWords(l, c) {
  if (!l || !Array.isArray(l.words)) return c || null;
  if (!c || !Array.isArray(c.words)) return l;
  const words = c.words.slice(), key = (w) => w.ru + "|" + w.theme;
  const have = new Set(words.map(key));
  l.words.forEach((w) => { if (!have.has(key(w))) words.push(w); });
  return { version: 1, words };
}
function parseDoc(d) {
  const p = (s, fb2) => { try { return s == null ? fb2 : JSON.parse(s); } catch (e) { return fb2; } };
  return { drills: p(d.drills, {}), lessons: p(d.lessons, { version: 1, lessons: {} }), words: p(d.words, null) };
}

// ---------- cloud I/O ----------
function ref() { return fb.doc(db, "users", user.uid); }
function payload() {
  const s = App.snapshot();
  return {
    v: 1,
    displayName: String(user.displayName || pendingName || (user.email || "Learner").split("@")[0]).slice(0, 60) || "Learner",
    drills: JSON.stringify(s.drills || {}),
    lessons: JSON.stringify(s.lessons || { version: 1, lessons: {} }),
    words: s.words ? JSON.stringify(s.words) : null,
    updatedAt: fb.serverTimestamp()
  };
}
function schedule() {
  if (!user || !live) return;
  gen++; setMeta({ uid: user.uid, dirty: true });
  sync("· saving…", "");
  clearTimeout(pushTimer); pushTimer = setTimeout(push, 1500);
}
async function push() {
  if (!user || !live || docExists === null) return;
  const my = gen, uid = user.uid, data = payload();
  if (!docExists) data.createdAt = fb.serverTimestamp();
  const p = docExists ? fb.setDoc(ref(), data, { merge: true }) : fb.setDoc(ref(), data);
  docExists = true;
  const slow = setTimeout(() => { if (ackGen < my) sync("· offline, saved on this device", "warn"); }, 4000);
  try {
    await p; clearTimeout(slow);
    if (!user || user.uid !== uid) return;
    ackGen = Math.max(ackGen, my);
    if (ackGen >= gen) { setMeta({ uid, dirty: false, synced: Date.now() }); sync("· ✓ synced", "ok"); }
  } catch (e) {
    clearTimeout(slow);
    console.warn("save failed", e);
    sync("· couldn't save to cloud (" + (e.code || "error") + ")", "bad");
  }
}
async function loadCloud() {
  live = false;
  const m = meta();
  if (m.uid && m.uid !== user.uid) { App.clearLocal(); App.apply({ drills: {}, lessons: null, words: null }); }
  sync("· loading…", "");
  let snap;
  try { snap = await fb.getDoc(ref()); }
  catch (e) {
    console.warn("load failed", e);
    docExists = null; live = true; setMeta({ uid: user.uid, dirty: App.hasLocalProgress() || !!m.dirty });
    sync("· offline, using this device's progress", "warn");
    return;
  }
  const localHas = App.hasLocalProgress();
  const firstHere = m.uid !== user.uid, dirty = !!m.dirty;
  if (!snap.exists()) {
    docExists = false; live = true; setMeta({ uid: user.uid, dirty: true });
    await push();
    if (localHas) toast("Your progress on this device is now saved to your account.");
    return;
  }
  docExists = true;
  const cloud = parseDoc(snap.data());
  let merged = cloud, needPush = false;
  if ((firstHere && localHas) || (!firstHere && dirty)) {
    const local = App.snapshot();
    merged = { drills: mergeDrills(local.drills, cloud.drills), lessons: mergeLessons(local.lessons, cloud.lessons), words: mergeWords(local.words, cloud.words) };
    needPush = true;
  }
  App.apply(merged);
  live = true; setMeta({ uid: user.uid, dirty: needPush });
  if (needPush) { gen++; await push(); if (firstHere) toast("Merged this device's progress into your account."); }
  else sync(snap.metadata.fromCache ? "· offline copy" : "· ✓ synced", snap.metadata.fromCache ? "warn" : "ok");
}
function toast(t) { const el = $("toast"); el.textContent = t; el.classList.remove("hidden"); clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.add("hidden"), 5000); }

// ---------- actions ----------
async function doSubmit(ev) {
  ev.preventDefault(); msg("");
  const email = $("aEmail").value.trim(), pass = $("aPass").value, name = $("aName").value.trim();
  if (mode === "up" && !name) { msg("Please type your name. It's shown at the top of the app.", "bad"); return; }
  if (!email) { msg(ERR["auth/missing-email"], "bad"); return; }
  if (!pass) { msg(ERR["auth/missing-password"], "bad"); return; }
  busy(true);
  try {
    if (mode === "up") {
      pendingName = name.slice(0, 60);
      const cred = await fb.createUserWithEmailAndPassword(auth, email, pass);
      try { await fb.updateProfile(cred.user, { displayName: pendingName }); } catch (e) {}
      if (user) { bar(); schedule(); }
    } else {
      await fb.signInWithEmailAndPassword(auth, email, pass);
    }
    $("aPass").value = "";
  } catch (e) { msg(errText(e), "bad"); }
  busy(false);
}
async function doForgot() {
  const email = $("aEmail").value.trim();
  if (!email) { msg("Type your email above, then tap “Forgot password?” again.", "bad"); $("aEmail").focus(); return; }
  busy(true);
  try { await fb.sendPasswordResetEmail(auth, email); msg("If there's an account for " + email + ", a reset link is on its way. Check your spam folder too.", "ok"); }
  catch (e) { msg(e.code === "auth/user-not-found" ? "If there's an account for " + email + ", a reset link is on its way." : errText(e), e.code === "auth/user-not-found" ? "ok" : "bad"); }
  busy(false);
}
async function doSignOut() {
  if (!user) { sessionStorage.removeItem(GUEST); setMode("in"); showOv("avForm"); return; }
  clearTimeout(pushTimer);
  if (meta().dirty) {
    await push();
    const ok = await Promise.race([fb.waitForPendingWrites(db).then(() => true), new Promise((r) => setTimeout(() => r(false), 3000))]);
    if (!ok && !confirm("Some progress hasn't reached the cloud yet (you seem to be offline). If you sign out now, it will be lost. Sign out anyway?")) return;
  }
  live = false;
  try { await fb.signOut(auth); } catch (e) {}
  try { await fb.terminate(db); await fb.clearIndexedDbPersistence(db); } catch (e) {}
  App.clearLocal(); try { localStorage.removeItem(LSC); } catch (e) {}
  location.reload();
}
function guest() { sessionStorage.setItem(GUEST, "1"); hideOv(); bar(); }

// ---------- boot ----------
function wire() {
  $("aForm").addEventListener("submit", doSubmit);
  $("aForgot").onclick = doForgot;
  $("aSwitch").onclick = () => setMode(mode === "up" ? "in" : "up");
  $("aShow").onclick = () => { const p = $("aPass"); p.type = p.type === "password" ? "text" : "password"; $("aShow").textContent = p.type === "password" ? "Show" : "Hide"; };
  $("aGuest").onclick = guest; $("fGuest").onclick = guest;
  $("fRetry").onclick = () => location.reload();
  $("uOut").onclick = doSignOut;
  App.onChange(() => schedule());
  window.addEventListener("online", () => { if (user && docExists === null) loadCloud(); else if (user && meta().dirty) push(); });
}
async function boot() {
  wire();
  if (!cfg) { hideOv(); $("userbar").classList.add("hidden"); return; }
  const failT = setTimeout(() => { if (!fb) { $("fText").textContent = "The sign-in service is taking a long time to load. You can keep waiting, or use the app on this device only for now."; showOv("avFail"); } }, 10000);
  try {
    const [a, b, c] = await Promise.all([import(SDK + "firebase-app.js"), import(SDK + "firebase-auth.js"), import(SDK + "firebase-firestore.js")]);
    fb = Object.assign({}, a, b, c);
  } catch (e) {
    clearTimeout(failT); console.warn("SDK load failed", e);
    $("fText").textContent = "Couldn't reach the sign-in service (no internet, or it's blocked on this network). You can use the app on this device; your progress is saved here.";
    showOv("avFail"); return;
  }
  clearTimeout(failT);
  const app = fb.initializeApp(cfg);
  auth = fb.getAuth(app); auth.languageCode = "en";
  try { db = fb.initializeFirestore(app, { localCache: fb.persistentLocalCache({ tabManager: fb.persistentMultipleTabManager() }) }); }
  catch (e) { db = fb.getFirestore(app); }
  const emu = new URLSearchParams(location.search).get("emu");
  if (emu && /^(localhost|127\.0\.0\.1)$/.test(location.hostname)) {
    fb.connectAuthEmulator(auth, "http://127.0.0.1:9099", { disableWarnings: true });
    fb.connectFirestoreEmulator(db, "127.0.0.1", 8080);
  }
  window.RuCloud = { get user() { return user; }, push, merge: { mergeDrills, mergeLessons, mergeWords } };
  fb.onAuthStateChanged(auth, async (u) => {
    user = u;
    if (u) { sessionStorage.removeItem(GUEST); hideOv(); bar(); await loadCloud(); }
    else { docExists = null; live = false; if (sessionStorage.getItem(GUEST)) { hideOv(); bar(); } else { setMode("in"); showOv("avForm"); bar(); } }
  });
}
boot();
