const BACKEND_URL = "https://ai-video-tools-dmpw.onrender.com";

async function send(action) {
  const fileInput = document.getElementById("video");
  const result = document.getElementById("result");

  if (!fileInput.files.length) {
    result.textContent = "Please select a video file";
    return;
  }

  const file = fileInput.files[0];

  // file size check (5MB – 25MB)
  const sizeMB = file.size / (1024 * 1024);
  if (sizeMB < 5 || sizeMB > 25) {
    result.textContent = "File size must be between 5MB and 25MB";
    return;
  }

  const formData = new FormData();
  formData.append("video", file);

  result.textContent = "Processing...";

  try {
    const res = await fetch(`${BACKEND_URL}/extract-audio`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      throw new Error("Server error");
    }

    const data = await res.json();
    result.textContent = data.message || "Done";
  } catch (err) {
    result.textContent = "Server error ❌";
  }
}
