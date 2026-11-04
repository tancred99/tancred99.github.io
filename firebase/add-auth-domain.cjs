// Adds a domain to Firebase Auth's authorized domains using the Firebase CLI's own login.
// Usage: node add-auth-domain.cjs <projectId> <domain>   (needs firebase-tools installed: NODE_PATH or local node_modules)
const path = process.env.FT || "firebase-tools";
const { requireAuth } = require(path + "/lib/requireAuth");
const { selectAccount } = require(path + "/lib/auth");
const { getAuthDomains, updateAuthDomains } = require(path + "/lib/gcp/auth");
(async () => {
  const [project, domain] = process.argv.slice(2);
  const acct = selectAccount(undefined, __dirname) || {};
  await requireAuth({ project, projectId: project, user: acct.user, tokens: acct.tokens });
  const cur = (await getAuthDomains(project)) || [];
  if (cur.includes(domain)) { console.log("already authorized:", cur.join(", ")); return; }
  const out = await updateAuthDomains(project, cur.concat(domain));
  console.log("authorized domains:", out.join(", "));
})().catch((e) => { console.error("FAILED:", e.message); process.exit(1); });
