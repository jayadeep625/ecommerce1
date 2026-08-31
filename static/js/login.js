document.addEventListener("DOMContentLoaded", function () {

    // ============================
    // Show / Hide Password
    // ============================

    const password = document.getElementById("password");
    const toggle = document.getElementById("togglePassword");

    if (password && toggle) {

        toggle.addEventListener("click", function () {

            if (password.type === "password") {

                password.type = "text";
                toggle.innerHTML = "🙈";

            } else {

                password.type = "password";
                toggle.innerHTML = "👁";

            }

        });

    }

    // ============================
    // 3D Card Effect
    // ============================

    const card = document.querySelector(".login-card");

    if (card) {

        card.addEventListener("mousemove", function (e) {

            const rect = card.getBoundingClientRect();

            const x = e.clientX - rect.left;

            const y = e.clientY - rect.top;

            const rotateX = -(y - rect.height / 2) / 18;

            const rotateY = (x - rect.width / 2) / 18;

            card.style.transform =
                `rotateX(${rotateX}deg)
                 rotateY(${rotateY}deg)
                 translateY(-8px)`;

        });

        card.addEventListener("mouseleave", function () {

            card.style.transform =
                "rotateX(0deg) rotateY(0deg)";

        });

    }

    // ============================
    // Input Animation
    // ============================

    const inputs = document.querySelectorAll("input");

    inputs.forEach(function (input) {

        input.addEventListener("focus", function () {

            input.parentElement.style.transform =
                "scale(1.03)";

        });

        input.addEventListener("blur", function () {

            input.parentElement.style.transform =
                "scale(1)";

        });

    });

    // ============================
    // Button Loading
    // ============================

    const form = document.querySelector(".login-form");

    if (form) {

        form.addEventListener("submit", function () {

            const btn = document.querySelector(".login-btn");

            btn.innerHTML = "Logging In...";

            btn.disabled = true;

        });

    }

    // ============================
    // Floating Background
    // ============================

    const circles = document.querySelectorAll(".floating-circle");

    document.addEventListener("mousemove", function (e) {

        circles.forEach(function (circle, index) {

            const speed = (index + 1) * 12;

            const x = (window.innerWidth / 2 - e.pageX) / speed;

            const y = (window.innerHeight / 2 - e.pageY) / speed;

            circle.style.transform =
                `translate(${x}px, ${y}px)`;

        });

    });

    // ============================
    // Fade In Animation
    // ============================

    if (card) {

        card.style.opacity = "0";

        card.style.transform = "translateY(40px)";

        setTimeout(function () {

            card.style.transition = "0.8s";

            card.style.opacity = "1";

            card.style.transform = "translateY(0px)";

        }, 300);

    }

});