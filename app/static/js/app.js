// توليد المحتوى
async function generateContent() {
    const prompt = document.getElementById("prompt").value;
    const resultDiv = document.getElementById("result");

    if (!prompt.trim()) {
        resultDiv.innerHTML = "<em>يرجى كتابة طلبك أولاً!</em>";
        return;
    }

    resultDiv.innerHTML = "⏳ جاري التوليد...";

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt })
        });
        const data = await response.json();
        resultDiv.innerHTML = data.output || "<em>لا توجد نتيجة.</em>";
    } catch (error) {
        resultDiv.innerHTML = "<span style='color:red;'>حدث خطأ أثناء التوليد.</span>";
        console.error(error);
    }
}

// حالة النظام
async function checkStatus() {
    const statusDiv = document.getElementById("statusResult");
    statusDiv.textContent = "⏳ جاري التحقق...";

    try {
        const response = await fetch("/status");
        const data = await response.json();
        statusDiv.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        statusDiv.innerHTML = "❌ حدث خطأ أثناء التحقق.";
        console.error(error);
    }
}

// رفع المصادر
async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const ingestResult = document.getElementById("ingestResult");

    if (!fileInput.files.length) {
        ingestResult.textContent = "❌ اختر ملف أولاً.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    ingestResult.textContent = "⏳ جاري رفع الملف...";

    try {
        const response = await fetch("/ingest", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        ingestResult.textContent = data.message;
    } catch (error) {
        ingestResult.textContent = "❌ حدث خطأ أثناء رفع الملف.";
        console.error(error);
    }
}
