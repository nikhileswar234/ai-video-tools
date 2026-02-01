function upload() {
  const fileInput = document.getElementById("video");
  const result = document.getElementById("result");

  if (!fileInput.files.length) {
    alert("Please select a video file");
    return;
  }

  const file = fileInput.files[0];

  // Size limits (in bytes)
  const MIN_SIZE = 5 * 1024 * 1024;   // 5MB
  const MAX_SIZE = 25 * 1024 * 1024;  // 25MB

  if (file.size < MIN_SIZE) {
    alert("File too small (minimum 5MB)");
    return;
  }

  if (file.size > MAX_SIZE) {
    alert("File too large (maximum 25MB)");
    return;
  }

  const formData = new FormData();
  formData.append("video", file);

  result.textContent = "Uploading & processing... ⏳";

  fetch("https://ai-video-tools-s0oo.onrender.com", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    result.textContent = JSON.stringify(data, null, 2);
  })
  .catch(() => {
    result.textContent = "Server error ❌";
  });
}


