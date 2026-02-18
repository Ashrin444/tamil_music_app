document.querySelectorAll(".playlist-form").forEach(form => {
  form.addEventListener("submit", () => {
    setTimeout(() => location.reload(), 300);
  });
});
