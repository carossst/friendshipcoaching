# Chantier À Faire

Ce fichier sert de liste de travail priorisée pour The Friendship Practice.

Règle simple :
- garder ce document orienté action
- supprimer ou déplacer ce qui est terminé
- ne pas transformer ce fichier en journal

## Plan business (novembre 2026)

### Le constat

Le site attire et inscrit (guides SEO, quiz, défi gratuit de 7 jours, version française), mais il ne vend pas encore : l'offre à 500 $ est annoncée « quand une place se libère », sans lien de réservation ni de paiement, et le site n'affiche aucun témoignage. Le plan ci-dessous vise à transformer cette audience en clients.

### Fait

- Message de l'accueil (EN et FR) : on ouvre sur ce que le visiteur veut (se faire des amis, renouer, approfondir) et la responsabilité personnelle reste présente comme moyen d'y arriver, pas comme accroche.
- Fin du défi et page de confirmation (EN et FR) : une façon concrète de demander une place, en répondant à un email du défi avec le mot « coaching ».
- Séquences Kit (EN et FR), fait directement dans Kit :
  - jour 5 : P.S. qui relie l'exercice au coaching
  - jour 7 : présentation de l'offre (4 séances, 500 $)
  - jour 8 : choix entre continuer seul et demander un coaching, par réponse « coaching »
  - jour 9 : question personnelle sans offre (« qu'avez-vous essayé depuis ? »)

Règle retenue : une seule façon de demander une place, la réponse « coaching » par email. Logique de la séquence : présenter l'offre, laisser le choix, puis ouvrir une conversation.

### À faire, par ordre d'impact

1. **Tester la réception des réponses.** Envoyer un message à `carole@thefriendshippractice.com` depuis une autre adresse et répondre à un vrai email du défi. Tout l'appel à l'action repose sur cette boîte.
2. **Suivre les demandes.** Ajouter à la main un tag Kit (par exemple `coaching-demande`) à chaque réponse « coaching ». Vérifier si un automatisme dépendait de l'ancien déclencheur `5715826` du jour 8 anglais et le rattacher à ce tag.
3. **Obtenir 3 à 5 témoignages.** Coacher des clients pilotes, gratuitement ou à prix réduit, contre un témoignage détaillé (situation de départ, ce qui a changé). Puis ajouter une section témoignages sur l'accueil EN et FR. C'est le manque le plus coûteux en conversion.
4. **Ouvrir la vente.** Remplacer « quand une place se libère » par un appel découverte gratuit de 20 minutes (Calendly), suivi du lien Stripe. À 500 $, on n'achète pas sans avoir parlé à la personne. La rareté reste possible (« 3 places par mois »), mais avec un bouton qui fonctionne.
5. **Créer une offre intermédiaire.** Entre le défi gratuit et les 500 $, il n'y a rien. Tester une séance unique (120 à 150 $) ou un atelier de groupe (49 à 79 $), où les participants se rencontrent aussi entre eux.
6. **Relier le quiz à une suite personnalisée.** Chacun des 4 profils (rencontrer, relancer, réciprocité, nouvelle ville) mène au guide correspondant et à une inscription email taguée par profil.
7. **Choisir une niche d'entrée.** « L'amitié pour les adultes » est large. Expatriés et amitiés à distance : crédibilité personnelle (Hawaï et Paris), public solvable, atout bilingue.
8. **Sortir du tout-SEO.** Podcasts invités, presse, LinkedIn, en s'appuyant sur le livre Eyrolles et les 77 épisodes de podcast.
9. **Tester le B2B.** Ateliers sur les liens entre collègues en télétravail ou l'intégration d'expatriés. Un contrat vaut plusieurs clients particuliers.

### Ce qu'on mesure

- inscrits au défi par mois
- réponses « coaching » par rapport aux inscrits
- appels découverte, puis clients
- quels guides amènent réellement des inscrits, avant d'en écrire d'autres

Le suivi GoatCounter (`funnel-tracking.js`) couvre déjà les clics vers le défi et vers l'offre. Les réponses et les ventes se comptent à la main pour l'instant.

## Priorité 1

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
