let index = 0;
let isPlaying = false;

const audio = document.getElementById("audio");
const title = document.getElementById("song-title");
const cover = document.getElementById("cover");
const player = document.getElementById("dj-player");
const canvas = document.getElementById("visualizer");
const ctx2d = canvas.getContext("2d");

const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
const source = audioCtx.createMediaElementSource(audio);

const bassFilter = audioCtx.createBiquadFilter();
bassFilter.type = "lowshelf";
bassFilter.frequency.value = 200;

const vocalFilter = audioCtx.createBiquadFilter();
vocalFilter.type = "highshelf";
vocalFilter.frequency.value = 2500;

const analyser = audioCtx.createAnalyser();
analyser.fftSize = 256;

source.connect(bassFilter);
bassFilter.connect(vocalFilter);
vocalFilter.connect(analyser);
analyser.connect(audioCtx.destination);

document.getElementById("bass").oninput = e => {
  bassFilter.gain.value = e.target.value;
};

document.getElementById("vocals").oninput = e => {
  vocalFilter.gain.value = e.target.value;
};

function loadSong() {
  const song = PLAYLIST[index];
  audio.src = `/static/songs/${song.filename}`;
  title.innerText = song.title;
  cover.src = `/static/images/${song.image}`;
}

function togglePlay() {
  if (!isPlaying) {
    audioCtx.resume();
    audio.play();
    isPlaying = true;
    player.classList.add("playing");
  } else {
    audio.pause();
    isPlaying = false;
    player.classList.remove("playing");
  }
}

function nextSong() {
  index = (index + 1) % PLAYLIST.length;
  loadSong();
  audio.play();
}

function prevSong() {
  index = (index - 1 + PLAYLIST.length) % PLAYLIST.length;
  loadSong();
  audio.play();
}

audio.onended = nextSong;

function drawVisualizer() {
  requestAnimationFrame(drawVisualizer);
  const data = new Uint8Array(analyser.frequencyBinCount);
  analyser.getByteFrequencyData(data);

  ctx2d.clearRect(0, 0, canvas.width, canvas.height);
  const barWidth = canvas.width / data.length;

  data.forEach((v, i) => {
    ctx2d.fillStyle = `rgb(${v + 50},50,50)`;
    ctx2d.fillRect(i * barWidth, canvas.height - v, barWidth - 2, v);
  });
}

loadSong();
drawVisualizer();
