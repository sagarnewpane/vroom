const searchInput = document.querySelector('.navbar .search input[type="text"]');
const searchResults = document.querySelector('.navbar .search-results');

function search(query) {
    const items = ["Scorpio", "Hundyai", "Polo"];
    const filteredItems = items.filter(item => item.toLowerCase().includes(query.toLowerCase()));
    displayResults(filteredItems);
}

// Frontend displayResults function
function displayResults(results) {
    searchResults.innerHTML = '';
    if (results.length === 0) {
        const li = document.createElement('li');
        li.textContent = "Not found";
        searchResults.appendChild(li);
    } else {
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

// Backend search function
function backendSearch(query, callback) {

    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/search?q=${query}`);
    xhr.onload = function() {
        if (xhr.status === 200) {
            const results = JSON.parse(xhr.responseText);
            callback(results);
        } else {
            console.error('Request failed');
        }
    };
    xhr.send();
}
