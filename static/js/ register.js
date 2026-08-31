document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // Password Show / Hide
    // ==========================

    const password1 = document.getElementById("id_password1");
    const password2 = document.getElementById("id_password2");

    if (password1) {

        const eye1 = document.createElement("span");
        eye1.innerHTML = "👁";
        eye1.className = "toggle-eye";

        password1.parentNode.style.position = "relative";
        password1.parentNode.appendChild(eye1);

        eye1.onclick = function () {

            if (password1.type === "password") {
                password1.type = "text";
                eye1.innerHTML = "🙈";
            }
            else {
                password1.type = "password";
                eye1.innerHTML = "👁";
            }

        }

    }

    if (password2) {

        const eye2 = document.createElement("span");
        eye2.innerHTML = "👁";
        eye2.className = "toggle-eye";

        password2.parentNode.style.position = "relative";
        password2.parentNode.appendChild(eye2);

        eye2.onclick = function () {

            if (password2.type === "password") {
                password2.type = "text";
                eye2.innerHTML = "🙈";
            }
            else {
                password2.type = "password";
                eye2.innerHTML = "👁";
            }

        }

    }

    // ==========================
    // Password Strength
    // ==========================

    if (password1) {

        const meter = document.createElement("div");
        meter.className = "strength-meter";

        const bar = document.createElement("div");
        bar.className = "strength-bar";

        meter.appendChild(bar);

        password1.parentNode.appendChild(meter);

        password1.addEventListener("keyup", function () {

            let value = password1.value;

            let score = 0;

            if (value.length >= 8) score++;
            if (/[A-Z]/.test(value)) score++;
            if (/[a-z]/.test(value)) score++;
            if (/[0-9]/.test(value)) score++;
            if (/[^A-Za-z0-9]/.test(value)) score++;

            switch (score) {

                case 1:
                    bar.style.width = "20%";
                    bar.style.background = "red";
                    break;

                case 2:
                    bar.style.width = "40%";
                    bar.style.background = "orange";
                    break;

                case 3:
                    bar.style.width = "60%";
                    bar.style.background = "#FFD700";
                    break;

                case 4:
                    bar.style.width = "80%";
                    bar.style.background = "#4CAF50";
                    break;

                case 5:
                    bar.style.width = "100%";
                    bar.style.background = "lime";
                    break;

                default:
                    bar.style.width = "0";
            }

        });

    }

    // ==========================
    // Card Hover Animation
    // ==========================

    const card = document.querySelector(".register-card");

    if (card) {

        card.addEventListener("mousemove", function (e) {

            let rect = card.getBoundingClientRect();

            let x = e.clientX - rect.left;
            let y = e.clientY - rect.top;

            let rotateX = -(y - rect.height / 2) / 18;
            let rotateY = (x - rect.width / 2) / 18;

            card.style.transform =
                `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;

        });

        card.addEventListener("mouseleave", function () {

            card.style.transform =
                "rotateX(0deg) rotateY(0deg)";

        });

    }

    // ==========================
    // Button Loading Animation
    // ==========================

    const form = document.querySelector(".register-form");

    if (form) {

        form.addEventListener("submit", function () {

            const btn = document.querySelector(".btn-register");

            btn.innerHTML = "Creating Account...";

            btn.disabled = true;

        });

    }

    // ==========================
    // Floating Inputs
    // ==========================

    const inputs = document.querySelectorAll("input");

    inputs.forEach(function (input) {

        input.addEventListener("focus", function () {

            input.style.transform = "scale(1.03)";

        });

        input.addEventListener("blur", function () {

            input.style.transform = "scale(1)";

        });

    });

});