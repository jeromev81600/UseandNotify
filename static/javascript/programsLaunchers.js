function launchDiscord() {
    // Exécuter une requête HTTP vers le serveur Flask pour lancer Discord
    fetch('/launch_discord')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors du lancement de Discord');
            }
        })
        .catch(error => {
            console.error('Une erreur s\'est produite:', error);
        });
}

function launchWhatsapp() {
    // Exécuter une requête HTTP vers le serveur Flask pour lancer Discord
    fetch('/launch_whatsapp')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors du lancement de Whatsapp');
            }
        })
        .catch(error => {
            console.error('Une erreur s\'est produite:', error);
        });
}

function launchSkype() {
    // Exécuter une requête HTTP vers le serveur Flask pour lancer Discord
    fetch('/launch_skype')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors du lancement de Skype');
            }
        })
        .catch(error => {
            console.error('Une erreur s\'est produite:', error);
        });
}