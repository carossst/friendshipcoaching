# The Friendship Practice

Static website for **The Friendship Practice**, a practical friendship coaching offer by Carole Stromboni.

Live site : [thefriendshippractice.com](https://thefriendshippractice.com)

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
| `seo-pages.json` | Source de vérité SEO par page |
| `SEO-PLAYBOOK.md` | Workflow SEO et statuts des pages |
| `IMPLEMENTATION_MEMORY.md` | Mémoire technique durable du projet |
| `scripts/` | Génération sitemap / robots / llms + validation SEO |
| `guides/` | Pages SEO éditoriales générées |
| `coding/CHANTIER_A_FAIRE.md` | Priorités et prochains chantiers |

## Mode actuel : liste d'attente

Le site est en mode **liste d'attente**. Le bouton principal pointe vers `#waitlist` (formulaire Kit). Stripe n'est pas encore actif.

Quand une place se libère :
- Remplacer `[[ADD_STRIPE_CHECKOUT_URL]]` par le lien Stripe Checkout dans `index.html`
- Mettre à jour la section `#waitlist` en `#price` dans index.html
- Mettre à jour les CTAs de nav dans les pages légales

Déjà renseignés :

- Email de contact : `contact@thefriendshippractice.com`
- Date d'entrée en vigueur : `January 7, 2026`
- Juridiction indiquée dans les Terms : `the State of Hawaii, United States`
- Page thank-you : bouton email vers `contact@thefriendshippractice.com`

## Images et icônes

Le site pointe vers un dossier `icons/` pour les favicons :

- `icons/favicon.svg`
- `icons/favicon.ico`
- `icons/favicon-32.png`
- `icons/favicon-16.png`
- `icons/apple-touch-icon.png`

L'image Open Graph utilisée par les balises sociales est :

- `icons/og-image.jpg`

## Déploiement (GitHub Pages)

1. Push le repo sur GitHub.
2. Settings → Pages → Source : `main` branch, `/ (root)`.
3. Custom domain : `thefriendshippractice.com` (le fichier `CNAME` est déjà là).
4. Activer **Enforce HTTPS**.
5. Côté DNS du domaine, créer un `CNAME` vers `<username>.github.io`.

## Stack

- HTML5 pur, aucun JavaScript
- CSS unique avec design tokens (variables CSS)
- Polices système (zéro requête externe)
- FAQ accessible via `<details>` natif

## SEO

- Générer les fichiers SEO :
  - `npm run publish:seo`
- Vérifier les balises des pages :
  - `npm run test:seo`
- Générer ou régénérer les guides SEO :
  - `npm run generate:guides`

## Licence

Code et contenu © 2026 Carole Stromboni. Tous droits réservés.
