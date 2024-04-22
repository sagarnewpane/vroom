const searchInput = document.querySelector('.navbar .search input[type="text"]');

const searchResults = document.querySelector('.navbar .search-results');

function search(query) {
    
    const items = ["Scorpio", "Hundyai", "Polo"];
    
    // Filter the items based on the query
    const filteredItems = items.filter(item => item.toLowerCase().includes(query.toLowerCase()));
    
    // Display the filtered items
    displayResults(filteredItems);
}


function displayResults(results) {
    searchResults.innerHTML = '';

    if (results.length === 0) {
        // If the results is not found, display "Not found" message
        const li = document.createElement('li');
        li.textContent = "Not found";
        searchResults.appendChild(li);
    } else {
        // Display new results
        results.forEach(result => {
            const li = document.createElement('li');
            li.textContent = result;
            searchResults.appendChild(li);
        });
    }
}

searchInput.addEventListener('input', function() {
    search(this.value);
});