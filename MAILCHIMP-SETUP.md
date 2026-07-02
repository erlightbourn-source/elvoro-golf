# Mailing list setup (Mailchimp)

The site's signup forms are wired to drop every address into a Mailchimp
audience — a real list you can send campaigns and automations from. Until you
paste in the two values below, signups keep flowing to the FormSubmit inbox
exactly as before, so the live site is never broken mid-setup.

## One-time setup (~5 minutes)

1. Create a free Mailchimp account and an **Audience** (name it "Elvoro Golf").
2. In Mailchimp: **Audience → Signup forms → Embedded forms → Continue**.
3. In the generated form HTML, find two things:
   - The `<form action="...">` URL. It looks like:
     `https://elvoro.us21.list-manage.com/subscribe/post?u=abc123def&id=456ghi`
   - A hidden anti-bot input near the bottom, e.g.
     `<input type="text" name="b_abc123def_456ghi" tabindex="-1" value="">`.
     You want its `name` (`b_abc123def_456ghi`).
4. Open `assets/site.js`, find the `MAILCHIMP` block near the top, and paste:
   ```js
   var MAILCHIMP = {
     action: "https://elvoro.us21.list-manage.com/subscribe/post?u=abc123def&id=456ghi",
     botField: "b_abc123def_456ghi"
   };
   ```
5. Commit + push. GitHub Pages redeploys and new signups land in Mailchimp.

## Optional: capture size + product interest

Product-page notify forms already collect a size, and each form knows which polo
it's for. To store those in Mailchimp, add two **audience fields**
(**Audience → Settings → Audience fields and *|MERGE|* tags**) with the tags:

- `SIZE` — the size chosen on a product notify form
- `PRODUCT` — which polo the signup came from (e.g. "The Evergreen Polo")

If you don't add them, the values are just ignored — nothing breaks.

## How it behaves

- **Configured:** signup → Mailchimp audience (primary list) **and** a best-effort
  FormSubmit note to your Gmail, so you still see signups land in real time.
- **Not configured:** signup → FormSubmit → Gmail, exactly like today.
- "Already subscribed" is treated as success, so repeat signups don't show errors.

## Sending your first campaign

Once addresses are flowing in, in Mailchimp: **Create → Email → Regular**, pick
the audience, and send. For the launch, a simple 2–3 email automation works well:
welcome on signup, a heads-up a few days before Drop One, and the "it's live"
email on launch day.
