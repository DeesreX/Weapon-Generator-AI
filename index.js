const API_URL = 'http://127.0.0.1:5000/generate-weapon';

async function generateAssetData() {
    const response = await fetch(API_URL);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

function createAssetCard(asset) {
    return `
        <div class="asset-card glow">
            <h2>${asset.name || "Mysterious Asset"}</h2>
            ${asset.image_url ? `<img src="${asset.image_url}" alt="Asset Image" class="asset-image">` : ''}
            <div class="asset-details">
                <p><strong>Type:</strong> ${asset.type || "Unknown"}</p>
                <p><strong>Element:</strong> ${asset.element || "None"}</p>
                <p><strong>Rarity:</strong> ${asset.rarity || "Unknown"}</p>
            </div>
            <div class="asset-stats">
                <p class="section-title">Asset Stats:</p>
                <ul>
                    ${Object.entries(asset.stats || {}).length > 0 
                        ? Object.entries(asset.stats).map(([key, value]) => 
                            `<li><span>${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</span> <span>${value}</span></li>`
                        ).join('') 
                        : "<li>No stats available</li>"
                    }
                </ul>
            </div>
        </div>
    `;
}

async function generateAssetCard() {
    const loadingElement = document.getElementById('loading');
    const containerElement = document.getElementById('asset-container');

    loadingElement.style.display = 'block';
    containerElement.innerHTML = '';

    try {
        const asset = await generateAssetData();
        console.log("Received asset data:", asset); // For debugging
        containerElement.innerHTML = createAssetCard(asset);
        saveAsset(asset);
    } catch (error) {
        containerElement.innerHTML = `<p class="error">Error generating asset: ${error.message}</p>`;
    } finally {
        loadingElement.style.display = 'none';
    }
}

function saveAsset(asset) {
    let assets = JSON.parse(localStorage.getItem('gameAssets')) || [];
    asset.id = Date.now(); // Add a unique id to the asset
    assets.push(asset);
    localStorage.setItem('gameAssets', JSON.stringify(assets));
}

document.getElementById('generateButton').addEventListener('click', generateAssetCard);