window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', 'G-EWKHJ174CD');

const locationFilter = document.getElementById('locationFilter');
const availabilityFilter = document.getElementById('availabilityFilter');
const priceFilter = document.getElementById('priceFilter');
const saatavuusFilter = document.getElementById('saatavuusFilter');
const cottageCards = [...document.querySelectorAll('.cottage-card')];
const noResults = document.getElementById('noResults');
const resultCount = document.getElementById('resultCount');
const menuButton = document.querySelector('.menu-btn');
const menu = document.getElementById('menuDropdown');

const populateFilter = (select, values, label) => {
    select.innerHTML = `<option value="all">${label}</option>`;
    values.forEach((value) => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
    });
};

function updateFilters() {
    const location = locationFilter.value;
    const weeks = cottageCards
        .filter((card) => location === 'all' || card.dataset.location === location)
        .map((card) => Number(card.dataset.week));
    populateFilter(availabilityFilter, [...new Set(weeks)].sort((a, b) => a - b), 'Kaikki viikot');
    filterCards();
}

function filterCards() {
    const location = locationFilter.value;
    const week = availabilityFilter.value;
    const status = saatavuusFilter.value;
    const type = priceFilter.value;
    let visibleCount = 0;

    cottageCards.forEach((card) => {
        const visible = (location === 'all' || card.dataset.location === location)
            && (week === 'all' || card.dataset.week === week)
            && (status === 'all' || card.dataset.status === status)
            && (type === 'all' || (type === 'vuokra' && card.dataset.rent) || (type === 'myynti' && card.dataset.sale));
        card.hidden = !visible;
        if (visible) visibleCount += 1;
    });

    noResults.hidden = visibleCount !== 0;
    resultCount.textContent = `${visibleCount} ilmoitusta`;
}

populateFilter(locationFilter, [...new Set(cottageCards.map((card) => card.dataset.location))], 'Kaikki kohteet');
updateFilters();

locationFilter.addEventListener('change', updateFilters);
availabilityFilter.addEventListener('change', filterCards);
saatavuusFilter.addEventListener('change', filterCards);
priceFilter.addEventListener('change', filterCards);

menuButton.addEventListener('click', () => {
    const isOpen = menu.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
});

menu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
        menu.classList.remove('is-open');
        menuButton.setAttribute('aria-expanded', 'false');
    });
});