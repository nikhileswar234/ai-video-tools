const API = "https://YOUR-RENDER-URL.onrender.com";

function send(type) {
  const file = document.getElementById("video").files[0];
  if (!file) {
    alert("Upload a video first");
    return;
  }

  const formData = new FormData();
  formData.append("video", file);

  fetch(`${API}/${type}`, {
    method: "POST",
    body: formData
  })
  .then(res => {
    if (type === "metadata") return res.json();
    return res.blob();
  })
  .then(data => {
    if (type === "metadata") {
      document.getElementById("result").textContent =
        JSON.stringify(data, null, 2);
    } else {
      const url = window.URL.createObjectURL(data);
      const a = document.createElement("a");
      a.href = url;
      a.download = "output";
      a.click();
    }
  })
  .catch(() => alert("Server error or file too large"));
}
