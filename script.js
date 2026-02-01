const BACKEND_URL = " https://ai-video-tools-s0oo.onrender.com";

async function extractAudio() {
  const fileInput = document.getElementById("video");
  const result = document.getElementById("result");

  if (!fileInput.files.length) {
    result.textContent = "❌ Please select a video";
    return;
  }

  const file = fileInput.files[0];

  if (file.size < 5 * 1024 * 1024 || file.size > 25 * 1024 * 1024) {
    result.textContent = "❌ File size must be 5MB–25MB";
    return;
  }

  const formData = new FormData();
  formData.append("video", file);

  result.textContent = "⏳ Processing...";

  try {
    const res = await fetch(`${BACKEND_URL}/extract-audio`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (data.success) {
      result.textContent = "✅ Audio extracted successfully";
    } else {
      result.textContent = "❌ Server error";
    }
  } catch (err) {
    result.textContent = "❌ Server error";
  }
}
