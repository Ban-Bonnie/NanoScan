window.onload = function () {
    setTimeout(() => {
        let loader = document.getElementById("loader-container");
        let content = document.getElementById("main-content");

        if (loader) {
            loader.style.opacity = "0";
            setTimeout(() => {
                loader.style.display = "none";
            }, 500);
        }

        if (content) {
            content.style.display = "block";
            content.style.opacity = "0";
            setTimeout(() => {
                content.style.opacity = "1";
            }, 100);
        }
    }, 1500);
};
