# Carole Friendship Coach

Static website for **Action-Based Friendship Coaching** by Carole Stromboni.

Live site : [carolefriendshipcoach.com](https://carolefriendshipcoach.com)

## Structure

| Fichier | Rôle |
|---|---|
| `index.html` | Page d'accueil + offre + FAQ |
| `terms.html` | Conditions générales |
| `privacy.html` | Politique de confidentialité |
| `disclaimer.html` | Avertissement (coaching ≠ thérapie) |
| `refund-cancellation.html` | Remboursement et annulation |
| `thank-you.html` | Page après paiement Stripe |
| `intake.html` | Questions d'intake (envoyée au client après paiement) |
| `404.html` | Page d'erreur 404 |
| `Fcoaching.css` | Feuille de style unique (mobile-first, sans JS) |
| `CNAME` | Domaine personnalisé pour GitHub Pages |

## À remplacer avant le lancement

Cherche ces placeholders dans tous les fichiers `.html` :

- `[[ADD_STRIPE_CHECKOUT_URL]]` — lien Stripe Checkout (bouton "Start the program for $500" dans `index.html`)
- `[[ADD_CALENDLY_URL_BEFORE_LAUNCH]]` — lien Calendly (`thank-you.html`)
- `[[ADD_CONTACT_EMAIL_BEFORE_LAUNCH]]` — email de contact (toutes les pages légales)
- `[[ADD_EFFECTIVE_DATE_BEFORE_LAUNCH]]` — date d'entrée en vigueur des CGV
- `[[ADD_JURISDICTION_BEFORE_LAUNCH]]` — juridiction applicable (`terms.html`)
- `[[ADD_BIO_TEXT]]` — bio personnelle (`index.html`, section À propos)

## Images à ajouter

À déposer à la racine avant le déploiement :

- `favicon.ico` (32×32)
- `favicon.svg` (vectoriel, optionnel mais recommandé)
- `apple-touch-icon.png` (180×180)
- `og-image.jpg` (1200×630, pour les partages sur réseaux sociaux)

Outil rapide : [favicon.io](https://favicon.io) à partir de `Carolephotobio.jpg`.

## Déploiement (GitHub Pages)

1. Push le repo sur GitHub.
2. Settings → Pages → Source : `main` branch, `/ (root)`.
3. Custom domain : `carolefriendshipcoach.com` (le fichier `CNAME` est déjà là).
4. Activer **Enforce HTTPS**.
5. Côté DNS du domaine, créer un `CNAME` vers `<username>.github.io`.

## Stack

- HTML5 pur, aucun JavaScript
- CSS unique avec design tokens (variables CSS)
- Polices système (zéro requête externe)
- FAQ accessible via `<details>` natif

## Licence

Code et contenu © 2026 Carole Stromboni. Tous droits réservés.
