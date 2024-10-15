function getAllAssets() {
    return JSON.parse(localStorage.getItem('gameAssets')) || [];
}

function getAsset(id) {
    const assets = getAllAssets();
    return assets.find(asset => asset.id === id);
}

function deleteAsset(id) {
    let assets = getAllAssets();
    assets = assets.filter(asset => asset.id !== id);
    localStorage.setItem('gameAssets', JSON.stringify(assets));
    renderAssetList();
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
            <button onclick="deleteAsset(${asset.id}); renderAssetList();">Delete Asset</button>
        </div>
    `;
}

function renderAssetList() {
    const assets = getAllAssets();
    const listElement = document.getElementById('asset-list');
    listElement.innerHTML = `
        <h2>Saved Assets</h2>
        <ul class="asset-list">
            ${assets.map(asset => `
                <li>
                    <a href="#" onclick="displayAsset(${asset.id}); return false;">
                        ${asset.name || "Unnamed Asset"}
                    </a>
                </li>
            `).join('')}
        </ul>
    `;
}

function displayAsset(id) {
    const asset = getAsset(id);
    const displayElement = document.getElementById('asset-display');
    displayElement.innerHTML = createAssetCard(asset);
}

document.addEventListener('DOMContentLoaded', renderAssetList);