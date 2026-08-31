const profile = document.querySelector(".profile-menu");

if (profile) {

    profile.addEventListener("click", function (e) {

        e.preventDefault();

        e.stopPropagation();

        profile.classList.toggle("active");

    });

    document.addEventListener("click", function () {

        profile.classList.remove("active");

    });

}