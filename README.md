# Stop My Auction Florida

Landing page for Probate Assets Elite, LLC. Live at [stopmyauctionflorida.com](https://stopmyauctionflorida.com).

We buy Florida homes for cash before foreclosure and tax deed auctions so owners can pay off what is owed, keep their equity, and move forward.

## Stack

Single static page (no build step) hosted on GitHub Pages with a custom domain.

- `index.html` — the landing page (all CSS and JS inline)
- `thanks.html` — form confirmation page
- `404.html` — custom not-found page
- `assets/` — logo, icons, social preview image
- Lead form posts to FormSubmit.co and delivers to the business inbox

## Editing

Brand colors live in the `:root` variables at the top of `index.html`. Phone number and email appear in several places; search and replace to change them.

## Lead source tracking

Print URLs like `stopmyauctionflorida.com/?src=letter-aug` on mailers. The `src` value rides along with each form submission, so every lead email shows which campaign produced it.
