document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('file-input');
    formData.append('pdf_file', fileInput.files[0]);

    const response = await fetch('/convert', {
        method: 'POST',
        body: formData
    });

    const result = await response.blob();
    const url = window.URL.createObjectURL(result);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'converted.docx';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
});
