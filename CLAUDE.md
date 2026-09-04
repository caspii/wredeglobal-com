# CLAUDE.md

Plain static HTML site for wredeglobal.com, deployed to GitHub Pages by
`.github/workflows/deploy.yml` on every push to `main`. See `README.md` for how
to edit, preview and rebuild the icons.

## DNS: this repo can edit its own Cloudflare records

`.env` holds `CLOUDFLARE_API_TOKEN`. It is gitignored — never commit it, never
paste it into a file, a commit message, or a chat message.

The zone ID for wredeglobal.com is `917b51e1a40acb44ea6eb4f7de268a5f`. There is
no CLI and no MCP server; call the API with `curl`:

```sh
set -a; source .env; set +a
ZONE=917b51e1a40acb44ea6eb4f7de268a5f

# List
curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | python3 -m json.tool

# Create
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"wredeglobal.com","content":"185.199.108.153","proxied":false,"ttl":1}'
```

### The token is scoped to this domain only

Verified 04.09.2026: it has `Zone` · `DNS` · `Edit` on wredeglobal.com and
nothing else. Requests to any other zone — keepthescore.com, leaderboarded.com,
scorejudge.com, rise.global, qrpage.co — come back `10000 Authentication error`,
and listing zones returns wredeglobal.com alone. You cannot damage a production
domain with it.

### What the records should be

The site is GitHub Pages on the apex domain (`CNAME` file says
`wredeglobal.com`), so the zone needs the four GitHub Pages A records —
`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` —
plus a `CNAME` for `www` pointing at the Pages host.

Keep them unproxied (`"proxied": false`) at least until GitHub has issued the
HTTPS certificate; Cloudflare's proxy hides the origin and the certificate
check fails.
