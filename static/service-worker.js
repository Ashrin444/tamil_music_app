self.addEventListener("install", e => {
  e.waitUntil(
    caches.open("music-v1").then(cache =>
      cache.addAll(["/"])
    )
  );
});
