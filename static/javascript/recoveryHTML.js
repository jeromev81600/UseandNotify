document.addEventListener('DOMContentLoaded', function () {
    // Récupération du contenu des e-mails depuis la variable Python
    var emailsContent = {{ emails_content | tojson }};

    // Sélection de la balise HTML où insérer le contenu de l'e-mail
    var emailsContentDiv = document.getElementById('emails-content');

    // Parcours de la liste emailContents et insertion dans la balise HTML
    emailsContent.forEach(function (content) {
        var emailContent = document.createElement('div');
        emailContent.innerHTML = content;
        emailsContentDiv.appendChild(emailContent);
    });
});


        document.addEventListener('DOMContentLoaded', function () {
            // Récupération du contenu des e-mails depuis la variable Python
            var emailContents = {{ email_content | tojson }};

            // Sélection de la balise HTML où insérer le contenu de l'e-mail
            var emailContentDiv = document.getElementById('email-content');

            // Parcours de la liste emailContents et insertion dans la balise HTML
            emailContents.forEach(function (content) {
                var emailContent = document.createElement('div');
                emailContent.innerHTML = content;
                emailContentDiv.appendChild(emailContent);
            });
        });

         document.addEventListener('DOMContentLoaded', function () {
            // Récupération des titres depuis la variable Python
            var emailsTitles = {{ emails_titles | tojson }};

            // Sélection de la balise HTML où insérer le contenu de l'e-mail
            var emailsTitlesDiv = document.getElementById('emails-titles');

            // Parcours de la liste emailContents et insertion dans la balise HTML
            emailsTitles.forEach(function (content) {
                var emailTitle = document.createElement('div');
                emailTitle.innerHTML = content;
                emailsTitlesDiv.appendChild(emailTitle);
            });
        });