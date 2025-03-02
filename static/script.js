document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    let formData = new FormData();
    let fileInput = document.getElementById("fileInput");
    formData.append("file", fileInput.files[0]);

    try {
        let response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            let errorData = await response.json();
            alert("Помилка: " + errorData.error);
            return;
        }

        let blob = await response.blob();
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = "output.json";
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (error) {
        alert("Помилка завантаження файлу");
    }
});
