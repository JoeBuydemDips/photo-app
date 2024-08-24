document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const resultsGrid = document.getElementById('results-grid');
    const themeToggle = document.getElementById('theme-toggle');
    const paginationContainer = document.getElementById('pagination');
    let currentPage = 1;
    const photosPerPage = 30;
    let totalPhotos = 0;
    let currentQuery = '';

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        currentQuery = searchInput.value.trim();
        if (currentQuery) {
            currentPage = 1;
            await fetchAndDisplayPhotos(currentQuery, currentPage);
        }
    });

    async function fetchAndDisplayPhotos(query, page) {
        try {
            resultsGrid.innerHTML = '<p>Loading...</p>'; // Show loading indicator

            const response = await fetch(`/search?query=${encodeURIComponent(query)}&page=${page}`);
            const data = await response.json();
            
            totalPhotos = data.total;
            currentPage = data.page;

            console.log(`Fetched ${data.results.length} photos out of ${totalPhotos} total for page ${currentPage}`);
            displayResults(data.results);
            displayPagination();
        } catch (error) {
            console.error('Error fetching search results:', error);
            resultsGrid.innerHTML = '<p>Error fetching results. Please try again.</p>';
        }
    }

    function displayResults(photos) {
        resultsGrid.innerHTML = '';
        photos.forEach(photo => {
            const photoCard = document.createElement('div');
            photoCard.className = 'photo-card';
            photoCard.innerHTML = `
                <img src="${photo.urls.small}" alt="${photo.alt_description || 'Unsplash photo'}">
                <div class="photo-info">
                    <p>By: ${photo.user.name}</p>
                </div>
            `;
            photoCard.addEventListener('click', () => showExpandedPreview(photo));
            resultsGrid.appendChild(photoCard);
        });
    }

    function displayPagination() {
        const totalPages = Math.ceil(totalPhotos / photosPerPage);
        console.log(`Total pages: ${totalPages}`);
        paginationContainer.innerHTML = '';

        const prevButton = document.createElement('button');
        prevButton.textContent = 'Previous';
        prevButton.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                fetchAndDisplayPhotos(currentQuery, currentPage);
            }
        });
        paginationContainer.appendChild(prevButton);

        const pageInfo = document.createElement('span');
        pageInfo.id = 'page-info';
        paginationContainer.appendChild(pageInfo);

        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.addEventListener('click', () => {
            if (currentPage < totalPages) {
                currentPage++;
                fetchAndDisplayPhotos(currentQuery, currentPage);
            }
        });
        paginationContainer.appendChild(nextButton);

        updatePaginationButtons();
    }

    function updatePaginationButtons() {
        const totalPages = Math.ceil(totalPhotos / photosPerPage);
        const prevButton = paginationContainer.querySelector('button:first-child');
        const nextButton = paginationContainer.querySelector('button:last-child');
        const pageInfo = document.getElementById('page-info');

        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;

        console.log(`Updated pagination: Page ${currentPage} of ${totalPages}`);
        console.log(`Prev button disabled: ${prevButton.disabled}`);
        console.log(`Next button disabled: ${nextButton.disabled}`);

        // Hide pagination if there are no results
        paginationContainer.style.display = totalPages > 0 ? 'flex' : 'none';
    }

    function showExpandedPreview(photo) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <img src="${photo.urls.regular}" alt="${photo.alt_description || 'Unsplash photo'}">
                <div class="photo-info">
                    <p>By: ${photo.user.name}</p>
                    <p>${photo.description || ''}</p>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        setTimeout(() => modal.classList.add('show'), 10);

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('show');
                setTimeout(() => modal.remove(), 300);
            }
        });
    }

    themeToggle.addEventListener('click', () => {
        const darkModeStyle = document.querySelector('link[href$="dark-mode.css"]');
        const lightModeStyle = document.querySelector('link[href$="light-mode.css"]');
        
        if (darkModeStyle.disabled) {
            darkModeStyle.disabled = false;
            lightModeStyle.disabled = true;
        } else {
            darkModeStyle.disabled = true;
            lightModeStyle.disabled = false;
        }
    });
});