# Chantier À Faire

Ce fichier sert de liste de travail priorisée pour The Friendship Practice.

Règle simple :
- garder ce document orienté action
- supprimer ou déplacer ce qui est terminé
- ne pas transformer ce fichier en journal

## Priorité 1

- Remplacer le placeholder Stripe `[[ADD_STRIPE_CHECKOUT_URL]]` dans `index.html`.
- Vérifier que `challenge.html` doit bien rester indexable maintenant qu’il est dans le sitemap.
- Déployer la nouvelle couche SEO et contrôler les pages en production.
- Vérifier que `icons/og-image.jpg` s’affiche correctement dans les partages sociaux.

## Priorité 2

- Ajouter une deuxième vague de guides SEO :
  - `how to keep friends as an adult`
  - `how to be a better friend`
  - `how to meet people in a new city`
  - `how to make friends after 30`
- Ajouter du maillage interne entre guides, pas seulement depuis la home.
- Ajouter un bloc “Related guides” ou “Start here” sur `challenge.html` si cela reste cohérent produit.

## Priorité 3

- Revoir les balises `title` et `meta description` après premiers retours Search Console.
- Ajouter un vrai contrôle de qualité éditoriale pour éviter les pages trop proches sémantiquement.
- Définir quels contenus doivent rester purement top-of-funnel et lesquels peuvent mener vers l’offre coaching.
- Préparer une page auteur / à propos plus SEO si nécessaire.

## Produit / Conversion

- Clarifier si le parcours principal doit pousser :
  - le challenge gratuit
  - la waitlist
  - la session payante
- Vérifier si le challenge doit renvoyer explicitement vers la waitlist ou vers l’offre coaching.
- Mesurer si les guides convertissent vers :
  - clic challenge
  - inscription email
  - demande coaching

## Technique

- Initialiser un repo git pour ce dossier si tu veux un historique propre.
- Documenter un workflow de déploiement GitHub Pages réel, pas seulement théorique.
- Ajouter une vérification simple pour détecter les divergences entre HTML statique et `seo-pages.json`.
- Évaluer si `robots.txt` doit continuer à autoriser explicitement certains bots IA.

## À Ne Pas Faire Sans Réflexion

- Ne pas éditer les fichiers dans `guides/` à la main.
- Ne pas indexer les pages transactionnelles.
- Ne pas écrire des pages SEO qui font croire à une prise en charge thérapeutique.
- Ne pas multiplier des guides quasi duplicatifs juste pour “faire du volume”.
