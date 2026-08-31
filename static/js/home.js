document.addEventListener("DOMContentLoaded", () => {

    /* ==========================
       Navbar Scroll Effect
    ========================== */

    const navbar = document.querySelector(".navbar");

    window.addEventListener("scroll", () => {

        if(window.scrollY > 40){

            navbar.style.background = "rgba(5,8,22,.95)";
            navbar.style.boxShadow = "0 5px 25px rgba(0,255,255,.2)";

        }

        else{

            navbar.style.background = "rgba(5,8,22,.85)";
            navbar.style.boxShadow = "none";

        }

    });


    /* ==========================
        Hero Fade Animation
    ========================== */

    const hero = document.querySelector(".hero");

    hero.style.opacity = "0";
    hero.style.transform = "translateY(60px)";

    setTimeout(() => {

        hero.style.transition = "1s ease";

        hero.style.opacity = "1";

        hero.style.transform = "translateY(0px)";

    },300);



    /* ==========================
         Button Hover Glow
    ========================== */

    document.querySelectorAll(".btn-primary,.btn-secondary,.book-btn")

    .forEach(button=>{

        button.addEventListener("mouseenter",()=>{

            button.style.boxShadow="0 0 35px cyan";

        });

        button.addEventListener("mouseleave",()=>{

            button.style.boxShadow="none";

        });

    });



    /* ==========================
         Mouse Parallax
    ========================== */

    const glow1=document.querySelector(".glow1");
    const glow2=document.querySelector(".glow2");

    document.addEventListener("mousemove",(e)=>{

        let x=(window.innerWidth/2-e.pageX)/40;
        let y=(window.innerHeight/2-e.pageY)/40;

        glow1.style.transform=
        `translate(${x}px,${y}px)`;

        glow2.style.transform=
        `translate(${-x}px,${-y}px)`;

    });



    /* ==========================
        Floating Animation
    ========================== */

    let angle=0;

    setInterval(()=>{

        angle+=0.02;

        glow1.style.top=
        (-180+Math.sin(angle)*20)+"px";

        glow2.style.bottom=
        (-180+Math.cos(angle)*20)+"px";

    },30);



    /* ==========================
        Typing Effect
    ========================== */

    const heading=document.querySelector(".hero span");

    const text=heading.innerText;

    heading.innerText="";

    let i=0;

    function type(){

        if(i<text.length){

            heading.innerHTML+=text.charAt(i);

            i++;

            setTimeout(type,80);

        }

    }

    setTimeout(type,800);



    /* ==========================
        Button Click Ripple
    ========================== */

    document.querySelectorAll("a").forEach(btn=>{

        btn.addEventListener("click",function(e){

            const ripple=document.createElement("span");

            ripple.className="ripple";

            ripple.style.left=e.offsetX+"px";
            ripple.style.top=e.offsetY+"px";

            this.appendChild(ripple);

            setTimeout(()=>{

                ripple.remove();

            },600);

        });

    });

});