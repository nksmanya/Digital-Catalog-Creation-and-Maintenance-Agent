function registerUser() {
  const name = document.getElementById("name").value.trim();
  const phone = document.getElementById("phone").value.trim();

  if (!name || !phone) {
    alert("Please enter name and phone.");
    return;
  }

  const user = { name, phone };
  localStorage.setItem("user_" + phone, JSON.stringify(user));
  alert("Registration successful!");
  window.location.href = "index.html";
}

function loginUser() {
  const phone = document.getElementById("phone").value.trim();
  const user = JSON.parse(localStorage.getItem("user_" + phone));

  if (!user) {
    alert("User not found. Please register.");
    return;
  }

  localStorage.setItem("loggedInUser", JSON.stringify(user));
  window.location.href = "dashboard.html";
}
