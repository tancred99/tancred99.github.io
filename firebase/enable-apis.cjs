// Enables the Google APIs this site needs, using the Firebase CLI's own login.
const path = process.env.FT || "firebase-tools";
const { requireAuth } = require(path + "/lib/requireAuth");
const { selectAccount } = require(path + "/lib/auth");
const { ensure } = require(path + "/lib/ensureApiEnabled");
(async () => {
  const project = process.argv[2];
  const acct = selectAccount(undefined, __dirname) || {};
  await requireAuth({ project, projectId: project, user: acct.user, tokens: acct.tokens });
  for (const api of ["firestore.googleapis.com", "identitytoolkit.googleapis.com"]) {
    await ensure(project, api, "setup", false); console.log("enabled", api);
  }
})().catch((e) => { console.error("FAILED:", e.message); process.exit(1); });
