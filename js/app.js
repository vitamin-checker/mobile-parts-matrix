const dict = {
    ar: {
        title: "موسوعة توافق القطع",
        subtitle: "ابحث عن الشاشات والبطاريات المتوافقة لهاتفك",
        search_placeholder: "ابحث باسم الهاتف أو رقم القطعة (مثال: Redmi Note 11 أو BN5D)",
        btn_search: "بحث",
        filter_all: "الكل",
        filter_screens: "شاشات",
        filter_batteries: "بطاريات",
        no_results: "لم يتم العثور على نتائج.",
        compatible_with: "يتوافق مع:",
        buy_now: "ابحث للشراء في AliExpress",
        screen_badge: "شاشة",
        battery_badge: "بطارية"
    },
    en: {
        title: "Parts Compatibility Engine",
        subtitle: "Find compatible screens and batteries for your phone",
        search_placeholder: "Search by phone model or part number (e.g. Redmi Note 11)...",
        btn_search: "Search",
        filter_all: "All",
        filter_screens: "Screens",
        filter_batteries: "Batteries",
        no_results: "No results found.",
        compatible_with: "Compatible with:",
        buy_now: "Search on AliExpress",
        screen_badge: "Screen",
        battery_badge: "Battery"
    },
    fr: {
        title: "Moteur de Compatibilité des Pièces",
        subtitle: "Trouvez les écrans et batteries compatibles pour votre téléphone",
        search_placeholder: "Rechercher par modèle ou pièce (ex: Redmi Note 11)...",
        btn_search: "Rechercher",
        filter_all: "Tout",
        filter_screens: "Écrans",
        filter_batteries: "Batteries",
        no_results: "Aucun résultat trouvé.",
        compatible_with: "Compatible avec :",
        buy_now: "Rechercher sur AliExpress",
        screen_badge: "Écran",
        battery_badge: "Batterie"
    }
};

let currentLang = localStorage.getItem('appLang');
let allData = [];
let currentFilter = 'all';

// DOM Elements
const elements = {
    html: document.documentElement,
    popup: document.getElementById('langPopup'),
    title: document.getElementById('mainTitle'),
    subtitle: document.getElementById('mainSubtitle'),
    searchInput: document.getElementById('searchInput'),
    searchBtn: document.getElementById('searchBtn'),
    filterAll: document.getElementById('filterAll'),
    filterScreens: document.getElementById('filterScreens'),
    filterBatteries: document.getElementById('filterBatteries'),
    resultsContainer: document.getElementById('resultsContainer'),
    noResults: document.getElementById('noResults'),
    loading: document.getElementById('loading')
};

// Initialize App
async function init() {
    if (!currentLang) {
        elements.popup.classList.add('active');
    } else {
        applyLanguage(currentLang);
        elements.popup.classList.remove('active');
    }

    setupEventListeners();
    await loadData();
    // Render initially empty or all (limit to 50 to avoid lag)
    renderResults(allData);
}

// Language Management
window.setLanguage = function(lang) {
    currentLang = lang;
    localStorage.setItem('appLang', lang);
    elements.popup.classList.remove('active');
    applyLanguage(lang);
    renderResults(getFilteredData(elements.searchInput.value));
};

window.openLangPopup = function() {
    elements.popup.classList.add('active');
};

function applyLanguage(lang) {
    const t = dict[lang];
    elements.html.lang = lang;
    elements.html.dir = lang === 'ar' ? 'rtl' : 'ltr';

    elements.title.textContent = t.title;
    elements.subtitle.textContent = t.subtitle;
    elements.searchInput.placeholder = t.search_placeholder;
    elements.searchBtn.textContent = t.btn_search;
    elements.filterAll.textContent = t.filter_all;
    elements.filterScreens.textContent = t.filter_screens;
    elements.filterBatteries.textContent = t.filter_batteries;
    elements.noResults.innerHTML = `<p>${t.no_results}</p>`;
}

// Data Loading
async function loadData() {
    elements.loading.classList.remove('hidden');
    try {
        const [batteriesRes, compatibilitiesRes, lcdsRes] = await Promise.all([
            fetch('batteries.json'),
            fetch('compatibilities.json'),
            fetch('lcds.json')
        ]);

        const batteries = await batteriesRes.json();
        const compatibilities = await compatibilitiesRes.json();
        const lcds = await lcdsRes.json();

        // Normalize data
        const formatData = (items, type) => items.map(item => ({
            type: type,
            ref: item.battery_ref || item.screen_ref || item.lcd_ref,
            brand: item.brand_ref,
            models: item.compatible_models ? item.compatible_models.map(m => `${m.brand} ${m.model}`) : []
        }));

        allData = [
            ...formatData(batteries, 'battery'),
            ...formatData(compatibilities, 'screen'),
            ...formatData(lcds, 'screen')
        ];
    } catch (error) {
        console.error("Error loading data:", error);
    } finally {
        elements.loading.classList.add('hidden');
    }
}

// Event Listeners
function setupEventListeners() {
    elements.searchInput.addEventListener('input', (e) => {
        handleSearch(e.target.value);
    });

    elements.searchBtn.addEventListener('click', () => {
        handleSearch(elements.searchInput.value);
    });

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            handleSearch(elements.searchInput.value);
        });
    });
}

// Search and Filter
function handleSearch(query) {
    const results = getFilteredData(query);
    renderResults(results);
}

function getFilteredData(query) {
    const q = query.toLowerCase().trim();
    return allData.filter(item => {
        // Filter by type
        if (currentFilter !== 'all' && item.type !== currentFilter) return false;

        // Filter by query
        if (!q) return true;
        
        const matchRef = item.ref.toLowerCase().includes(q);
        const matchModels = item.models.some(model => model.toLowerCase().includes(q));
        return matchRef || matchModels;
    });
}

// Render Results
function renderResults(data) {
    elements.resultsContainer.innerHTML = '';
    
    if (data.length === 0) {
        elements.noResults.classList.remove('hidden');
        return;
    }
    
    elements.noResults.classList.add('hidden');
    const t = dict[currentLang || 'ar'];
    
    // Limit to 50 results to prevent browser lag for empty searches
    const displayData = data.slice(0, 50);

    const html = displayData.map(item => {
        const badgeClass = item.type === 'screen' ? 'badge-screen' : 'badge-battery';
        const badgeText = item.type === 'screen' ? t.screen_badge : t.battery_badge;
        
        // Search link (example: Aliexpress search URL)
        const searchUrl = `https://www.aliexpress.com/wholesale?SearchText=${encodeURIComponent(item.ref)}`;

        return `
            <div class="result-card glass-card">
                <div class="card-header">
                    <span class="part-ref">${item.ref}</span>
                    <span class="badge ${badgeClass}">${badgeText}</span>
                </div>
                <div>
                    <p class="text-muted" style="margin-bottom: 0.5rem; font-size: 0.9rem;">${t.compatible_with}</p>
                    <div class="models-list">
                        ${item.models.map(model => `<span class="model-tag">${model}</span>`).join('')}
                    </div>
                </div>
                <a href="${searchUrl}" target="_blank" class="btn-buy">${t.buy_now}</a>
            </div>
        `;
    }).join('');

    elements.resultsContainer.innerHTML = html;
}

// Run app
init();
