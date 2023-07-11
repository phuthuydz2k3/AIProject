// Selecting the sidebar and buttons
const sidebar = document.querySelector(".sidebar");
const sidebarOpenBtn = document.querySelector("#sidebar-open");
const sidebarCloseBtn = document.querySelector("#sidebar-close");
const sidebarLockBtn = document.querySelector("#lock-icon");

// Function to toggle the lock state of the sidebar
const toggleLock = () => {
  sidebar.classList.toggle("hoverable");
  // If the sidebar is not hoverable
  if (!sidebar.classList.contains("hoverable")) {
    sidebar.classList.add("locked");
    sidebarLockBtn.classList.replace("bx-lock-open-alt", "bx-lock-alt");
  } else {
    sidebar.classList.remove("locked");
    sidebarLockBtn.classList.replace("bx-lock-alt", "bx-lock-open-alt");
  }
};

// Function to hide the sidebar when the mouse leaves
const hideSidebar = () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.add("close");
  }
};

// Function to show the sidebar when the mouse enter
const showSidebar = () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.remove("close");
  }
};

// Function to show and hide the sidebar
const toggleSidebar = () => {
  sidebar.classList.toggle("close");
};

// If the window width is less than 800px, close the sidebar and remove hoverability and lock
if (window.innerWidth < 800) {
  sidebar.classList.add("close");
  sidebar.classList.remove("locked");
  sidebar.classList.remove("hoverable");
}

// Adding event listeners to buttons and sidebar for the corresponding actions
sidebarLockBtn.addEventListener("click", toggleLock);
sidebar.addEventListener("mouseleave", hideSidebar);
sidebar.addEventListener("mouseenter", showSidebar);
// sidebarOpenBtn.addEventListener("click", toggleSidebar);
sidebarCloseBtn.addEventListener("click", toggleSidebar);

const menuItem = document.getElementsByClassName("menu_item")[0];
console.log(menuItem)
const li = menuItem.querySelectorAll("li");
const li1 = li[0];
const li2 = li[1];

li1.addEventListener("click", () => {
    const article = document.getElementById("article");
    allCompany.style.display = "none";
    article.style.display = "flex";
})

li2.addEventListener("click", () => {
    const allCompany = document.getElementById("allCompany");
    article.style.display = "none";
    allCompany.style.display = "flex";
})

