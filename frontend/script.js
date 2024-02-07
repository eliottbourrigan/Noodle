// Récupérez la référence de l'élément input
var searchInput = document.getElementById('searchInput');

// Placez automatiquement le curseur dans la barre de recherche
searchInput.focus();

// Ajoutez un écouteur d'événements pour l'événement keypress
searchInput.addEventListener('keypress', function(event) {
    // Vérifiez si la touche appuyée est la touche Entrée (code 13)
    if (event.key === 'Enter') {
        // Appellez la fonction performSearch lorsque la touche Entrée est enfoncée
        performSearch();
    }
});

document.getElementById('reloadPage').addEventListener('click', function() {
    location.reload(true); // La valeur true force le rechargement depuis le serveur et ignore le cache
  });
  

function performSearch() {
    // Supprime l'élément .titlescreen s'il existe
    const titlescreen = document.querySelector('.titlescreen');
    if (titlescreen) {
        titlescreen.remove();
    }

    // Simulation d'une recherche avec une chaîne exemple (remplacez cela par votre logique de recherche réelle)
    const searchInput = "example string";
    console.log("searchInput: ", searchInput);

    // Remplacez l'URL par l'URL réelle de votre API de recherche
    const apiUrl = `http://127.0.0.1:8000/search?q=${encodeURIComponent(searchInput)}`;

    // Récupère la référence du conteneur des résultats de recherche
    const searchResultsDiv = document.getElementById('searchResults');

    // Effectue la requête API
    fetch(apiUrl)
        .then(response => response.json())
        .then(results => {
            // Efface le contenu précédent
            searchResultsDiv.innerHTML = '';

            // Parcours les résultats et crée des éléments HTML pour chaque résultat
            results.forEach(result => {
                // Crée un élément de liste
                const listItem = document.createElement('li');

                // Crée un conteneur div pour chaque page avec le hover effect, padding, style et centrage horizontal
                const pageContainer = document.createElement('div');
                pageContainer.style.cursor = 'pointer';
                pageContainer.style.transition = 'background-color 0.3s'; // Add smooth transition
                pageContainer.style.padding = '15px'; // Add 5px padding
                pageContainer.style.maxWidth = '500px'; // Set maximum width
                pageContainer.style.borderRadius = '10px'; // Round the corners
                pageContainer.style.margin = 'auto'; // Center horizontally

                // Ajoute un événement de clic pour rediriger vers le lien
                pageContainer.addEventListener('click', function() {
                    window.location.href = result.url;
                });

                pageContainer.addEventListener('mouseover', function() {
                    pageContainer.style.backgroundColor = 'lightgrey';
                });
                
                pageContainer.addEventListener('mouseout', function() {
                    pageContainer.style.backgroundColor = 'initial';
                });

                // Crée un élément de titre (gras, noir) enveloppé dans un div
                const titleDiv = document.createElement('div');
                titleDiv.style.fontFamily = 'Poppins';
                titleDiv.style.fontWeight = 'bold';
                titleDiv.style.color = 'black';
                titleDiv.textContent = result.title;

                // Ajoute un événement de clic pour rediriger vers le lien
                titleDiv.addEventListener('click', function() {
                    window.location.href = result.url;
                });

                // Crée un élément de lien (poppins light, gris, italique)
                const linkElement = document.createElement('div');
                linkElement.style.fontFamily = 'Poppins';
                linkElement.style.fontWeight = '300'; // Poppins Light
                linkElement.style.color = 'grey';
                linkElement.style.fontStyle = 'italic';
                linkElement.textContent = result.url;

                // Crée un élément de contenu (poppins light, noir)
                const contentElement = document.createElement('div');
                contentElement.style.fontFamily = 'Poppins';
                contentElement.style.fontWeight = '300'; // Poppins Light
                contentElement.style.color = 'black';
                contentElement.textContent = result.content;

                // Ajoute les éléments au conteneur de la page
                pageContainer.appendChild(titleDiv);
                pageContainer.appendChild(linkElement);
                pageContainer.appendChild(contentElement);

                // Ajoute le conteneur de la page à la liste
                listItem.appendChild(pageContainer);

                // Ajoute la liste au conteneur des résultats de recherche
                searchResultsDiv.appendChild(listItem);
            });
        })
        .catch(error => console.error('Erreur de recherche :', error));
}

    