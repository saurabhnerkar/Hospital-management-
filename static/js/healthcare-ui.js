document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector("[data-sidebar]");
    const backdrop = document.querySelector("[data-sidebar-backdrop]");
    const toggles = document.querySelectorAll("[data-sidebar-toggle]");

    const setSidebarState = (open) => {
        if (!sidebar || !backdrop) {
            return;
        }

        sidebar.classList.toggle("is-open", open);
        backdrop.classList.toggle("is-open", open);
        document.body.classList.toggle("sidebar-open", open);
    };

    toggles.forEach((toggle) => {
        toggle.addEventListener("click", () => {
            const shouldOpen = !sidebar?.classList.contains("is-open");
            setSidebarState(shouldOpen);
        });
    });

    if (backdrop) {
        backdrop.addEventListener("click", () => setSidebarState(false));
    }

    document.querySelectorAll("[data-counter]").forEach((counter) => {
        const target = Number(counter.getAttribute("data-counter")) || 0;
        const duration = 850;
        const start = performance.now();

        const tick = (now) => {
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            counter.textContent = Math.round(target * eased).toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(tick);
            }
        };

        requestAnimationFrame(tick);
    });
});
