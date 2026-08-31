document.addEventListener("DOMContentLoaded", () => {

    /* ==========================
       3D Card Tilt Effect
    ========================== */

    const cards = document.querySelectorAll(".product-card");

    cards.forEach(card => {

        card.addEventListener("mousemove", (e) => {

            const rect = card.getBoundingClientRect();

            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const rotateX = -(y - rect.height / 2) / 18;
            const rotateY = (x - rect.width / 2) / 18;

            card.style.transform =
                `perspective(1000px)
                 rotateX(${rotateX}deg)
                 rotateY(${rotateY}deg)
                 translateY(-12px)
                 scale(1.03)`;

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform =
                "perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)";

        });

    });

    /* ==========================
       Fade In Animation
    ========================== */

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0px)";

            }

        });

    }, {
        threshold: 0.2
    });

    cards.forEach(card => {

        card.style.opacity = "0";
        card.style.transform = "translateY(60px)";
        card.style.transition = "0.8s ease";

        observer.observe(card);

    });

    /* ==========================
       Image Float Animation
    ========================== */

    const images = document.querySelectorAll(".image-box img");

    images.forEach(img => {

        img.addEventListener("mouseenter", () => {

            img.style.transform =
                "scale(1.1) rotate(-5deg) translateY(-10px)";

        });

        img.addEventListener("mouseleave", () => {

            img.style.transform =
                "scale(1) rotate(0deg) translateY(0px)";

        });

    });

    /* ==========================
       Add To Cart Animation
    ========================== */

    const cartButtons = document.querySelectorAll(".cart-btn");

    cartButtons.forEach(btn => {

        btn.addEventListener("click", function () {

            this.innerHTML = "✔ Added";

            this.style.background =
                "linear-gradient(90deg,#00ff88,#00d46a)";

            setTimeout(() => {

                this.innerHTML = "Add to Cart";

                this.style.background =
                    "linear-gradient(90deg,#00d9ff,#3bc5ff)";

            }, 1500);

        });

    });

    /* ==========================
       Neon Glow Effect
    ========================== */

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {

            card.style.boxShadow =
                "0 0 30px cyan, 0 0 60px rgba(0,255,255,.3)";

        });

        card.addEventListener("mouseleave", () => {

            card.style.boxShadow =
                "0 10px 30px rgba(0,0,0,.3)";

        });

    });

});