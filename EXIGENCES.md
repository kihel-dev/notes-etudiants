# Exigences de sécurité de l'application des notes

| # | Exigence : « Le système doit… » | Vérification | Étape du SDLC | Test |
|---|---|---|---|---|
| 1 | traiter toute saisie de l'utilisateur comme une donnée, jamais comme du SQL (requêtes paramétrées) | Test automatique, Bandit | Développement | S1, S5 |
| 2 | refuser toute modification de note si l'utilisateur n'est pas identifié (code 401) | Test automatique | Développement | S2 |
| 3 | réserver la modification des notes aux enseignants (code 403 pour un étudiant) | Test automatique | Développement | S3 |
| 4 | n'autoriser un enseignant à modifier que les notes de son propre module (code 403 sinon) | Test automatique | Développement | S4 |
| 5 | n'accepter qu'une note numérique comprise entre 0 et 20 (code 400 sinon) | Test automatique | Développement | S5 |
| 6 | ne jamais afficher de détail technique dans une réponse d'erreur | Test automatique, revue de code | Développement | S7 |
| 7 | permettre à l'enseignant du module de modifier la note de son étudiant | Test automatique | Développement | S6 |
