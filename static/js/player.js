const players = document.querySelectorAll(".player");

players.forEach(player => {
  const audio = player.querySelector("audio");
  const bars = player.querySelectorAll(".bar");

  audio.addEventListener("play", () => {
    players.forEach(p => {
      if (p !== player) {
        p.classList.remove("playing");
        const a = p.querySelector("audio");
        a.pause();
      }
    });

    player.classList.add("playing");
    bars.forEach(b => b.classList.add("active"));
  });

  audio.addEventListener("pause", () => {
    player.classList.remove("playing");
    bars.forEach(b => b.classList.remove("active"));
  });

  audio.addEventListener("ended", () => {
    player.classList.remove("playing");
    bars.forEach(b => b.classList.remove("active"));
  });
});
