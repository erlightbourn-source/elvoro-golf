/* ELVORO GOLF — interactions. Subtle motion only. */
(function () {
  "use strict";

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
  var FORM_ENDPOINT = "https://formsubmit.co/ajax/d32e4dad5c35cab7cb74c858a6943793";

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

  document.querySelectorAll("form[data-capture]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector(".form-success");
      var email = form.querySelector('input[type="email"]');
      var btn = form.querySelector('button[type="submit"]');
      if (email && !email.checkValidity()) { email.reportValidity(); return; }
      if (btn) btn.disabled = true;
      if (note) note.textContent = "Adding you to the list…";
      var payload = {
        email: email.value,
        _subject: form.dataset.product
          ? "Elvoro Golf — notify request: " + form.dataset.product
          : "Elvoro Golf — new mailing list signup",
        _template: "table"
      };
      if (form.dataset.product) payload.product = form.dataset.product;
      sendForm(payload).then(function () {
        if (note) note.textContent = "Thank you — you're on the list. We'll be in touch.";
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
        form.reset();
      }).catch(function () {
        if (note) note.textContent = "Something went wrong — please try again, or email us directly.";
      }).finally(function () {
        if (btn) btn.disabled = false;
      });
    });
  });

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
