# Shyamal & Tropa · web invitation

One page for every guest: palace doors with a marigold toran that open on tap into a
petal shower, then the invitation, a live countdown, both celebrations with
"add to calendar" buttons, the venue with Google Maps, and a Share button.
Plain HTML/CSS/JS in `index.html`, no build step.

There are two ways to put it online. Both serve this same `index.html`.

## Option A: Streamlit Community Cloud

`shyamal-invitation-app.py` (in the repo root) shows this page full-screen, with
Streamlit's header and padding hidden.

1. Go to <https://share.streamlit.io> → **Create app** → **Deploy a public app from GitHub**.
2. Repository: `bhuiyanmobasshir94/wedding-ceremony-card-generator`, branch `main`
   (or `add-shyamal-app` before the PR is merged).
3. Main file path: `shyamal-invitation-app.py`.
4. App URL: pick something like `shyamal-tropa` → `https://shyamal-tropa.streamlit.app`.
5. **Deploy**. The existing `requirements.txt` is enough.

Things to know:
- Free Community Cloud apps **go to sleep after 12 hours without visitors**. The
  next guest then sees a "wake this app up" button and waits about 30 seconds.
  Open the link yourself now and then, or share it in bursts.
- WhatsApp/Messenger show Streamlit's generic preview for the link, not the
  maroon card in `og-image.jpg`.

## Option B: Netlify (never sleeps, shows the maroon link preview)

**Drag and drop (2 minutes):**
1. Sign in at <https://app.netlify.com/drop>.
2. Drag this `shyamal-invitation` folder onto the page. It goes live straight away.
3. **Site configuration → Change site name** → e.g. `shyamal-tropa` →
   `https://shyamal-tropa.netlify.app`.

**Or from GitHub (redeploys on every push):** **Add new site → Import an existing
project → GitHub** → pick this repo. `netlify.toml` in the repo root already
publishes this folder, so leave the build settings empty and click **Deploy**.

**Then, for the link preview:** in `index.html`, replace each `YOUR-SITE.netlify.app`
(in the `og:` and `twitter:` tags near the top) with your real address, and deploy again.

## Editing

Dates, venue, map search and music are in the `CONFIG` block at the bottom of
`index.html`.

- **Music:** put an mp3 next to `index.html` and set `music: "music.mp3"`. A play/pause
  button appears and the music starts when the doors open.
- **Shubho Bibaho location:** no time or separate venue was given, so it goes into
  calendars as an all-day event without a location. If it is also at the restaurant,
  set `atVenue: true`.
