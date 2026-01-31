function send(action) {
  const url = document.getElementById("videoUrl").value;
  const result = document.getElementById("result");

  if (!url) {
    alert("Please paste a video URL");
    return;
  }

  result.textContent = "Processing... ⏳";

  fetch("https://YOUR-BACKEND-URL.onrender.com/process", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      url: url,
      action: action
    })
  })
  .then(res => res.json())
  .then(data => {
    result.textContent = JSON.stringify(data, null, 2);
  })
  .catch(() => {
    result.textContent = "Server error ❌";
  });
}
