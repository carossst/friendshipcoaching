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

## À remplacer avant le lancement

Il reste uniquement ce placeholder dans les fichiers `.html` :

- `[[ADD_STRIPE_CHECKOUT_URL]]` - lien Stripe Checkout (bouton "Start the program for $500" dans `index.html`)

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

L'image Open Graph reste attendue à la racine :

- `og-image.jpg`

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

## Licence

Code et contenu © 2026 Carole Stromboni. Tous droits réservés.
