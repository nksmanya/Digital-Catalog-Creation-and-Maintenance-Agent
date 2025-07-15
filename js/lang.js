const translations = {
  en: {
    dashboardTitle: "📦 Catalog Dashboard",
    addProduct: "➕ Add Product",
    export: "📤 Export",
    searchPlaceholder: "🔍 Search by name, category, or keyword...",
    lowStock: "📢 Low Stock Alerts",
    recentActivity: "🕓 Recent Activity",
    allGood: "All stock levels are good.",
    logout: "Logout",
    save: "✅ Save",
    cancel: "❌ Cancel",
    edit: "✏️ Edit",
    delete: "🗑️ Delete",
    modalAdd: "Add Product",
    modalEdit: "Edit Product"
  },
  hi: {
    dashboardTitle: "📦 उत्पाद सूची डैशबोर्ड",
    addProduct: "➕ नया उत्पाद",
    export: "📤 निर्यात करें",
    searchPlaceholder: "🔍 नाम, श्रेणी या कीवर्ड से खोजें...",
    lowStock: "📢 कम स्टॉक अलर्ट",
    recentActivity: "🕓 हाल की गतिविधि",
    allGood: "सभी स्टॉक स्तर सही हैं।",
    logout: "लॉगआउट",
    save: "✅ सहेजें",
    cancel: "❌ रद्द करें",
    edit: "✏️ संपादित करें",
    delete: "🗑️ हटाएं",
    modalAdd: "नया उत्पाद जोड़ें",
    modalEdit: "उत्पाद संपादित करें"
  }
};

function changeLanguage(lang) {
  localStorage.setItem("lang", lang);
  applyLanguage();
}

function applyLanguage() {
  const lang = localStorage.getItem("lang") || "en";
  const t = translations[lang];

  // Set dropdown
  const select = document.getElementById("langSelect");
  if (select) select.value = lang;

  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (t[key]) el.innerText = t[key];
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (t[key]) el.setAttribute("placeholder", t[key]);
  });
}
