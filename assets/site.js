/* ELVORO GOLF — interactions. Subtle motion only. */
(function () {
  "use strict";

  /* ---- Analytics (privacy-conscious GA4) ----
     Set GA_ID to your GA4 Measurement ID (looks like "G-ABC123XYZ") to turn it on.
     Stays completely dormant until then, and never loads if the visitor has
     Do-Not-Track enabled. IP anonymization is forced on. One line, every page. */
  var GA_ID = "G-XXXXXXXXXX";
  (function () {
    var dnt = navigator.doNotTrack == "1" || window.doNotTrack == "1" || navigator.msDoNotTrack == "1";
    if (!GA_ID || GA_ID.indexOf("XXXX") !== -1 || dnt) return;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA_ID, { anonymize_ip: true });
  })();
  function track(name, params) { if (window.gtag) window.gtag("event", name, params || {}); }

  /* ---- Header: solid on scroll ---- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      if (window.scrollY > 40) header.classList.add("is-solid");
      else header.classList.remove("is-solid");
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- Mobile nav toggle ---- */
  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      document.body.classList.toggle("nav-open");
      var open = document.body.classList.contains("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".nav-link").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ---- Reveal on scroll ---- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- Email capture / forms — delivered via FormSubmit.co ---- */
  /* FormSubmit random-string alias — hides the destination inbox from scrapers */
  var FORM_ENDPOINT = "https://formsubmit.co/ajax/939083f9927a031c7a6c93dad38d05df";

  function sendForm(payload) {
    return fetch(FORM_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    }).then(function (json) {
      var ok = json && (json.success === true || json.success === "true");
      if (!ok) throw new Error((json && json.message) || "Submission failed");
      return json;
    });
  }

  /* ---- Mailing list — Mailchimp audience ----
     Signups POST straight into a Mailchimp audience, so you have a real list to
     broadcast from (campaigns + automations) — not just inbox forwards.

     TO TURN IT ON — two values from your Mailchimp audience:
       Audience → Signup forms → Embedded forms → Continue.
       1) Copy the <form action="..."> URL into `action` below. It looks like:
          https://elvoro.us21.list-manage.com/subscribe/post?u=abc123def&id=456ghi
       2) In that same form's HTML there's a hidden anti-bot field near the end,
          e.g. <input type="text" name="b_abc123def_456ghi" ...>. Copy that
          field's name into `botField`.
     Until `action` is filled in, signups fall back to the FormSubmit inbox below,
     so the live site keeps working unchanged.

     Optional: to store size + product interest, add audience merge fields with
     tags SIZE and PRODUCT (Audience → Settings → Audience fields). If you skip
     this, those values are simply ignored by Mailchimp. */
  var MAILCHIMP = {
    action: "",
    botField: ""
  };

  // Mailchimp's endpoint sends no CORS headers, so a normal fetch() POST is
  // blocked from a static site. JSONP against the post-json endpoint is the
  // supported no-server pattern.
  var mcSeq = 0;
  function sendMailchimp(data) {
    return new Promise(function (resolve, reject) {
      if (!MAILCHIMP.action) { reject(new Error("Mailchimp not configured")); return; }
      var url = MAILCHIMP.action.replace("/post?", "/post-json?").replace(/\/post$/, "/post-json");
      var cb = "mc_cb_" + (++mcSeq);
      var parts = ["EMAIL=" + encodeURIComponent(data.email)];
      if (data.size) parts.push("SIZE=" + encodeURIComponent(data.size));
      if (data.product) parts.push("PRODUCT=" + encodeURIComponent(data.product));
      if (MAILCHIMP.botField) parts.push(encodeURIComponent(MAILCHIMP.botField) + "=");
      parts.push("c=" + cb);
      var script = document.createElement("script");
      var done = false;
      var cleanup = function () {
        try { delete window[cb]; } catch (e) { window[cb] = undefined; }
        if (script.parentNode) script.parentNode.removeChild(script);
      };
      window[cb] = function (resp) {
        done = true; cleanup();
        // {result:"success"|"error", msg:"…"}. An "already subscribed" error
        // still means the address is on the list, so treat it as success.
        var already = resp && resp.msg && /already/i.test(resp.msg);
        if (resp && (resp.result === "success" || already)) resolve(resp);
        else reject(new Error((resp && resp.msg) || "Subscription failed"));
      };
      script.onerror = function () { if (!done) { cleanup(); reject(new Error("Network error")); } };
      script.src = url + (url.indexOf("?") === -1 ? "?" : "&") + parts.join("&");
      document.head.appendChild(script);
      setTimeout(function () { if (!done) { cleanup(); reject(new Error("Timeout")); } }, 10000);
    });
  }

  document.querySelectorAll("form[data-capture]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector(".form-success");
      var email = form.querySelector('input[type="email"]');
      var btn = form.querySelector('button[type="submit"]');
      var honeypot = form.querySelector('input[name="company"]');
      // Bots fill the hidden field — pretend success, send nothing.
      if (honeypot && honeypot.value) {
        if (note) note.textContent = "You're on the list — we'll email you before Drop One opens, with your 25% founding-member code.";
        form.reset();
        return;
      }
      if (email && !email.checkValidity()) { email.reportValidity(); return; }
      if (btn) btn.disabled = true;
      if (note) note.textContent = "Adding you to the list…";

      var product = form.dataset.product || "";
      var sizeEl = form.querySelector('select[name="size"]');
      var size = (sizeEl && sizeEl.value) || "";

      // Same payload the inbox has always received — kept as a live notification
      // when Mailchimp is on, and the full fallback when it isn't configured yet.
      var payload = {
        email: email.value,
        _subject: product
          ? "Elvoro Golf — notify request: " + product
          : "Elvoro Golf — new mailing list signup",
        _template: "table"
      };
      if (product) payload.product = product;
      if (size) payload.size = size;

      var subscribe = MAILCHIMP.action
        ? sendMailchimp({ email: email.value, size: size, product: product })
            .then(function (r) { sendForm(payload).catch(function () {}); return r; })
        : sendForm(payload);

      subscribe.then(function () {
        if (note) note.textContent = "You're on the list — we'll email you before Drop One opens, with your 25% founding-member code.";
        track(product ? "notify_signup" : "list_signup",
              product ? { product: product, size: size || "unspecified" } : {});
        form.reset();
      }).catch(function () {
        if (note) note.textContent = "Something went wrong — please try again in a moment.";
      }).finally(function () {
        if (btn) btn.disabled = false;
      });
    });
  });

  document.querySelectorAll("form[data-contact]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector(".form-success");
      var btn = form.querySelector('button[type="submit"]');
      var honeypot = form.querySelector('input[name="company"]');
      // Bots fill the hidden field — pretend success, send nothing.
      if (honeypot && honeypot.value) {
        if (note) note.textContent = "Message received. We'll reply within one business day.";
        form.reset();
        return;
      }
      var fields = ["name", "email", "topic", "message"].reduce(function (acc, key) {
        var el = form.querySelector('[name="' + key + '"]');
        if (el) acc[key] = el.value;
        return acc;
      }, {});
      var emailEl = form.querySelector('input[type="email"]');
      if (emailEl && !emailEl.checkValidity()) { emailEl.reportValidity(); return; }
      if (btn) btn.disabled = true;
      if (note) note.textContent = "Sending…";
      fields._subject = "Elvoro Golf — contact form: " + (fields.topic || "General");
      fields._template = "table";
      sendForm(fields).then(function () {
        if (note) note.textContent = "Message received. We'll reply within one business day.";
        track("contact_submit", { topic: fields.topic || "General" });
        form.reset();
      }).catch(function () {
        if (note) note.textContent = "Something went wrong — please try again, or email us directly.";
      }).finally(function () {
        if (btn) btn.disabled = false;
      });
    });
  });

  /* ---- Hero video: fade in once it can render, only if motion is allowed ---- */
  var heroVideo = document.querySelector(".hero-video");
  if (heroVideo) {
    var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduceMotion) {
      heroVideo.removeAttribute("autoplay");
      heroVideo.pause && heroVideo.pause();
    } else {
      var reveal = function () { heroVideo.classList.add("is-ready"); };
      if (heroVideo.readyState >= 2) reveal();
      else heroVideo.addEventListener("loadeddata", reveal, { once: true });
    }
  }

  /* ---- Coming-soon / 404 background video: fade in, respect reduced motion ---- */
  var comingVideo = document.querySelector(".coming-video");
  if (comingVideo) {
    var reduceMo = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduceMo) {
      comingVideo.removeAttribute("autoplay");
      comingVideo.pause && comingVideo.pause();
    } else {
      var showC = function () { comingVideo.classList.add("is-ready"); };
      if (comingVideo.readyState >= 2) showC();
      else comingVideo.addEventListener("loadeddata", showC, { once: true });
      var pc = comingVideo.play && comingVideo.play(); if (pc && pc.catch) pc.catch(function () {});
    }
  }

  /* ---- Ambient interlude video: defer load until near viewport ---- */
  var ambient = document.querySelector(".ambient-video");
  if (ambient) {
    var noMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!noMotion) {
      var startAmbient = function () {
        if (ambient.dataset.started) return;
        ambient.dataset.started = "1";
        ambient.setAttribute("preload", "auto");
        ambient.load();
        var show = function () { ambient.classList.add("is-ready"); };
        ambient.addEventListener("loadeddata", show, { once: true });
        var p = ambient.play(); if (p && p.catch) p.catch(function () {});
      };
      if ("IntersectionObserver" in window) {
        var ao = new IntersectionObserver(function (entries) {
          entries.forEach(function (e) { if (e.isIntersecting) { startAmbient(); ao.disconnect(); } });
        }, { rootMargin: "300px 0px" });
        ao.observe(ambient);
      } else { startAmbient(); }
    }
  }

  /* ---- Footer year ---- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---- Policy nav scroll-spy ---- */
  var policyLinks = document.querySelectorAll(".policy-nav a");
  if (policyLinks.length && "IntersectionObserver" in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          policyLinks.forEach(function (l) {
            l.classList.toggle("active", l.getAttribute("href") === "#" + e.target.id);
          });
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    document.querySelectorAll(".policy-body h2[id]").forEach(function (h) { spy.observe(h); });
  }
})();
