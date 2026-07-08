document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById("loader");
    const loaderText = document.getElementById("loader-text");
    const mainContent = document.getElementById("main-content");
    const audioBtn = document.getElementById("audio-btn");
    const audioText = document.getElementById("audio-text");

    // --- A. Loader Sequence Animation ---
    setTimeout(() => {
        // Step 1: Scale text in smoothly
        loaderText.classList.remove("scale-90", "opacity-0");
        loaderText.classList.add("scale-110", "opacity-100");
    }, 200);

    setTimeout(() => {
        // Step 2: Slide up & Fade loader container out
        loader.classList.add("-translate-y-full", "opacity-0");
        // Step 3: Enable scrolling and show main body contents
        document.body.classList.remove("overflow-hidden");
        mainContent.classList.remove("opacity-0");
    }, 2200);


    // --- B. Audio Controller System ---
    let isPlaying = false;
    
    // To include a voiceover like the video, insert your audio file name inside the quotes below:
    const audioTrack = new Audio(""); 

    audioBtn.addEventListener("click", () => {
        isPlaying = !isPlaying;
        if (isPlaying) {
            audioText.innerHTML = "■ Pause Intro";
            if (audioTrack.src) {
                audioTrack.play().catch(e => console.log("Audio track source path is empty or unassigned."));
            }
        } else {
            audioText.innerHTML = "▶ Play Intro";
            audioTrack.pause();
        }
    });
    
    // Automatically revert button text layout if the audio track finishes naturally
    audioTrack.addEventListener("ended", () => {
        isPlaying = false;
        audioText.innerHTML = "▶ Play Intro";
    });
});