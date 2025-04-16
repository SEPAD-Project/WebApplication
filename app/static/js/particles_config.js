particlesJS("particles-js", {
    particles: {
        number: { value: 50, density: { enable: true, value_area: 800 } },
        color: { value: "#FFFFFF" },
        shape: { type: "circle" },
        opacity: { value: 0.5, random: true },
        size: { value: 3, random: true },
        move: { enable: true, speed: 3, direction: "none", random: true },
    },
    interactivity: {
        events: { onhover: { enable: true, mode: "repulse" } },
    },
});