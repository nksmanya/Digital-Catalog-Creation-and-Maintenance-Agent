function getCatalogKey() {
  const user = JSON.parse(localStorage.getItem("loggedInUser"));
  document.getElementById("userName").innerText = user.name;
  return "catalog_" + user.phone;
}

function logout() {
  localStorage.removeItem("loggedInUser");
  window.location.href = "index.html";
}

function loadDashboard() {
  applyLanguage();
  loadProducts();
  renderSummary();
}

function loadProducts(filter = "") {
  const catalogKey = getCatalogKey();
  const catalog = JSON.parse(localStorage.getItem(catalogKey)) || [];

  const list = document.getElementById("productList");
  list.innerHTML = "";

  const lang = localStorage.getItem("lang") || "en";
  const t = translations[lang];

  catalog.forEach((p, i) => {
    if (
      filter &&
      ![p.name, p.category, p.description].some(val =>
        val.toLowerCase().includes(filter.toLowerCase())
      )
    ) return;

    const card = document.createElement("div");
    card.className = "product-card" + (p.stock < 5 ? " low-stock" : "");
    card.innerHTML = `
      <h3>${p.name}</h3>
      <p>${p.description}</p>
      <p>₹${p.price} | Stock: ${p.stock}</p>
      <p>Category: ${p.category}</p>
      <div class="card-actions">
        <button onclick="editProduct(${i})">${t.edit}</button>
        <button onclick="deleteProduct(${i})">${t.delete}</button>
      </div>
    `;
    list.appendChild(card);
  });
}

function openAddForm() {
  const lang = localStorage.getItem("lang") || "en";
  const t = translations[lang];

  document.getElementById("modalContainer").classList.remove("hidden");
  document.getElementById("productForm").reset();
  document.getElementById("modalTitle").innerText = t.modalAdd;
  document.getElementById("editIndex").value = "";
}

function closeModal() {
  document.getElementById("modalContainer").classList.add("hidden");
}

function saveProduct(event) {
  event.preventDefault();
  const catalogKey = getCatalogKey();
  const catalog = JSON.parse(localStorage.getItem(catalogKey)) || [];

  const newProduct = {
    name: document.getElementById("name").value,
    description: document.getElementById("description").value,
    price: +document.getElementById("price").value,
    stock: +document.getElementById("stock").value,
    category: document.getElementById("category").value,
    time: new Date().toISOString()
  };

  const editIndex = document.getElementById("editIndex").value;
  if (editIndex === "") {
    catalog.push(newProduct);
  } else {
    catalog[editIndex] = newProduct;
  }

  localStorage.setItem(catalogKey, JSON.stringify(catalog));
  closeModal();
  loadProducts();
  renderSummary();
}

function editProduct(index) {
  const catalogKey = getCatalogKey();
  const catalog = JSON.parse(localStorage.getItem(catalogKey)) || [];
  const p = catalog[index];

  const lang = localStorage.getItem("lang") || "en";
  const t = translations[lang];

  document.getElementById("modalContainer").classList.remove("hidden");
  document.getElementById("modalTitle").innerText = t.modalEdit;
  document.getElementById("name").value = p.name;
  document.getElementById("description").value = p.description;
  document.getElementById("price").value = p.price;
  document.getElementById("stock").value = p.stock;
  document.getElementById("category").value = p.category;
  document.getElementById("editIndex").value = index;
}

function deleteProduct(index) {
  const catalogKey = getCatalogKey();
  const catalog = JSON.parse(localStorage.getItem(catalogKey)) || [];
  if (confirm("Are you sure you want to delete this product?")) {
    catalog.splice(index, 1);
    localStorage.setItem(catalogKey, JSON.stringify(catalog));
    loadProducts();
    renderSummary();
  }
}

function searchCatalog() {
  const query = document.getElementById("searchBar").value;
  loadProducts(query);
}

function renderSummary() {
  const catalogKey = getCatalogKey();
  const catalog = JSON.parse(localStorage.getItem(catalogKey)) || [];

  const lang = localStorage.getItem("lang") || "en";
  const t = translations[lang];

  const lowStock = catalog.filter(p => p.stock < 5);
  const recent = catalog.slice(-3).reverse();

  let html = `<h3>${t.lowStock} (${lowStock.length})</h3>`;
  html += lowStock.length === 0
    ? `<p>${t.allGood}</p>`
    : "<ul>" + lowStock.map(p => `<li>${p.name} (${p.stock})</li>`).join("") + "</ul>";

  html += `<h3>${t.recentActivity}</h3>`;
  html += "<ul>" + recent.map(p => `<li>${p.name} - ${new Date(p.time).toLocaleString()}</li>`).join("") + "</ul>";

  document.getElementById("summary").innerHTML = html;
}

function exportCatalog() {
  const catalogKey = getCatalogKey();
  const catalog = JSON.parse(localStorage.getItem(catalogKey)) || [];
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(catalog, null, 2));
  const link = document.createElement("a");
  link.href = dataStr;
  link.download = "catalog.json";
  link.click();
}

// Initialize
document.addEventListener('DOMContentLoaded', loadDashboard);
