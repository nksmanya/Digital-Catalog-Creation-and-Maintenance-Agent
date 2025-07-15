function getCatalogKey() {
  const user = JSON.parse(localStorage.getItem("loggedInUser"));
  return "catalog_" + user.phone;
}

function saveProduct() {
  const name = document.getElementById("name").value;
  const description = document.getElementById("description").value;
  const price = +document.getElementById("price").value;
  const stock = +document.getElementById("stock").value;
  const category = document.getElementById("category").value;

  const product = { name, description, price, stock, category, time: new Date().toISOString() };

  const catalogKey = getCatalogKey();
  const existing = JSON.parse(localStorage.getItem(catalogKey)) || [];
  existing.push(product);
  localStorage.setItem(catalogKey, JSON.stringify(existing));

  alert("Product saved!");
  window.location.href = "dashboard.html";
}

function loadCatalog() {
  const catalogKey = getCatalogKey();
  const catalog = JSON.parse(localStorage.getItem(catalogKey)) || [];

  let html = "";
  catalog.forEach((p, index) => {
    html += `
      <div class="product">
        <h3>${p.name}</h3>
        <p>${p.description}</p>
        <p>₹${p.price} | Stock: ${p.stock}</p>
        <p>Category: ${p.category}</p>
      </div>
    `;
  });

  document.getElementById("productList").innerHTML = html;
}

// Auto-load when on dashboard
if (window.location.pathname.includes("dashboard.html")) {
  loadCatalog();
}
