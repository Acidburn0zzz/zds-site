# Messages flash


Un message dit "flash" est un message d'information ou d'alerte qui est masquable selon la volonté de l'utilisateur et qui disparraîtra généralement à la page suivante (comportement selon le _back-end_).


## Utilisation de base

Le texte placé dans le bouton de fermeture est présent pour des raisons d'accessibilité. Il n'est pas visible par défaut.

Il y a trois couleurs : 

- rouge, pour les erreurs `alert-box error`
- orange, pour les alertes/avertissements `alert-box warning`
- vert, pour les succès/confirmations `alert-box success`

<div class="alert-box error">
    Votre formulaire n'est pas bien rempli !
    <button class="close-alert-box ico-after cross white">Masquer l'alerte</button>
</div>

<div class="alert-box alert">
    <strong>Attention</strong>, vous modifiez un contenu sensible.
    <button class="close-alert-box ico-after cross white">Masquer l'alerte</button>
</div>

<div class="alert-box success">
    Votre message a été envoyé.
    <button class="close-alert-box ico-after cross white">Masquer l'alerte</button>
</div>

Code des exemples : 

```html
<!-- Changez simplement la classe "success" pour une autre pour changer le fond -->
<div class="alert-box success">
    Votre message ici.
    <button class="close-alert-box ico-after cross white">Masquer l'alerte</button>
</div>
```

## Modulation

Il est possible de forcer l'affichage du texte à la place ou en plus de la croix en rajoutant la classe `close-alert-box-text` au bouton de fermeture.

<div class="alert-box success">
    Pas d'icône, juste du texte.
    <button class="close-alert-box close-alert-box-text">Masquer l'alerte</button>
</div>

Code de l'exemple : 

```html
<div class="alert-box success">
    Pas d'icône, juste du texte.
    <button class="close-alert-box close-alert-box-text">Masquer l'alerte</button>
</div>
```

Vous pouvez combiner icône et texte comme ceci : 

<div class="alert-box success">
    Croix + texte.
    <button class="close-alert-box close-alert-box-text ico-after cross white">Masquer l'alerte</button>
</div>

Code de l'exemple : 

```html
<div class="alert-box success">
    Croix + texte.
    <button class="close-alert-box close-alert-box-text ico-after cross white">Masquer l'alerte</button>
</div>
```