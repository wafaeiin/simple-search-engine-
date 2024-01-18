function search() {
    const query = document.getElementById('searchInput').value;

    fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById('results');
            resultsContainer.innerHTML = '';

            data.forEach(result => {
                const resultElement = document.createElement('div');
                resultElement.innerHTML = `
                    <h3>${result.title}</h3>
                    <p>${result.authors.join(', ')}</p>
                    <p>${result.publication_date}</p>
                    <p>${result.abstract}</p>
                    <p>Keywords: ${result.keywords.join(', ')}</p>
                `;
                resultsContainer.appendChild(resultElement);
            });
        })
        .catch(error => console.error('Error:', error));
}
