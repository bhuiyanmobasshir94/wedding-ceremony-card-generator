# Shyamal & Tropa · web invitation

A single-page wedding invitation: palace doors with a marigold toran that open on tap,
a falling-petal shower, the invitation itself, a live countdown, both celebrations with
"add to calendar" buttons, the venue with Google Maps, and a share button.
Plain HTML/CSS/JS, no build step.

## Deploy

**Netlify, drag and drop:** open <https://app.netlify.com/drop> and drop this
`shyamal-invitation` folder.

**Netlify, from GitHub:** "Add new site → Import an existing project" and pick this repo.
`netlify.toml` at the repo root already tells Netlify to publish this folder.

Then, in Site settings, rename the site to something like `shyamal-tropa`.

## After deploying

1. In `index.html`, replace every `YOUR-SITE.netlify.app` with your real address
   (in the `og:` and `twitter:` tags near the top). This is what makes WhatsApp and
   Messenger show the maroon preview card (`og-image.jpg`) when the link is shared.
2. In `shyamal-app.py`, set `INVITATION_SITE_URL` to the same address. The card
   generator will then also give a personalised web link for every guest.

## Personalised links

Add `?to=` and the guest's name to the address:

```
https://shyamal-tropa.netlify.app/?to=Mr.%20Rahim%20Uddin
```

The doors then greet "Dear Mr. Rahim Uddin", and so does the invitation. The page's own
Share button always shares the plain link, so a guest who forwards it never passes on
their name.

## Editing

Dates, venue, map search and music are in the `CONFIG` block at the bottom of
`index.html`.

- **Music:** put an mp3 next to `index.html` and set `music: "music.mp3"`. A play/pause
  button appears and the music starts when the doors open.
- **Shubho Bibaho location:** no time or separate venue was given, so it is added to
  calendars as an all-day event without a location. If it is also at the restaurant,
  set `atVenue: true`.
