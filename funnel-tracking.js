(function () {
  "use strict";

  var initialPath = window.location.pathname;
  var initialSearch = window.location.search;
  var challengePage = /(?:^|\/)challenge\.html$/.test(initialPath) || /\/fr\/defi\.html$/.test(initialPath);
  var unlockedOnArrival = /(?:^|[?&])unlocked=1(?:&|$)/.test(initialSearch);

  function sourceKey() {
    var key = initialPath
      .replace(/^\/+|\/+$/g, "")
      .replace(/\.html$/i, "")
      .replace(/\//g, "_");

    if (!key || key === "index") return "home";
    if (key === "fr_index") return "fr-home";
    return key.slice(0, 90);
  }

  function sendEvent(action, title) {
    var attempts = 0;
    var eventPath = "funnel-" + action + "@" + sourceKey();

    function sendWhenReady() {
      if (window.goatcounter && typeof window.goatcounter.count === "function") {
        window.goatcounter.count({
          path: eventPath,
          title: title,
          event: true
        });
        return;
      }

      attempts += 1;
      if (attempts < 50) {
        window.setTimeout(sendWhenReady, 100);
      }
    }

    sendWhenReady();
  }

  function sameSiteUrl(href) {
    try {
      var url = new URL(href, window.location.href);
      return url.origin === window.location.origin ? url : null;
    } catch (error) {
      return null;
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (unlockedOnArrival && challengePage) {
      sendEvent("challenge-unlocked", "Challenge unlocked after email signup");
    }

    document.addEventListener("click", function (event) {
      var link = event.target && event.target.closest ? event.target.closest("a[href]") : null;
      if (!link) return;

      var url = sameSiteUrl(link.getAttribute("href"));
      if (!url) return;

      if (url.pathname === "/challenge.html" || url.pathname === "/fr/defi.html") {
        sendEvent("challenge-cta", "Challenge CTA click");
        return;
      }

      if (
        url.pathname === "/guides/what-is-friendship-coaching/" ||
        url.pathname === "/fr/guides/quest-ce-que-le-coaching-en-amitie/" ||
        url.hash === "#coaching" ||
        url.hash === "#programme"
      ) {
        sendEvent("coaching-interest", "Coaching interest click");
      }
    }, true);

    document.addEventListener("submit", function (event) {
      var form = event.target;
      if (!form || !form.classList || !form.classList.contains("formkit-form")) return;

      sendEvent(
        challengePage ? "challenge-form-submit" : "kit-form-submit",
        challengePage ? "Challenge email form submitted" : "Kit form submitted"
      );
    }, true);

    if (challengePage) {
      document.addEventListener("change", function (event) {
        var target = event.target;
        if (!target || !target.matches || !target.matches("[data-complete]") || !target.checked) return;

        var day = target.closest("[data-day]");
        if (day && day.getAttribute("data-day") === "7") {
          sendEvent("challenge-complete", "7-day challenge completed");
        }
      }, true);
    }
  });
}());
