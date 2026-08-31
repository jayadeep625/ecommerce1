// ============================
// Live Address Preview
// ============================

const fullName = document.querySelector('input[name="full_name"]');
const phone = document.querySelector('input[name="phone"]');
const email = document.querySelector('input[name="email"]');
const house = document.querySelector('input[name="house"]');
const street = document.querySelector('input[name="street"]');
const city = document.querySelector('input[name="city"]');
const state = document.querySelector('input[name="state"]');
const pincode = document.querySelector('input[name="pincode"]');

function updatePreview(input, previewId, defaultText) {
    if (!input) return;

    input.addEventListener("input", () => {
        document.getElementById(previewId).innerText =
            input.value || defaultText;
    });
}

updatePreview(fullName, "preview-name", "Your Name");
updatePreview(phone, "preview-phone", "Phone Number");
updatePreview(email, "preview-email", "Email Address");
updatePreview(house, "preview-house", "House / Flat");
updatePreview(street, "preview-street", "Street");
updatePreview(city, "preview-city", "City");
updatePreview(state, "preview-state", "State");
updatePreview(pincode, "preview-pin", "Pincode");

// ============================
// 3D Card Tilt
// ============================

const card = document.querySelector(".glass-card");

if (card) {
    card.addEventListener("mousemove", (e) => {

        const rect = card.getBoundingClientRect();

        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const rotateY = ((x / rect.width) - 0.5) * 12;
        const rotateX = ((0.5 - y / rect.height)) * 12;

        card.style.transform =
            `perspective(1200px)
             rotateX(${rotateX}deg)
             rotateY(${rotateY}deg)
             scale(1.02)`;

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform =
            "perspective(1200px) rotateX(0deg) rotateY(0deg)";

    });
}

// ============================
// Button Ripple Animation
// ============================

const button = document.querySelector(".save-btn");

if (button) {

    button.addEventListener("click", function(e){

        const ripple = document.createElement("span");

        const rect = this.getBoundingClientRect();

        ripple.style.left = (e.clientX - rect.left) + "px";
        ripple.style.top = (e.clientY - rect.top) + "px";

        ripple.classList.add("ripple");

        this.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);

    });

}

// ============================
// Fade-in Animation
// ============================

window.addEventListener("load", () => {

    document.querySelectorAll(".input-box").forEach((box, index) => {

        box.style.opacity = "0";
        box.style.transform = "translateY(30px)";

        setTimeout(() => {

            box.style.transition = ".5s";

            box.style.opacity = "1";

            box.style.transform = "translateY(0px)";

        }, index * 120);

    });

});