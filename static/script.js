document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predict-form");
  const resultBox = document.getElementById("result");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const obj = {};
    for (const [k, v] of formData.entries()) {
      obj[k] = parseFloat(v);
    }

    resultBox.innerText = "Predicting...";

    try {
      const resp = await fetch("/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(obj)
      });

      const data = await resp.json();
      if (resp.ok) {
        resultBox.innerText = "Predicted Fare: $" + data.prediction.toFixed(2);
      } else {
        resultBox.innerText = "Error: " + (data.error || "Unknown error");
      }
    } catch (err) {
      resultBox.innerText = "Request failed: " + err.message;
    }
  });
});