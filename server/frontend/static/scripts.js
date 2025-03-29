function uploadFiles() {
    const input = document.getElementById("pdfInput");
    const fileContainer = document.querySelector('.file-name');
    const fileItems = fileContainer.querySelectorAll('.file-item');

    if (input.files.length === 0) {
        alert("Please select at least one PDF file.");
        return;
    }

    const formData = new FormData();

    // Get all files and their colors
    fileItems.forEach((item, index) => {
        const file = input.files[index];
        const color = item.querySelector('input[type="color"]').value;
        console.log(`File: ${file.name}, Color: ${color}`);
        formData.append(`file_${index}`, file);
        formData.append(`color_${index}`, color);
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

// Distinct colors that are visually different from each other
const distinctColors = [
    '#FF6B6B', // Coral Red
    '#4ECDC4', // Turquoise
    '#45B7D1', // Sky Blue
    '#96CEB4', // Sage Green
    '#FFEEAD', // Cream Yellow
    '#D4A5A5', // Dusty Rose
    '#9B59B6', // Purple
    '#3498DB', // Blue
    '#E67E22', // Orange
    '#2ECC71', // Emerald Green
    '#E74C3C', // Red
    '#1ABC9C', // Turquoise
    '#F1C40F', // Yellow
    '#8E44AD', // Dark Purple
    '#16A085', // Green
    '#D35400', // Dark Orange
    '#2980B9', // Dark Blue
    '#27AE60', // Dark Green
    '#C0392B', // Dark Red
    '#7F8C8D'  // Gray
];

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

    // Loop through each file and add the filename with a color picker
    Array.from(files).forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        const fileInfo = document.createElement('div');
        fileInfo.className = 'file-info';
        
        const fileName = document.createElement('span');
        fileName.textContent = file.name;
        
        const colorPicker = document.createElement('input');
        colorPicker.type = 'color';
        colorPicker.value = distinctColors[index % distinctColors.length]; // Cycle through distinct colors
        colorPicker.className = 'color-picker';
        
        fileInfo.appendChild(fileName);
        fileInfo.appendChild(colorPicker);
        fileItem.appendChild(fileInfo);
        fileNameParagraph.appendChild(fileItem);
    });
});