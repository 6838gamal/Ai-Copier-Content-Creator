async function generateContent() {
    const prompt = document.getElementById("prompt").value;

    const res = await fetch("/api/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt: prompt })
    });

    const data = await res.json();
    document.getElementById("result").innerText = data.response;
}

async function checkStatus() {
    const res = await fetch("/api/status");
    const data = await res.json();

    document.getElementById("statusResult").innerText =
        JSON.stringify(data, null, 2);
}
