const enhanceBtn = document.getElementById("enhanceBtn");
const userPrompt = document.getElementById("userPrompt");
const result = document.getElementById("result");
const loading = document.getElementById("loading");

enhanceBtn.addEventListener("click", async () => {
  const prompt = userPrompt.value.trim();
  if (!prompt) {
    alert("Please enter a prompt.");
    return;
  }

  result.textContent = "";
  loading.style.display = "block";

  try {
    const response = await fetch("http://localhost:8000/enhance", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_prompt: prompt }),
    });

    if (!response.ok) throw new Error("Network response was not ok");

    const data = await response.json();
    result.textContent = data.enhanced_prompt || "No enhanced prompt received.";
  } catch (error) {
    result.textContent = `Error: ${error.message}`;
  } finally {
    loading.style.display = "none";
  }
});
