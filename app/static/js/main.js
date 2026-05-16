const root = document.documentElement;
const savedTheme = localStorage.getItem("theme") || "light";
root.setAttribute("data-theme", savedTheme);

// Dark / Light Mode
const themeToggle = document.getElementById("themeToggle");

if (themeToggle) {
    const icon = themeToggle.querySelector("i");

    const syncThemeButton = () => {
        const isDark = root.getAttribute("data-theme") === "dark";

        if (icon) {
            icon.className = isDark ? "bi bi-sun" : "bi bi-moon-stars";
        }
    };

    syncThemeButton();

    themeToggle.addEventListener("click", () => {
        const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        localStorage.setItem("theme", next);
        syncThemeButton();
    });
}

// Hero Carousel Enhancement
document.addEventListener("DOMContentLoaded", function () {
    const heroCarousel = document.getElementById("heroCarousel");
    
    if (heroCarousel) {
        // Initialize Bootstrap carousel with custom timing
        const carousel = new bootstrap.Carousel(heroCarousel, {
            interval: 6000,
            ride: "carousel",
            wrap: true
        });

        // Trigger animation classes on slide change
        heroCarousel.addEventListener("slide.bs.carousel", function (event) {
            const nextSlide = event.relatedTarget;
            const animatedElements = nextSlide.querySelectorAll("[class*='animate-']");
            
            animatedElements.forEach((el) => {
                // Reset animation
                el.style.animation = "none";
                setTimeout(() => {
                    el.style.animation = "";
                }, 10);
            });
        });

        // Pause on hover
        heroCarousel.addEventListener("mouseenter", function () {
            carousel.pause();
        });

        // Resume on mouse leave
        heroCarousel.addEventListener("mouseleave", function () {
            carousel.cycle();
        });
    }
});

// Sidebar toggle removed - using top navbar instead

// Auto close flash alerts
setTimeout(() => {
    document.querySelectorAll(".alert").forEach((alert) => {
        const instance = bootstrap.Alert.getOrCreateInstance(alert);
        instance.close();
    });
}, 4500);

// Quick table search
const quickSearch = document.getElementById("quickTableSearch");

if (quickSearch) {
    quickSearch.addEventListener("keyup", () => {
        const value = quickSearch.value.toLowerCase();

        document.querySelectorAll("[data-task-row]").forEach((row) => {
            row.style.display = row.textContent.toLowerCase().includes(value) ? "" : "none";
        });
    });
}