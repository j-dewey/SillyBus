function uploadFiles() {
    const input = document.getElementById("pdfInput");

    if (input.files.length === 0) {
        alert("Please select at least one PDF file.");
        return;
    }

    const formData = new FormData();

    Array.from(input.files).forEach(file => {
        console.log(file.name + " , " + file);
        formData.append("file_name", file.name);
        formData.append("file", file);
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

// list pdfs
const fileInput = document.querySelector('#pdfInput');
fileInput.addEventListener('change', (e) => {
    console.log("Files added");

    // Get the selected files
    const files = e.target.files;

    // Get the element where you want to display the filenames
    const fileNameParagraph = document.querySelector('.file-name');

    // Clear the existing content before adding new filenames
    fileNameParagraph.innerHTML = '';

    // Loop through each file and add the filename with a line break
    for (const file of files) {
        const fileName = file.name;
        fileNameParagraph.innerHTML += `${fileName}<br>`;
    }
});