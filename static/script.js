window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-EWKHJ174CD');

const locationFilter = document.getElementById('locationFilter');
const availabilityFilter = document.getElementById('availabilityFilter');
const priceFilter = document.getElementById('priceFilter');
const saatavuusFilter = document.getElementById('saatavuusFilter');
const tableRows = document.querySelectorAll('#myTable tbody tr');
const cottageList = document.getElementById('cottageList');

const availableWeeks = {
    levi: [8, 13, 14, 15],
    katinkulta: [8, 11, 27, 28, 29, 30, 31]
};

function filterTable() {
    const locationValue = locationFilter.value;
    const availabilityValue = availabilityFilter.value;
    const saatavuusValue = saatavuusFilter.value;
    const priceValue = priceFilter.value;

    let anyRowsVisible = false; 
    let noResultsRow = document.getElementById('noResultsRow'); 

    tableRows.forEach(row => {
        const locationCell = row.querySelector('td:nth-child(1)');
        const availabilityCell = row.querySelector('td:nth-child(3)');
        const vuokrahintaCell = row.querySelector('td:nth-child(6)');
        const myyntihintaCell = row.querySelector('td:nth-child(7)');
        const availCell = row.querySelector('td:nth-child(9)');

        const locationMatch = locationValue === 'all' || locationCell.textContent.toLowerCase() === locationValue;
        const availabilityMatch = availabilityValue === 'all' || availabilityCell.textContent === availabilityValue;
        const availMatch = saatavuusValue === 'all' || availCell.textContent.toLowerCase() === saatavuusValue;

        let priceMatch = true;
        if (priceValue === 'vuokra') {
            priceMatch = vuokrahintaCell.textContent.trim() !== '';
        } else if (priceValue === 'myynti') {
            priceMatch = myyntihintaCell.textContent.trim() !== '';
        }

        if (locationMatch && availabilityMatch && availMatch && priceMatch) {
            row.style.display = 'table-row';
            anyRowsVisible = true; 
        } else {
            row.style.display = 'none';
        }
    });

    
    if (!anyRowsVisible && !noResultsRow) {
        noResultsRow = document.createElement('tr');
        const noResultsCell = document.createElement('td');
        noResultsCell.colSpan = "10";
        noResultsCell.textContent = "Ei lomaviikkoja";
        noResultsRow.appendChild(noResultsCell);
        noResultsRow.id = 'noResultsRow'; 
        cottageList.appendChild(noResultsRow);
    } else if (anyRowsVisible && noResultsRow) {
    
        noResultsRow.remove();
    }

}


locationFilter.addEventListener('change', function () {
    const selectedLocation = this.value;
    const weeks = availableWeeks[selectedLocation] || [];

    
    availabilityFilter.innerHTML = '<option value="all">Kaikki</option>';

    
    if (selectedLocation === 'all') {
        
        Object.values(availableWeeks).flat().forEach(week => {
            const option = document.createElement('option');
            option.value = week;
            option.textContent = week;
            availabilityFilter.appendChild(option);
        });
    } else {
        weeks.forEach(week => {
            const option = document.createElement('option');
            option.value = week;
            option.textContent = week;
            availabilityFilter.appendChild(option);
        });
    }

    
    filterTable();
});

availabilityFilter.addEventListener('change', filterTable);
saatavuusFilter.addEventListener('change', filterTable);
priceFilter.addEventListener('change', filterTable);

function toggleMenu() {
    var menu = document.getElementById("menuDropdown");
    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }
}

function openNewPage(url) {
    window.location.href = url;
}