function uploadFiles() {
    const input = document.getElementById("pdfInput");

    if (input.files.length === 0) {
        alert("Please select at least one PDF file.");
        return;
    }

    const formData = new FormData();

    Array.from(input.files).forEach(file => {
        console.log(file.name + " , " + file);
        formData.append(file.name, file);
    });

    fetch('/upload/', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });

}