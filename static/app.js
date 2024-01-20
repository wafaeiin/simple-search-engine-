function search() {
    // Get the search query from the input field
    const query = document.getElementById('searchInput').value;

    // Make a GET request to the /search endpoint with the query parameter
    fetch(`/search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(results => displayResults(results))
        .catch(error => console.error('Error:', error));
}

function displayResults(results) {
    // Get the results container element
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = ''; // Clear previous results

    // Iterate through the results and create HTML elements for each result
    results.forEach(result => {
        const resultElement = document.createElement('div');
        resultElement.classList.add('result');

        // Create a clickable link for the title
        const titleLink = document.createElement('a');
        titleLink.href = result.link; // Assuming 'link' contains the URL to the document
        titleLink.textContent = result.title;
        titleLink.target = '_blank'; // Open link in a new tab

        // Append the title link to the result element
        resultElement.appendChild(titleLink);

        // Create a div for authors and publication date, both in green
        const authorsDateElement = document.createElement('div');
        authorsDateElement.innerHTML = `
            <span class="green">${result.authors.join(', ')}</span> -
            <span class="green">${result.publication_date}</span>`;
        resultElement.appendChild(authorsDateElement);

        // Create a p element for the abstract
        const abstractElement = document.createElement('p');
        abstractElement.textContent = result.abstract;
        resultElement.appendChild(abstractElement);

        // Add the result element to the results container
        resultsContainer.appendChild(resultElement);
    });
}
