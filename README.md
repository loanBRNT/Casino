# Casino

Par BERNAT Loan & GAUDILLAT Eliott

--

L'objectif de ce projet est de mettre en place une première ébauche de casino en ligne.

Nous avons 2 agents qui intéragissent avec un troisième agent, le whiteboard : 
- Le serveur : Permets de lancer la game.
- Le joueur : Permets de se connecter à la game.

Il est possible de jouer avec plusieurs joueurs. Mais nous n'avons pas eu le temps d'implémenter une fonctionalité de pseudonyme pour les joueurs afin de les différencier dans les statistiques.

Voici également d'autres éléments que nous n'avons pas eu le temps d'implémenter mais auxquels nous avons pensé : 
- Statistiques des derniers tirages.
- Que le serveur attende qu'il y ait au moins un joueur de connecté avant de lancer la partie.
- Le chat entre les joueurs.
- Faire tourner la roue lors du tirage.

Pensez à lancer la plateforme ingescape circle et à vérifier que la sortie de l'agent serveur est bien relié à l'entrée titre du Whiteboard. Ensuite, vous pouvez exécuter les agents.

--

##Comment jouer ?

Il sera nécéssaire d'installer pygame. Vous pouvez lancez les deux agents dans n'importe quel ordre.
Pour jouer, il vous suffit de sélectionner une mise sur la fenêtre joueur puis de cliquer à l'endroit où vous souhaitez déposer votre mise.

Si votre mise est prise en compte, un message s'affiche sur le whiteboard et l'argent est débité de votre solde (visible en bas à gauche).
